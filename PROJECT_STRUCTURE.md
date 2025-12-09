# BookClub Platform - Project Structure

## Directory Structure

```
bookclub-platform/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── group.py
│   │   │   ├── book.py
│   │   │   ├── comment.py
│   │   │   └── progress.py
│   │   ├── schemas/           # Pydantic schemas (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── group.py
│   │   │   ├── book.py
│   │   │   ├── comment.py
│   │   │   └── progress.py
│   │   ├── routers/           # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── groups.py
│   │   │   ├── books.py
│   │   │   ├── comments.py
│   │   │   └── progress.py
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── book_service.py
│   │   │   ├── comment_service.py
│   │   │   └── progress_service.py
│   │   ├── utils/             # Helper functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── invite_code.py
│   │   └── middleware/        # Custom middleware
│   │       ├── __init__.py
│   │       └── auth_middleware.py
│   ├── alembic/               # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/                 # Backend tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_groups.py
│   │   ├── test_comments.py
│   │   └── test_progress.py
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── alembic.ini           # Alembic configuration
│
├── frontend/                  # React web app
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/           # Images, fonts
│   │   │   └── fonts/
│   │   ├── components/       # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   └── Avatar.jsx
│   │   │   ├── auth/
│   │   │   │   └── GoogleLoginButton.jsx
│   │   │   ├── groups/
│   │   │   │   ├── GroupCard.jsx
│   │   │   │   ├── GroupHeader.jsx
│   │   │   │   ├── CreateGroupModal.jsx
│   │   │   │   └── InviteCodeDisplay.jsx
│   │   │   ├── books/
│   │   │   │   ├── BookCard.jsx
│   │   │   │   ├── BookSearch.jsx
│   │   │   │   └── BookCover.jsx
│   │   │   ├── comments/
│   │   │   │   ├── CommentCard.jsx
│   │   │   │   ├── CommentFeed.jsx
│   │   │   │   ├── CommentInput.jsx
│   │   │   │   └── AheadNotifications.jsx
│   │   │   └── progress/
│   │   │       ├── ProgressIndicator.jsx
│   │   │       ├── ProgressBar.jsx
│   │   │       └── UpdateProgressModal.jsx
│   │   ├── pages/            # Page components
│   │   │   ├── HomePage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── GroupsPage.jsx
│   │   │   ├── GroupDetailPage.jsx
│   │   │   ├── BookDiscussionPage.jsx
│   │   │   ├── JoinGroupPage.jsx
│   │   │   └── ProfilePage.jsx
│   │   ├── hooks/            # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useGroups.js
│   │   │   ├── useComments.js
│   │   │   └── useProgress.js
│   │   ├── contexts/         # React contexts
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── services/         # API service layer
│   │   │   ├── api.js        # Axios instance
│   │   │   ├── authService.js
│   │   │   ├── groupService.js
│   │   │   ├── bookService.js
│   │   │   ├── commentService.js
│   │   │   └── progressService.js
│   │   ├── utils/            # Utility functions
│   │   │   ├── formatters.js
│   │   │   ├── validators.js
│   │   │   └── constants.js
│   │   ├── styles/           # Global styles
│   │   │   ├── index.css
│   │   │   ├── variables.css
│   │   │   └── typography.css
│   │   ├── App.jsx           # Root component
│   │   ├── main.jsx          # Entry point
│   │   └── router.jsx        # React Router setup
│   ├── package.json
│   ├── vite.config.js        # Vite configuration
│   ├── .env.example
│   └── .eslintrc.js
│
├── docs/                      # Documentation
│   ├── API.md                # API documentation
│   ├── SETUP.md              # Setup instructions
│   └── DEPLOYMENT.md         # Deployment guide
│
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
│
├── docker-compose.yml        # Local development with Docker
├── .gitignore
└── README.md
```

## Technology Stack Details

