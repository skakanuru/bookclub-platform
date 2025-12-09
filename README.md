# BookClub Platform

A spoiler-free book discussion platform where readers can engage in conversations about books without fear of spoilers. Users only see comments from readers at or behind their current reading progress.

## Key Features

- **Spoiler-Free Discussions**: Comment visibility based on reading progress with 3% buffer zone
- **Reading Groups**: Create and join book clubs with invite links
- **Progress Tracking**: Track reading by page number or percentage
- **Social Features**: Like comments, see who's ahead, and engage with fellow readers
- **Clean Design**: Book-friendly aesthetic with typography-focused interface
- **Google Authentication**: Simple one-click login

## How It Works

1. **Join a Group**: Use an invite link to join a reading group
2. **Set Your Progress**: Enter your edition's page count and current page
3. **Start Discussing**: Post comments and see discussions from readers at your level or behind
4. **Stay Spoiler-Free**: Comments from readers ahead are hidden until you catch up
5. **Get Notified**: See how many comments are waiting as you progress

## Technology Stack

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Authentication**: Google OAuth 2.0
- **Book Data**: Open Library API
- **Hosting**: Railway/Render (under $200/year)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Google OAuth credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd bookclub-platform
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Database setup**
   ```bash
   # Using Docker
   docker run --name bookclub-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bookclub -p 5432:5432 -d postgres:15

   # Run migrations
   alembic upgrade head
   ```

4. **Frontend setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your API URL
   ```

5. **Run development servers**
   ```bash
   # Terminal 1 - Backend (from backend/ directory)
   uvicorn app.main:app --reload --port 8000

   # Terminal 2 - Frontend (from frontend/ directory)
   npm run dev
   ```

6. **Open your browser**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

## Project Structure

```
bookclub-platform/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── models/    # Database models
│   │   ├── routers/   # API endpoints
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── tests/
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   └── public/
└── docs/              # Documentation
```

## Documentation

- [Technical Specification](TECHNICAL_SPEC.md) - Detailed technical design
- [Project Structure](PROJECT_STRUCTURE.md) - Code organization and setup
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)

## Key Design Decisions

### Comment Visibility Algorithm

Comments are filtered based on the user's current reading progress minus a 3% buffer:

```python
visible_threshold = user_progress_percentage - 3.0
visible_comments = comments.filter(progress_percentage <= visible_threshold)
```

**Example**: If you're at 50% progress, you see comments up to 47%.

### Progress Normalization

Different editions are normalized via percentage:

```python
progress_percentage = (current_page / total_pages) × 100
```

Users with different editions can still have synchronized discussions.

### Group-Based Privacy

All comments are group-scoped. You only see comments from:
- Groups you're a member of
- Readers at or behind your progress (minus buffer)

## Design Philosophy

**Typography-Focused**
- Serif fonts for book titles and headings (Merriweather)
- Sans-serif for UI elements (Inter)
- Generous line-height and whitespace

**Calm Color Palette**
- Deep sage green (#2C5F4F)
- Warm off-white background (#FAF9F6)
- Book leather accents (#C7956D)

**Mobile-First**
- Touch-friendly targets (44x44px minimum)
- Responsive breakpoints
- Progressive enhancement

## Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Write/update tests
4. Commit with conventional commits: `feat(scope): description`
5. Push and create pull request

### Code Style

**Python**
- Follow PEP 8
- Use Black for formatting
- Type hints required
- Docstrings for public functions

**JavaScript**
- ESLint + Prettier
- Functional components with hooks
- PropTypes or TypeScript (future)

### Testing

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests
cd frontend
npm run test
```

## Deployment

### Railway Deployment

1. Push code to GitHub
2. Connect repository to Railway
3. Add PostgreSQL database
4. Configure environment variables
5. Deploy backend and frontend services
6. Run migrations: `alembic upgrade head`

### Environment Variables

See `.env.example` files in `backend/` and `frontend/` for required variables.

**Critical Variables**:
- `DATABASE_URL` - PostgreSQL connection string
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth secret
- `SECRET_KEY` - JWT signing key (32+ characters)
- `FRONTEND_URL` - Frontend domain (for CORS)

## Roadmap

### MVP (Current)
- [x] Technical specification
- [ ] Backend implementation
- [ ] Frontend implementation
- [ ] Google OAuth integration
- [ ] Comment visibility logic
- [ ] Progress tracking
- [ ] Group management
- [ ] Deployment

### Phase 2
- [ ] Multiple books per group
- [ ] Friend system
- [ ] Reading schedules
- [ ] Enhanced notifications
- [ ] Chapter-based progress

### Phase 3
- [ ] React Native mobile apps
- [ ] Kindle/Audible integration
- [ ] Push notifications
- [ ] Book recommendations
- [ ] Reading statistics

## FAQ

**Q: What if someone posts a spoiler in an early comment?**
A: Users can report comments with the spoiler button. Reported comments are flagged for review.

**Q: How accurate is the progress matching between editions?**
A: The 3% buffer zone accounts for edition differences. Percentage-based matching works well for most books.

**Q: Can I join multiple groups?**
A: Yes! You can join unlimited groups and track progress separately in each.

**Q: What if I'm re-reading a book?**
A: Reset your progress to 0%, and all comments become visible as you progress again.

**Q: Is my reading data private?**
A: Yes. Only group members see your progress and comments. Nothing is public outside your groups.

**Q: What books are available?**
A: Any book in the Open Library database (millions of books). You can also manually add books.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bookclub-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bookclub-platform/discussions)
- **Email**: support@bookclub.app (when deployed)

## License

MIT License - see [LICENSE](LICENSE) for details

## Acknowledgments

- [Open Library](https://openlibrary.org/) for book data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python framework
- [React](https://react.dev/) for the frontend framework
- Inspired by Goodreads, Notion, and the joy of reading

---

**Built with ❤️ for readers who love discussing books without spoilers**

**Status**: In Development
**Version**: 0.1.0-alpha
**Last Updated**: 2025-12-09
