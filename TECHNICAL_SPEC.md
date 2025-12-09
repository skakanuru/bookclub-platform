# BookClub Platform - Technical Specification

## Executive Summary
A spoiler-free book discussion platform where users can only see comments from readers at or behind their current reading progress.

## Core Features (MVP)

### User Features
- Google OAuth authentication (no native accounts)
- Create and join reading groups via invite links
- Add books to groups (group creator/admin only)
- Track reading progress (page number or percentage)
- Post comments at current progress level
- View comments from readers at ≤ their progress (with 3% buffer)
- See notifications for unread comments ahead
- Like/react to comments
- Report spoilers

### Group Features
- Any user can create a group
- Group creator has admin privileges
- One book per group (for MVP)
- Invite-link based joining
- Public discussion visible to all group members

### Book Features
- Search books via Open Library API
- Manual entry for edition page count
- Automatic percentage conversion across editions
- 3% buffer zone for progress matching

## Technical Architecture

### Stack
- **Frontend**: React (web app, mobile-responsive)
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Authentication**: Google OAuth 2.0
- **Hosting**: Railway or Render (under $200/year budget)
- **Book Data**: Open Library API

### Why This Stack?
- **React Web First**: Faster iteration, easier debugging, can access on any device
- **FastAPI**: Modern Python framework, automatic API docs, async support, type hints
- **PostgreSQL**: Handles complex queries (progress-based filtering), relational data, free tiers available
- **Google OAuth Only**: Simplifies auth, no password management, reliable

## Database Schema

### Tables

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### groups
```sql
CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    invite_code VARCHAR(12) UNIQUE NOT NULL,
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### group_members
```sql
CREATE TABLE group_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- 'admin' or 'member'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, user_id)
);
```

#### books
```sql
CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20),
    open_library_id VARCHAR(50),
    cover_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### group_books
```sql
CREATE TABLE group_books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    added_by UUID REFERENCES users(id) ON DELETE SET NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, book_id)
);
```

#### user_reading_progress
```sql
CREATE TABLE user_reading_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    current_page INTEGER NOT NULL,
    total_pages INTEGER NOT NULL,
    progress_percentage DECIMAL(5,2) GENERATED ALWAYS AS ((current_page::DECIMAL / total_pages::DECIMAL) * 100) STORED,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, book_id, group_id)
);
```

#### comments
```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    progress_page INTEGER NOT NULL,
    progress_total_pages INTEGER NOT NULL,
    progress_percentage DECIMAL(5,2) GENERATED ALWAYS AS ((progress_page::DECIMAL / progress_total_pages::DECIMAL) * 100) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_progress ON comments(book_id, group_id, progress_percentage);
```

#### comment_likes
```sql
CREATE TABLE comment_likes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(comment_id, user_id)
);
```

#### spoiler_reports
```sql
CREATE TABLE spoiler_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    reported_by UUID REFERENCES users(id) ON DELETE CASCADE,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'resolved', 'dismissed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication
- `POST /auth/google` - Google OAuth callback
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout

### Users
- `GET /users/me` - Get current user profile
- `GET /users/{user_id}` - Get user profile (public info only)

### Groups
- `POST /groups` - Create new group
- `GET /groups/{group_id}` - Get group details
- `GET /groups/my-groups` - Get user's groups
- `POST /groups/join` - Join group via invite code
- `DELETE /groups/{group_id}/members/{user_id}` - Remove member (admin only)
- `PUT /groups/{group_id}` - Update group (admin only)

### Books
- `GET /books/search?q={query}` - Search books via Open Library
- `POST /books` - Add book to database
- `GET /books/{book_id}` - Get book details
- `POST /groups/{group_id}/books` - Add book to group (admin only)
- `GET /groups/{group_id}/books` - Get books in group

### Reading Progress
- `GET /progress/{group_id}/{book_id}` - Get user's progress for book in group
- `PUT /progress/{group_id}/{book_id}` - Update reading progress
- `GET /progress/{group_id}/{book_id}/all` - Get all members' progress (for notifications)

### Comments
- `POST /groups/{group_id}/books/{book_id}/comments` - Create comment
- `GET /groups/{group_id}/books/{book_id}/comments` - Get comments (filtered by user's progress)
- `GET /groups/{group_id}/books/{book_id}/comments/ahead` - Get count of unread comments ahead
- `POST /comments/{comment_id}/like` - Like/unlike comment
- `POST /comments/{comment_id}/report` - Report comment for spoilers

### Admin
- `GET /admin/reports` - Get spoiler reports (admin only)
- `PUT /admin/reports/{report_id}` - Update report status (admin only)

## Comment Visibility Logic

```python
# Buffer zone: 3%
BUFFER_PERCENTAGE = 3.0

