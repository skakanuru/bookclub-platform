"""Book service for Open Library API integration and book management."""
from typing import List, Optional
from uuid import UUID
import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..config import get_settings
from ..models.book import Book, GroupBook
from ..models.group import Group, GroupMember
from ..schemas.book import BookCreate, BookSearchResult, GroupBookCreate

settings = get_settings()


class BookService:
    """Service for handling book operations."""

    @staticmethod
    async def search_books(query: str, limit: int = 10) -> List[BookSearchResult]:
        """
        Search books using Open Library API.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of BookSearchResult

        Raises:
            HTTPException: If API request fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.open_library_api_url}/search.json",
                    params={
                        "q": query,
                        "limit": limit,
                        "fields": "key,title,author_name,isbn,cover_i,first_publish_year"
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for doc in data.get("docs", []):
                    # Get first author
                    author = doc.get("author_name", ["Unknown"])[0] if doc.get("author_name") else "Unknown"

                    # Get ISBN
                    isbn = None
                    if doc.get("isbn"):
                        isbn = doc["isbn"][0]

                    # Get Open Library ID (from key like "/works/OL123W")
                    ol_id = None
                    if doc.get("key"):
                        ol_id = doc["key"].split("/")[-1]

                    # Get cover URL
                    cover_url = None
                    if doc.get("cover_i"):
                        cover_url = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"

                    results.append(BookSearchResult(
                        title=doc.get("title", "Unknown Title"),
                        author=author,
                        isbn=isbn,
                        open_library_id=ol_id,
                        cover_url=cover_url,
                        publish_year=doc.get("first_publish_year")
                    ))

                return results

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to search books: {str(e)}"
            )

    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        """
        Create a new book in the database.

        Args:
            db: Database session
            book_data: Book creation data

        Returns:
            Created Book instance
        """
        # Check if book already exists by ISBN or Open Library ID
        if book_data.isbn:
            existing = db.query(Book).filter(Book.isbn == book_data.isbn).first()
            if existing:
                return existing

        if book_data.open_library_id:
            existing = db.query(Book).filter(
                Book.open_library_id == book_data.open_library_id
            ).first()
            if existing:
                return existing

        # Create new book
        book = Book(
            title=book_data.title,
            author=book_data.author,
            isbn=book_data.isbn,
            open_library_id=book_data.open_library_id,
            cover_url=book_data.cover_url
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def get_book(db: Session, book_id: UUID) -> Book:
        """
        Get a book by ID.

        Args:
            db: Database session
            book_id: Book UUID

        Returns:
            Book instance

        Raises:
            HTTPException: If book not found
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book

    @staticmethod
    def add_book_to_group(
        db: Session,
        group_id: UUID,
        user_id: UUID,
        book_data: GroupBookCreate
    ) -> GroupBook:
        """
        Add a book to a group.

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID (must be member of group)
            book_data: Book data (either existing book_id or new book info)

        Returns:
            Created GroupBook instance

        Raises:
            HTTPException: If group not found or user not member
        """
        # Verify group exists
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Verify user is member of group
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group to add books"
            )

        # Get or create book
        if book_data.book_id:
            book = db.query(Book).filter(Book.id == book_data.book_id).first()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
        else:
            # Create new book from provided data
            if not book_data.title or not book_data.author:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title and author are required to create a new book"
                )
            book = BookService.create_book(
                db,
                BookCreate(
                    title=book_data.title,
                    author=book_data.author,
                    isbn=book_data.isbn,
                    open_library_id=book_data.open_library_id,
                    cover_url=book_data.cover_url
                )
            )

        # Check if book already added to group
        existing = db.query(GroupBook).filter(
            GroupBook.group_id == group_id,
            GroupBook.book_id == book.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book already added to this group"
            )

        # Create group book association
        group_book = GroupBook(
            group_id=group_id,
            book_id=book.id,
            added_by=user_id
        )
        db.add(group_book)
        db.commit()
        db.refresh(group_book)
        return group_book

    @staticmethod
    def get_group_books(db: Session, group_id: UUID, user_id: UUID) -> List[GroupBook]:
        """
        Get all books for a group.

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID (must be member of group)

        Returns:
            List of GroupBook instances

        Raises:
            HTTPException: If user not member of group
        """
        # Verify user is member of group
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group to view books"
            )

        return db.query(GroupBook).filter(GroupBook.group_id == group_id).all()
