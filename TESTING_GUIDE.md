# Testing Guide - BookClub Platform MVP

## Quick Test Checklist

Use this checklist when testing with your book club:

### 1. Authentication ✓
- [ ] Can log in with Google
- [ ] User profile shows correct name and email
- [ ] Can log out successfully
- [ ] Protected routes redirect to login

### 2. Group Management ✓
- [ ] Can create a new group
- [ ] Group shows unique invite code
- [ ] Can copy invite code
- [ ] Can join group via invite link
- [ ] Can see list of group members
- [ ] Admin can add books to group
- [ ] Regular members cannot add books

### 3. Book Management ✓
- [ ] Can search for books by title/author
- [ ] Search shows results from Open Library
- [ ] Can add book to group (admin only)
- [ ] Book cover displays correctly
- [ ] Can see book details in group

### 4. Reading Progress ✓
- [ ] Can set initial progress (page + total pages)
- [ ] Can update progress at any time
- [ ] Progress shows as percentage
- [ ] Different users can have different editions

### 5. Comment System ✓
- [ ] Can post comment at current progress
- [ ] Character counter shows (max 1000)
- [ ] Comment shows user's name and avatar
- [ ] Comments display chronologically
- [ ] Can see own comments immediately

### 6. Comment Visibility (CRITICAL) ✓
- [ ] User at 50% CANNOT see comments from 60%
- [ ] User at 50% CAN see comments from 47% (within 3% buffer)
- [ ] User at 50% CAN see comments from 30%
- [ ] Badge shows count of unread comments ahead
- [ ] Clicking badge shows list of comments ahead (no content)

### 7. Social Features ✓
- [ ] Can like/unlike comments
- [ ] Like count updates in real-time
- [ ] Can report spoilers
- [ ] Report button works

### 8. Avatar System ✓
- [ ] Google avatar shows by default
- [ ] Can upload custom avatar
- [ ] Avatar displays in comments
- [ ] Avatar displays in profile

### 9. Mobile Responsiveness ✓
- [ ] Site works on phone browser
- [ ] All buttons are tap-friendly
- [ ] Text is readable
- [ ] Navigation works

### 10. Error Handling ✓
- [ ] Shows error when internet disconnects
- [ ] Shows loading states
- [ ] Handles invalid invite codes gracefully
- [ ] Shows helpful error messages

## Detailed Test Scenarios

### Scenario 1: New User Joins Book Club

**Setup:** User has never used the app

1. User receives invite link from friend: `http://localhost:5173/join/ABC123XYZ`
2. Click link → Redirected to login
3. Click "Sign in with Google" → Google OAuth flow
4. After auth → Automatically joins group
5. Lands on group page
6. Sees book cover and title
7. Sees prompt: "Set your progress to start reading"
8. Enter total pages: 300, current page: 0
9. Click "Update Progress"
10. Can now see comments from page 0

**Expected:** Smooth onboarding, no errors, clear next steps

### Scenario 2: Posting First Comment

**Setup:** User has set progress to page 50 (16.7%)

1. Scroll to comment input at bottom
2. See current progress displayed: "Commenting at Page 50 (16.7%)"
3. Type comment: "Wow, the plot twist at the end of chapter 3 was amazing!"
4. Character counter shows: "62 / 1000"
5. Click "Post Comment"
6. Comment appears immediately in feed
7. Other users' "unread ahead" counters update

**Expected:** Instant feedback, no lag, comment visible immediately

### Scenario 3: Spoiler Protection Test

**Setup:**
- User A is at page 100 (33%)
- User B is at page 150 (50%)
- User C is at page 200 (67%)

**Test:**
1. User C posts comment at page 200: "I can't believe the main character died!"
2. User B sees notification: "1 comment ahead at page 200 (67%)"
3. User B clicks notification → Sees "User C commented at page 200" (no content shown)
4. User A also sees notification but cannot see content
5. User B updates progress to page 200
6. User B can now see User C's comment
7. User A still cannot see it

**Expected:** Perfect isolation, no spoilers leaked

### Scenario 4: Multiple Users Discussion

**Setup:** 4 people reading the same book at different paces

**Test:**
1. User A (page 50) posts: "Just started, excited!"
2. User B (page 100) posts: "Getting interesting at chapter 5"
3. User C (page 150) posts: "The twist in chapter 8!"
4. User D (page 200) posts: "Almost done, what an ending!"

**Expected Results:**
- User A (page 50) sees only: User A's comment
- User B (page 100) sees: User A and User B's comments
- User C (page 150) sees: User A, B, and C's comments
- User D (page 200) sees: All comments

**Verify:** Use browser dev tools to check API responses

### Scenario 5: Edition Differences

**Setup:** Same book, different editions

**Test:**
1. User A has 300-page paperback edition
2. User B has 450-page hardcover edition
3. Both are at 50% progress
4. User A is at page 150
5. User B is at page 225
6. Both post comments at 50%
7. Both should see each other's comments (percentage-based matching)

**Expected:** Comments sync correctly across editions

## API Testing

### Using the Auto-Generated API Docs

1. Start backend: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. You'll see Swagger UI with all endpoints

### Key Endpoints to Test

#### Authentication
```
POST /auth/google
Body: {"token": "google-oauth-token"}
Response: {"access_token": "jwt-token", "token_type": "bearer"}
```

#### Get Current User
```
GET /auth/me
Headers: Authorization: Bearer {jwt-token}
Response: {"id": "uuid", "name": "John", "email": "john@example.com"}
```

#### Create Group
```
POST /groups
Headers: Authorization: Bearer {jwt-token}
Body: {"name": "My Book Club", "description": "Friends reading together"}
Response: {"id": "uuid", "name": "My Book Club", "invite_code": "ABC123XYZ"}
```

