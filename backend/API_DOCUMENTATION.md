# BookClub Platform API Documentation

## Overview

Complete backend API for the BookClub reading platform with Google OAuth authentication, group management, book tracking, and comment visibility based on reading progress.

## Key Features

- **Google OAuth Authentication**: Secure user authentication via Google
- **Group Management**: Create groups, join via invite codes (max 32 members)
- **Book Integration**: Search books via Open Library API
- **Reading Progress Tracking**: Track user reading progress per book per group
- **Comment Visibility System**: Comments visible only when user's progress >= comment's progress + 3% buffer
- **Comment Likes**: Like/unlike comments
- **Role-Based Access**: Admin and member roles for groups

## API Endpoints

### Authentication (`/auth`)

#### `POST /auth/google`
Authenticate user with Google ID token
- **Request**: `{ "token": "google-id-token" }`
- **Response**: JWT access token + user info

#### `GET /auth/me`
Get current authenticated user
- **Auth**: Required
- **Response**: User information

#### `POST /auth/logout`
Logout user (client-side token removal)
- **Auth**: Required

#### `POST /auth/refresh`
Refresh JWT token
- **Auth**: Required
- **Response**: New JWT token

### Users (`/users`)

#### `GET /users/me`
Get current user's profile
- **Auth**: Required

#### `PUT /users/me`
Update current user's profile
- **Auth**: Required
- **Body**: `{ "name": "...", "avatar_url": "..." }`

#### `GET /users/{user_id}`
Get public user information
- **Auth**: Required

### Groups (`/groups`)

#### `POST /groups`
Create a new group
- **Auth**: Required
- **Body**: `{ "name": "...", "description": "..." }`
- **Returns**: Group with unique invite code

#### `GET /groups`
Get all groups user is member of
- **Auth**: Required

#### `GET /groups/{group_id}`
Get specific group details with members
- **Auth**: Required (must be member)

#### `PUT /groups/{group_id}`
Update group (admin only)
- **Auth**: Required (admin)
- **Body**: `{ "name": "...", "description": "..." }`

#### `DELETE /groups/{group_id}`
Delete group (admin only)
- **Auth**: Required (admin)

#### `POST /groups/join`
Join group via invite code
- **Auth**: Required
- **Body**: `{ "invite_code": "ABCD1234EFGH" }`

#### `POST /groups/{group_id}/leave`
Leave a group
- **Auth**: Required

#### `GET /groups/{group_id}/members`
Get all group members
- **Auth**: Required (must be member)

#### `DELETE /groups/{group_id}/members/{member_id}`
Remove member from group (admin only)
- **Auth**: Required (admin)

#### `POST /groups/{group_id}/members/{member_id}/promote`
Promote member to admin (admin only)
- **Auth**: Required (admin)

### Books (`/books`)

#### `GET /books/search?q={query}&limit={limit}`
Search books via Open Library API
- **Auth**: Required
- **Query Params**:
  - `q`: Search query (required)
  - `limit`: Max results 1-50 (default: 10)

#### `POST /books/groups/{group_id}/books`
Add book to group
- **Auth**: Required (must be member)
- **Body**: Either `{ "book_id": "..." }` or new book data

#### `GET /books/groups/{group_id}/books`
Get all books in a group
- **Auth**: Required (must be member)

### Comments (`/comments`)

#### `POST /comments/groups/{group_id}/comments`
Create comment
- **Auth**: Required (must be member)
- **Body**:
```json
{
  "book_id": "uuid",
  "content": "1-1000 chars",
  "progress_page": 50,
  "progress_total_pages": 300
}
```

#### `GET /comments/groups/{group_id}/books/{book_id}/comments`
Get visible comments for a book
- **Auth**: Required
- **Visibility**: Only shows comments where `comment.progress_percentage <= user.progress_percentage - 3.0`

#### `GET /comments/comments/{comment_id}`
Get specific comment (with visibility check)
- **Auth**: Required

#### `PUT /comments/comments/{comment_id}`
Update comment (own comments only)
- **Auth**: Required (owner)
- **Body**: `{ "content": "..." }`

#### `DELETE /comments/comments/{comment_id}`
Delete comment (own comments only)
- **Auth**: Required (owner)

#### `POST /comments/comments/{comment_id}/like`
Like a comment
- **Auth**: Required

#### `DELETE /comments/comments/{comment_id}/like`
Unlike a comment
- **Auth**: Required

### Reading Progress (`/progress`)

#### `POST /progress`
Create or update reading progress
- **Auth**: Required
- **Body**:
```json
{
  "book_id": "uuid",
  "group_id": "uuid",
  "current_page": 150,
  "total_pages": 300
}
```

#### `GET /progress?group_id={group_id}`
Get all user's reading progress (optionally filtered by group)
- **Auth**: Required

#### `GET /progress/groups/{group_id}/books/{book_id}`
Get user's progress for specific book
- **Auth**: Required

#### `GET /progress/groups/{group_id}/books/{book_id}/all`
Get all members' progress for a book
- **Auth**: Required (must be member)

#### `PUT /progress/{progress_id}`
Update progress
- **Auth**: Required (owner)
- **Body**: `{ "current_page": 200, "total_pages": 300 }`

#### `DELETE /progress/{progress_id}`
Delete progress
- **Auth**: Required (owner)

## Comment Visibility Logic

**Critical Feature**: Comments are filtered based on reading progress to prevent spoilers.

```python
# User can see comment if:
comment.progress_percentage <= user.progress_percentage - 3.0

# Examples:
# User at 50% can see comments up to 47%
# User at 10% can see comments up to 7%
# User with no progress can only see 0% comments
```

## Business Rules

1. **Group Member Limit**: Maximum 32 members per group
2. **Comment Length**: 1-1000 characters
3. **Progress Buffer**: 3% buffer for comment visibility
4. **Roles**:
   - Admin: Can manage group, remove members, promote members
   - Member: Can view, add books, comment, track progress
5. **Last Admin**: Cannot remove/leave if you're the last admin

## Authentication

All endpoints (except `/auth/google`) require JWT Bearer token:

```
Authorization: Bearer <jwt-token>
```

## Error Responses

Standard error format:
```json
{
  "detail": "Error message",
  "message": "User-friendly message"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request (validation error)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `422`: Unprocessable Entity (validation error)
- `500`: Internal Server Error

## Database Models

### User
- Google OAuth authentication
- Name, email, avatar
- Created/last login timestamps

### Group
- Name, description
- Unique 12-character invite code
- Creator reference
- Max 32 members

### Book
- Title, author
- ISBN, Open Library ID
- Cover URL (hotlinked from Open Library)

### Comment
- Content (1-1000 chars)
- Progress tracking (page/total pages)
- Calculated progress percentage
- Likes/reactions

### UserReadingProgress
- Current page / total pages
- Calculated progress percentage
- Per user, per book, per group

### GroupMember
- User-Group association
- Role (admin/member)
- Join timestamp

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your credentials

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Environment Variables
See `.env.example` for all required configuration.

### API Documentation
- Swagger UI: `http://localhost:8000/docs` (development only)
- ReDoc: `http://localhost:8000/redoc` (development only)

## Health Checks

- `GET /`: Basic health check
- `GET /health`: Detailed health check with database status