def get_visible_comments(user_progress_percentage, group_id, book_id):
    """
    User can see comments at or below their progress minus buffer
    If user is at 50%, they see comments up to 47%
    """
    visible_threshold = user_progress_percentage - BUFFER_PERCENTAGE

    query = """
        SELECT c.*, u.name, u.avatar_url,
               COUNT(cl.id) as like_count,
               EXISTS(
                   SELECT 1 FROM comment_likes
                   WHERE comment_id = c.id AND user_id = %s
               ) as user_has_liked
        FROM comments c
        JOIN users u ON c.user_id = u.id
        LEFT JOIN comment_likes cl ON c.id = cl.id
        WHERE c.group_id = %s
          AND c.book_id = %s
          AND c.progress_percentage <= %s
        GROUP BY c.id, u.name, u.avatar_url
        ORDER BY c.created_at ASC
    """

    return execute_query(query, (current_user_id, group_id, book_id, visible_threshold))

def get_ahead_comment_notifications(user_progress_percentage, group_id, book_id):
    """
    Get notifications for comments ahead of user's progress
    """
    visible_threshold = user_progress_percentage - BUFFER_PERCENTAGE

    query = """
        SELECT c.id, u.name, c.progress_percentage, c.progress_page, c.created_at
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.group_id = %s
          AND c.book_id = %s
          AND c.progress_percentage > %s
        ORDER BY c.progress_percentage ASC
    """

    return execute_query(query, (group_id, book_id, visible_threshold))
```

## UI/UX Design Philosophy

### Design Principles
- **Clean & Minimal**: Inspired by Goodreads, Notion, and modern reading apps
- **Typography-focused**: Reading is about words - make text beautiful
- **Calm Colors**: Muted, book-friendly palette (cream, sage, navy, warm grays)
- **Spacious Layout**: Generous whitespace, comfortable line-height
- **Mobile-first**: Touch-friendly targets, readable on small screens

### Color Palette
```css
:root {
  /* Primary Colors */
  --color-primary: #2C5F4F;        /* Deep sage green */
  --color-primary-light: #3A7860;
  --color-primary-dark: #1F4538;

  /* Neutral Colors */
  --color-background: #FAF9F6;      /* Warm off-white (book page) */
  --color-surface: #FFFFFF;
  --color-border: #E8E6E1;

  /* Text Colors */
  --color-text-primary: #2B2B2B;
  --color-text-secondary: #6B6B6B;
  --color-text-tertiary: #9B9B9B;

  /* Accent Colors */
  --color-accent: #C7956D;          /* Warm tan (book leather) */
  --color-danger: #C85A54;
  --color-success: #5A8C6F;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
}
```

### Typography
```css
/* Font Stack */
--font-serif: 'Merriweather', 'Georgia', serif;      /* For headings, book titles */
--font-sans: 'Inter', 'system-ui', sans-serif;       /* For UI, body text */
--font-mono: 'JetBrains Mono', 'Courier', monospace; /* For progress indicators */

