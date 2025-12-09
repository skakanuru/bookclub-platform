# BookClub Platform - Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - DATABASE_URL (PostgreSQL connection string)
# - GOOGLE_CLIENT_ID (from Google Cloud Console)
# - GOOGLE_CLIENT_SECRET (from Google Cloud Console)
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - FRONTEND_URL (your frontend URL)
```

### 3. Setup Database
```bash
# Create PostgreSQL database
createdb bookclub

# Run migrations
alembic upgrade head
```

### 4. Run the Server
```bash
# Development mode (with auto-reload)
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload
```

### 5. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Google OAuth Setup

### 1. Create OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Configure consent screen
6. Create OAuth client ID (Web application)
7. Add authorized redirect URIs:
   - `http://localhost:5173` (for local frontend)
   - Your production frontend URL

### 2. Copy Credentials to .env
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret-here
```

---

## Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Authenticate with Google
From your frontend, get a Google ID token, then:
```bash
curl -X POST http://localhost:8000/auth/google \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_GOOGLE_ID_TOKEN"}'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "name": "John Doe",
    "email": "john@example.com",
    ...
  }
}
```

### 3. Use JWT Token
```bash
# Save token
export TOKEN="your-jwt-token-here"

# Get current user
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer $TOKEN"

# Create a group
curl -X POST http://localhost:8000/groups \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Book Club", "description": "Reading sci-fi novels"}'

# Search books
curl "http://localhost:8000/books/search?q=dune&limit=5" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Common Operations

### Create a Group
```python
POST /groups
{
  "name": "Sci-Fi Book Club",
  "description": "Monthly sci-fi book discussions"
}
# Returns: Group with invite_code
```

### Join a Group
```python
POST /groups/join
{
  "invite_code": "ABCD1234EFGH"
}
```

### Add a Book to Group
```python
POST /books/groups/{group_id}/books
{
  "title": "Dune",
  "author": "Frank Herbert",
  "isbn": "9780441172719",
  "cover_url": "https://..."
}
```

### Update Reading Progress
```python
POST /progress
{
  "book_id": "uuid",
  "group_id": "uuid",
  "current_page": 150,
  "total_pages": 500
}
# Progress: 30%
```

### Create a Comment
```python
POST /comments/groups/{group_id}/comments
{
  "book_id": "uuid",
  "content": "The spice must flow! Loving this book so far.",
  "progress_page": 150,
  "progress_total_pages": 500
}
# Comment at 30% progress
```

### View Comments (with Visibility)
```python
GET /comments/groups/{group_id}/books/{book_id}/comments
# Only returns comments where:
# comment.progress_percentage <= user.progress_percentage - 3.0
```

---

## Key Features to Test

### 1. Comment Visibility System
```
Scenario:
- User A at page 200/400 (50% progress)
- User B creates comment at page 100/400 (25% progress)
- User C creates comment at page 190/400 (47.5% progress)

User A can see:
- User B's comment (25% < 47%)  ✓
- User C's comment (47.5% > 47%) ✗

When User A reaches page 210/400 (52.5%):
- Can now see User C's comment (47.5% < 49.5%) ✓
```

### 2. Group Member Limit
```
- Create a group
- Add 32 members (should succeed)
- Try to add 33rd member (should fail with error)
```

### 3. Admin Permissions
```
- Create group (you become admin)
- Add member
- Try to update group as member (should fail)
- Try to update group as admin (should succeed)
- Promote member to admin
- Try to leave as last admin (should fail)
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct
```

### Google OAuth Error
```
Error: Invalid token audience
Solution: Check GOOGLE_CLIENT_ID matches the token's audience
```

### Import Errors
```
Error: ModuleNotFoundError
Solution: Ensure you're in the backend directory and installed requirements
```

### JWT Token Expired
```
Error: 401 Unauthorized
Solution: Get a new token via /auth/google or /auth/refresh
```

---

## Development Workflow

### 1. Make Changes
Edit files in `app/` directory

### 2. Auto-Reload
Server automatically reloads when files change (in dev mode)

### 3. Test Changes
Use Swagger UI at http://localhost:8000/docs

### 4. Database Changes
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

---

## Production Deployment

### 1. Environment Variables
```env
ENVIRONMENT=production
DATABASE_URL=postgresql://...  # Production database
FRONTEND_URL=https://yourdomain.com
```

### 2. Disable API Docs
API docs are automatically disabled in production (ENVIRONMENT=production)

### 3. Run with Production Server
```bash
# Using gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Use HTTPS
Ensure your production deployment uses HTTPS for secure token transmission

---

## API Endpoint Summary

**Authentication**
- `POST /auth/google` - Login with Google
- `GET /auth/me` - Get current user
- `POST /auth/refresh` - Refresh token

**Users**
- `GET /users/me` - Get profile
- `PUT /users/me` - Update profile

**Groups**
- `POST /groups` - Create group
- `GET /groups` - List my groups
- `POST /groups/join` - Join via code
- `GET /groups/{id}` - Get group details
- `PUT /groups/{id}` - Update group
- `DELETE /groups/{id}` - Delete group

**Books**
- `GET /books/search` - Search books
- `POST /books/groups/{id}/books` - Add book
- `GET /books/groups/{id}/books` - List books

**Comments**
- `POST /comments/groups/{id}/comments` - Create
- `GET /comments/groups/{gid}/books/{bid}/comments` - List (with visibility)
- `PUT /comments/comments/{id}` - Update
- `DELETE /comments/comments/{id}` - Delete
- `POST /comments/comments/{id}/like` - Like
- `DELETE /comments/comments/{id}/like` - Unlike

**Progress**
- `POST /progress` - Create/Update
- `GET /progress` - List my progress
- `GET /progress/groups/{gid}/books/{bid}` - Get specific
- `PUT /progress/{id}` - Update
- `DELETE /progress/{id}` - Delete

---

## Support

- **API Documentation**: http://localhost:8000/docs
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Full API Reference**: See `API_DOCUMENTATION.md`

---

**You're all set! Start the server and begin testing. 🚀**