### Backend Dependencies (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.1
google-auth==2.23.4
google-auth-oauthlib==1.1.0
pydantic==2.5.0
pydantic-settings==2.1.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Frontend Dependencies (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.8.4",
    "axios": "^1.6.2",
    "@react-oauth/google": "^0.12.1",
    "zustand": "^4.4.7",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0",
    "react-hot-toast": "^2.4.1",
    "framer-motion": "^10.16.5",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bookclub

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# JWT
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# CORS
FRONTEND_URL=http://localhost:5173

# Open Library API
OPEN_LIBRARY_API_URL=https://openlibrary.org

# Environment
ENVIRONMENT=development  # development, staging, production
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

## Development Workflow

### Initial Setup

1. **Clone Repository**
   ```bash
   git clone <repo-url>
   cd bookclub-platform
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Database Setup**
   ```bash
   # Install PostgreSQL locally or use Docker
   docker run --name bookclub-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bookclub -p 5432:5432 -d postgres:15

   # Run migrations
   alembic upgrade head
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your values
   ```

5. **Run Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

### Development Commands

#### Backend
```bash
# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black app/
isort app/

# Lint
flake8 app/
```

#### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Format code
npm run format

# Run tests
npm run test
```

## API Documentation

Once the backend is running, API documentation is automatically available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Management

### Useful PostgreSQL Commands
```bash
# Connect to database
psql -U user -d bookclub

# List tables
\dt

# Describe table
\d table_name

# View data
SELECT * FROM users LIMIT 10;

# Backup database
pg_dump -U user bookclub > backup.sql

# Restore database
psql -U user bookclub < backup.sql
```

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] CORS settings updated for production domain
- [ ] Google OAuth redirect URIs updated
- [ ] Frontend API URL updated
- [ ] SSL certificate configured

### Railway Deployment
1. Connect GitHub repository to Railway
2. Create new project
3. Add PostgreSQL database
4. Deploy backend service
5. Deploy frontend service
6. Configure custom domain
7. Set environment variables
8. Run database migrations

## Monitoring & Maintenance

### Health Checks
- Backend: `GET /health`
- Database: `SELECT 1;`

### Logs
- Backend logs via Railway dashboard
- Frontend errors via browser console
- Database logs via Railway/Render

### Backup Strategy
- Daily automated database backups (Railway/Render)
- Weekly manual backups
- Store backups in separate location

## Security Best Practices

1. **Never commit .env files**
2. **Use environment-specific configurations**
3. **Rotate secrets regularly**
4. **Keep dependencies updated**
5. **Use HTTPS in production**
6. **Implement rate limiting**
7. **Sanitize user inputs**
8. **Use parameterized queries**
9. **Enable CORS only for trusted domains**
10. **Monitor for suspicious activity**

## Git Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches

### Commit Message Format
```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(comments): add comment visibility filtering

- Implement progress-based filtering
- Add 3% buffer zone
- Update tests

Closes #123
```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use Black for formatting
- Use type hints
- Write docstrings for public functions
- Max line length: 100 characters

### JavaScript (Frontend)
- Use ES6+ features
- Use functional components with hooks
- Use meaningful variable names
- Write JSDoc comments for complex functions
- Max line length: 100 characters

## Testing Strategy

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_comments.py

# Run specific test
pytest tests/test_comments.py::test_comment_visibility
```

### Frontend Tests
```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Performance Optimization

### Backend
- Use database indexes on frequently queried columns
- Implement pagination for large result sets
- Cache frequently accessed data
- Use async/await for I/O operations
- Optimize SQL queries

### Frontend
- Code splitting by route
- Lazy load components
- Optimize images (WebP, lazy loading)
- Use React.memo for expensive components
- Debounce search inputs
- Implement virtual scrolling for long lists

## Troubleshooting

### Common Issues

1. **Database connection fails**
   - Check DATABASE_URL in .env
   - Ensure PostgreSQL is running
   - Verify credentials

2. **Google OAuth fails**
   - Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
   - Verify redirect URI in Google Console
   - Ensure cookies are enabled

3. **CORS errors**
   - Check FRONTEND_URL in backend .env
   - Verify CORS middleware configuration
   - Check browser console for details

4. **Comments not filtering correctly**
   - Verify user has set reading progress
   - Check progress percentage calculation
   - Inspect SQL query in logs

## Support & Documentation

- Technical Spec: `TECHNICAL_SPEC.md`
- API Documentation: http://localhost:8000/docs
- Setup Guide: `docs/SETUP.md`
- Deployment Guide: `docs/DEPLOYMENT.md`

---

**Document Version**: 1.0
**Last Updated**: 2025-12-09