/* Type Scale */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 2rem;      /* 32px */
```

### Key UI Components

#### Book Card
- Large cover image
- Title in serif font
- Author in secondary text
- Progress bar (thin, elegant)
- Last updated timestamp

#### Comment Card
- User avatar (small, circular)
- Name + timestamp
- Progress indicator badge (e.g., "Page 127 · 42%")
- Comment text (serif font, good line-height)
- Like count + button
- Report button (subtle, bottom-right)

#### Progress Indicator
- Clean circular progress ring OR horizontal bar
- Page number / total pages
- Percentage
- "Update Progress" button (prominent but not aggressive)

#### Group Header
- Group name (large serif heading)
- Member count
- Book cover (medium size)
- Invite code (copy button)

## User Flows

### Flow 1: New User Joins Group
1. User clicks invite link: `bookclub.app/join/ABC123XYZ`
2. Not logged in → Redirect to Google OAuth
3. After auth → Create account → Auto-join group
4. Land on group page → See book, see "Set your progress to start reading"
5. User enters total pages of their edition + current page
6. User can now see comments up to their progress - 3%

### Flow 2: Posting a Comment
1. User on group book page
2. Scrolls to "Add Comment" section (always visible at bottom)
3. Text area + current progress shown (e.g., "Commenting at Page 45 (15%)")
4. Option to update progress before commenting
5. Click "Post" → Comment appears immediately in feed
6. Other users' "unread ahead" counter updates

### Flow 3: Viewing Ahead Notifications
1. User sees badge: "12 comments ahead"
2. Clicks badge → Modal/section opens
3. List shows:
   - "Sarah commented at Page 127 (42%)"
   - "John commented at Page 135 (45%)"
   - etc.
4. No content shown, just who + where
5. Motivates user to keep reading

## Mobile Responsiveness

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Mobile Optimizations
- Bottom tab navigation (Groups, Profile)
- Swipe gestures for navigation
- Sticky "Add Comment" button (floating action button)
- Collapsible progress indicator
- Touch-friendly like buttons (min 44x44px)

## Hosting & Deployment

### Cost Breakdown (Annual)
- **Railway/Render Web Service**: $5/month = $60/year
- **PostgreSQL Database**: $5/month = $60/year
- **Domain**: $12/year (e.g., via Namecheap)
- **SSL**: Free (via Railway/Render)
- **Total**: ~$132/year (well under $200 budget)

### Deployment Strategy
1. Backend on Railway (Python FastAPI)
2. Frontend on Railway Static Sites or Vercel (React build)
3. PostgreSQL on Railway
4. Google OAuth credentials (free)
5. CI/CD via GitHub Actions (free)

## Security Considerations

### Authentication
- Google OAuth only (no password storage)
- JWT tokens for session management
- HTTP-only cookies for token storage
- CORS configured for frontend domain only

### Data Privacy
- Users can only see comments in groups they're members of
- No public profiles or comments
- Email addresses not exposed to other users
- Invite codes are randomly generated (12 chars, URL-safe)

### Input Validation
- Sanitize all user inputs (comment text, group names)
- Rate limiting on comment posting (max 10/minute)
- File upload validation (if avatars added later)

## Testing Strategy

### Backend Tests
- Unit tests for progress calculation logic
- Integration tests for comment visibility queries
- Auth flow tests

### Frontend Tests
- Component tests (React Testing Library)
- E2E tests for critical flows (Playwright)

### Manual Testing Checklist
- [ ] Create group and generate invite code
- [ ] Join group via invite link
- [ ] Add book to group
- [ ] Set reading progress
- [ ] Post comment at different progress levels
- [ ] Verify comment visibility based on progress
- [ ] Like/unlike comments
- [ ] Report spoiler
- [ ] Update progress and see new comments appear

## Future Enhancements (Post-MVP)

### Phase 2
- Multiple books per group
- Friend system
- Kindle/Audible integration
- Chapter-based progress tracking
- Reading schedules/deadlines

### Phase 3
- React Native mobile apps (iOS + Android)
- Push notifications
- Book recommendations
- Author Q&A integration
- Reading statistics/analytics

### Phase 4
- Video/audio comments
- Inline quote discussions
- Book clubs with meeting scheduling
- Integration with local bookstores/libraries

## Development Timeline (Estimate)

### Week 1-2: Backend Foundation
- Database setup
- FastAPI project structure
- Google OAuth integration
- Basic CRUD endpoints

### Week 3-4: Core Features Backend
- Comment visibility logic
- Progress tracking
- Group management
- Book search integration

### Week 5-6: Frontend Foundation
- React project setup
- Component library setup
- Authentication flow
- Routing

### Week 7-8: Core Features Frontend
- Group pages
- Book display
- Comment feed
- Progress tracking UI

### Week 9-10: Polish & Testing
- UI/UX refinements
- Mobile responsiveness
- Bug fixes
- Performance optimization

### Week 11-12: Deployment & Launch
- Production deployment
- Domain setup
- User testing
- Launch!

## Success Metrics

### MVP Success Criteria
- 10+ active users
- 3+ active groups
- 50+ comments posted
- < 1 second page load time
- Zero spoiler complaints (or quick resolution)

### User Satisfaction
- Users report enjoying spoiler-free discussions
- Users invite friends to their groups
- Users return daily/weekly

## Open Questions & Decisions Needed

1. **Group names**: Any restrictions? Max length? Uniqueness?
2. **Comment length**: Character limit? (Suggest 500-1000 chars)
3. **Book cover images**: Store locally or hotlink from Open Library?
4. **Admin panel**: Needed for managing spoiler reports? Or email notifications?
5. **User avatars**: Use Google avatar or allow custom upload?
6. **Group size limits**: Any max members per group?
7. **Beta testing**: Who will be initial testers?

## Next Steps

1. **Review and approve** this technical spec
2. **Answer open questions** above
3. **Set up development environment** (Python, Node, PostgreSQL)
4. **Create GitHub repository**
5. **Start with backend** (database schema + auth)
6. **Then frontend** (authentication + basic routing)
7. **Iterate rapidly** on core features

---

**Document Version**: 1.0
**Last Updated**: 2025-12-09
**Status**: Pending Approval