#### Join Group
```
POST /groups/join
Headers: Authorization: Bearer {jwt-token}
Body: {"invite_code": "ABC123XYZ"}
Response: {"message": "Successfully joined group"}
```

#### Search Books
```
GET /books/search?q=Harry+Potter
Response: [{"title": "Harry Potter", "author": "J.K. Rowling", "isbn": "..."}]
```

#### Add Book to Group
```
POST /groups/{group_id}/books
Headers: Authorization: Bearer {jwt-token}
Body: {"title": "Harry Potter", "author": "J.K. Rowling", "isbn": "..."}
Response: {"id": "uuid", "title": "Harry Potter"}
```

#### Update Progress
```
PUT /progress/{group_id}/{book_id}
Headers: Authorization: Bearer {jwt-token}
Body: {"current_page": 50, "total_pages": 300}
Response: {"current_page": 50, "total_pages": 300, "progress_percentage": 16.67}
```

#### Post Comment
```
POST /groups/{group_id}/books/{book_id}/comments
Headers: Authorization: Bearer {jwt-token}
Body: {
  "content": "Great chapter!",
  "progress_page": 50,
  "progress_total_pages": 300
}
Response: {"id": "uuid", "content": "Great chapter!", "progress_percentage": 16.67}
```

#### Get Comments (Filtered by Progress)
```
GET /groups/{group_id}/books/{book_id}/comments
Headers: Authorization: Bearer {jwt-token}
Response: [
  {
    "id": "uuid",
    "content": "Great chapter!",
    "progress_percentage": 16.67,
    "user": {"name": "John", "avatar_url": "..."},
    "like_count": 5,
    "created_at": "2025-12-09T10:00:00Z"
  }
]
```

## Performance Testing

### Load Test with Your Book Club

1. **Concurrent Users:** Have 5+ people use the app simultaneously
2. **Comment Flood:** Everyone posts 3-4 comments quickly
3. **Progress Updates:** Everyone updates progress multiple times
4. **Observe:**
   - Page load times (should be < 2 seconds)
   - Comment posting speed (should be instant)
   - No errors or crashes

### Expected Performance
- **Backend Response Time:** < 200ms for most endpoints
- **Frontend Load Time:** < 1 second
- **Comment Visibility Filter:** < 100ms
- **Book Search:** < 1 second (depends on Open Library API)

## Bug Testing

### Common Issues to Check

1. **Off-by-one errors in progress:**
   - User at exactly 50% should see comments at 47% (with 3% buffer)
   - Not 46.9% or 47.1%

2. **Race conditions:**
   - Two users posting comments simultaneously
   - User updating progress while viewing comments

3. **Edge cases:**
   - User at 0% progress (should see no comments)
   - User at 100% progress (should see all comments)
   - Empty comment content (should be rejected)
   - 1001 character comment (should be rejected)

4. **Group limits:**
   - Try adding 33rd member (should fail)
   - Non-admin trying to add book (should fail)

5. **Invalid data:**
   - Negative page numbers
   - Current page > total pages
   - Invalid invite code
   - Expired JWT token

## Database Testing

### Check Data Integrity

```sql
-- Connect to database
psql -U postgres -d bookclub

-- Check user count
SELECT COUNT(*) FROM users;

-- Check groups and members
SELECT g.name, COUNT(gm.id) as member_count
FROM groups g
LEFT JOIN group_members gm ON g.id = gm.group_id
GROUP BY g.id, g.name;

-- Check comments with progress
SELECT c.content, c.progress_percentage, u.name
FROM comments c
JOIN users u ON c.user_id = u.id
ORDER BY c.created_at DESC
LIMIT 10;

-- Verify progress calculations
SELECT
    u.name,
    urp.current_page,
    urp.total_pages,
    urp.progress_percentage,
    ROUND((urp.current_page::DECIMAL / urp.total_pages::DECIMAL) * 100, 2) as calculated
FROM user_reading_progress urp
JOIN users u ON urp.user_id = u.id;
```

## Security Testing

### Authentication Tests

1. **Without Token:**
   ```bash
   curl http://localhost:8000/auth/me
   # Expected: 401 Unauthorized
   ```

2. **With Invalid Token:**
   ```bash
   curl -H "Authorization: Bearer invalid-token" http://localhost:8000/auth/me
   # Expected: 401 Unauthorized
   ```

3. **With Valid Token:**
   ```bash
   curl -H "Authorization: Bearer {your-jwt-token}" http://localhost:8000/auth/me
   # Expected: 200 OK with user data
   ```

### Authorization Tests

1. **Non-member accessing group:**
   - User A creates group
   - User B (not member) tries to access
   - Expected: 403 Forbidden

2. **Non-admin adding book:**
   - User B (member, not admin) tries to add book
   - Expected: 403 Forbidden

## Browser Testing

Test on multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if Mac available)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

## Regression Testing

After any code changes, re-run:
1. Authentication flow
2. Create and join group
3. Add book
4. Post comment
5. Verify comment visibility

## Reporting Issues

When you find a bug, document:
1. **What you were doing:** Step-by-step actions
2. **What happened:** Actual behavior
3. **What you expected:** Expected behavior
4. **Browser/Device:** Chrome on Windows, iPhone Safari, etc.
5. **Screenshots:** If applicable
6. **Console errors:** Open browser dev tools → Console tab

## Success Criteria

MVP is ready for beta when:
- ✅ All Quick Test Checklist items pass
- ✅ Spoiler protection works 100% correctly
- ✅ No critical bugs
- ✅ All 4 detailed scenarios work
- ✅ Performance is acceptable (< 2 sec load times)
- ✅ Works on mobile browsers
- ✅ Your book club can use it without confusion

---

**Happy Testing! 📚**

Report any issues and we'll fix them together.
