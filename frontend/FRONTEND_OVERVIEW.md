# BookClub Frontend - Complete Overview

## Project Summary

A production-ready React frontend for the BookClub platform that enables spoiler-free book discussions. Built with modern web technologies and following best practices for performance, accessibility, and user experience.

## Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────┐
│                   React 18.3.1                  │
│            (UI Library & Components)            │
├─────────────────────────────────────────────────┤
│  Vite 5.4      │  React Router 6  │ TailwindCSS │
│  (Build Tool)  │  (Routing)       │  (Styling)  │
├─────────────────────────────────────────────────┤
│  TanStack Query │  Axios          │  Zustand    │
│  (Data Fetch)   │  (HTTP Client)  │  (State)    │
├─────────────────────────────────────────────────┤
│  Google OAuth   │  date-fns       │  Lucide     │
│  (Auth)         │  (Dates)        │  (Icons)    │
└─────────────────────────────────────────────────┘
```

### Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── GoogleLoginButton.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── books/
│   │   │   ├── BookCard.jsx
│   │   │   ├── BookCover.jsx
│   │   │   └── BookSearch.jsx
│   │   ├── comments/
│   │   │   ├── AheadNotifications.jsx
│   │   │   ├── CommentCard.jsx
│   │   │   ├── CommentFeed.jsx
│   │   │   └── CommentInput.jsx
│   │   ├── common/
│   │   │   ├── Avatar.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── Modal.jsx
│   │   ├── groups/
│   │   │   ├── CreateGroupModal.jsx
│   │   │   ├── GroupCard.jsx
│   │   │   ├── GroupHeader.jsx
│   │   │   └── InviteCodeDisplay.jsx
│   │   └── progress/
│   │       ├── ProgressIndicator.jsx
│   │       └── UpdateProgressModal.jsx
│   ├── contexts/
│   │   └── AuthContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useComments.js
│   │   ├── useGroups.js
│   │   └── useProgress.js
│   ├── pages/
│   │   ├── BookDiscussionPage.jsx
│   │   ├── GroupDetailPage.jsx
│   │   ├── GroupsPage.jsx
│   │   ├── HomePage.jsx
│   │   ├── JoinGroupPage.jsx
│   │   └── LoginPage.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── bookService.js
│   │   ├── commentService.js
│   │   ├── groupService.js
│   │   └── progressService.js
│   ├── styles/
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── eslint.config.js
├── .env.example
├── .gitignore
├── README.md
├── SETUP.md
└── FRONTEND_OVERVIEW.md
```

## Core Features

### 1. Authentication (Google OAuth)

**Components:**
- `GoogleLoginButton` - Handles OAuth flow
- `ProtectedRoute` - Guards authenticated routes

**Flow:**
1. User clicks "Sign in with Google"
2. Google OAuth popup opens
3. User authenticates
4. Credential sent to backend
5. Backend returns JWT token
6. Token stored in localStorage
7. User redirected to dashboard

**Files:**
- `src/components/auth/GoogleLoginButton.jsx`
- `src/components/auth/ProtectedRoute.jsx`
- `src/contexts/AuthContext.jsx`
- `src/services/authService.js`

### 2. Group Management

**Features:**
- Create new groups
- View all user's groups
- Join via invite code
- Share invite links
- Admin controls

**Components:**
- `GroupCard` - Group preview card
- `GroupHeader` - Group page header with invite
- `CreateGroupModal` - Group creation form
- `InviteCodeDisplay` - Shareable invite widget

**User Flows:**

**Creating a Group:**
```
GroupsPage → Click "Create Group" → Fill form → Submit
→ Group created → Navigate to group detail
```

**Joining a Group:**
```
Receive invite link → Click link → JoinGroupPage
→ Login (if needed) → Auto-join → Navigate to group
```

**Files:**
- `src/components/groups/*.jsx`
- `src/pages/GroupsPage.jsx`
- `src/pages/GroupDetailPage.jsx`
- `src/pages/JoinGroupPage.jsx`
- `src/services/groupService.js`
- `src/hooks/useGroups.js`

### 3. Book Management

**Features:**
- Search books via Open Library API
- Add books to groups (admin only)
- View book details
- Display book covers

**Components:**
- `BookCard` - Book display with progress
- `BookCover` - Cover image with fallback
- `BookSearch` - Search interface

**Files:**
- `src/components/books/*.jsx`
- `src/services/bookService.js`

### 4. Reading Progress

**Features:**
- Set current page & total pages
- Automatic percentage calculation
- Different editions support
- Visual progress indicators
- 3% buffer zone calculation

**Components:**
- `ProgressIndicator` - Visual progress (bar + ring)
- `UpdateProgressModal` - Update progress form

**Progress Calculation:**
```javascript
percentage = (current_page / total_pages) * 100
visible_threshold = user_percentage - 3%
```

**Files:**
- `src/components/progress/*.jsx`
- `src/services/progressService.js`
- `src/hooks/useProgress.js`

### 5. Comment System

**Features:**
- Post comments at current progress
- View comments filtered by progress
- Like/unlike comments
- Report spoilers
- See count of comments ahead

**Components:**
- `CommentCard` - Individual comment
- `CommentFeed` - List of comments
- `CommentInput` - Create comment form
- `AheadNotifications` - Show hidden comments

**Comment Visibility Logic:**
```javascript
// User at 50%, total 300 pages
currentPage = 150
totalPages = 300
percentage = 50%

// 3% buffer
bufferPercentage = 3%
visibleThreshold = 50% - 3% = 47%

// User sees comments from:
// - Page 0 to ~141 (47% of 300)
// - All comments at ≤47% progress
```

**Files:**
- `src/components/comments/*.jsx`
- `src/services/commentService.js`
- `src/hooks/useComments.js`

### 6. Notifications

**Features:**
- Count of comments ahead
- List of ahead commenters
- Progress indicators
- Motivation to keep reading

**Component:**
- `AheadNotifications` - Badge + modal

**Files:**
- `src/components/comments/AheadNotifications.jsx`

## Design System

### Color Palette

```css
Primary:    #2C5F4F (Deep Sage Green)
Background: #FAF9F6 (Warm Off-White)
Accent:     #C7956D (Book Leather Tan)
Danger:     #C85A54 (Muted Red)
Success:    #5A8C6F (Forest Green)
```

### Typography

```css
Headings:   Merriweather (Serif)
Body:       Inter (Sans-serif)
Code:       JetBrains Mono (Monospace)
```

### Component Variants

**Button:**
- Primary (sage green)
- Secondary (tan)
- Outline (bordered)
- Ghost (transparent)
- Danger (red)

**Sizes:**
- sm: Small buttons/text
- md: Default size
- lg: Large emphasis

**Card:**
- Default: White background, subtle border
- Hover: Elevated shadow on hover

## State Management

### React Query (TanStack Query)

**Cache Keys:**
```javascript
['groups']                    // User's groups
['group', groupId]           // Single group
['groupBooks', groupId]      // Books in group
['book', bookId]             // Single book
['progress', groupId, bookId] // User's progress
['comments', groupId, bookId] // Visible comments
['commentsAhead', groupId, bookId] // Comments ahead
```

**Refetch Strategy:**
- Comments: Auto-refetch every 30 seconds
- Progress: Refetch on update
- Groups: Manual invalidation

### Auth Context (React Context)

```javascript
{
  user: User | null,
  isLoading: boolean,
  isAuthenticated: boolean,
  login: (credential) => Promise<void>,
  logout: () => Promise<void>
}
```

### Local Storage

```
accessToken: JWT token
user: Serialized user object
```

## API Integration

### API Service (`api.js`)

**Features:**
- Base Axios instance
- Request interceptor (adds auth token)
- Response interceptor (handles 401 errors)
- Automatic token refresh on 401

**Configuration:**
```javascript
baseURL: process.env.VITE_API_URL
headers: { 'Content-Type': 'application/json' }
withCredentials: true
```

### Service Layer

**Pattern:**
```javascript
// service/exampleService.js
export const exampleService = {
  async getItems() {
    const response = await api.get('/items')
    return response.data
  },
  async createItem(data) {
    const response = await api.post('/items', data)
    return response.data
  }
}
```

**Services:**
- `authService` - Authentication
- `groupService` - Group CRUD
- `bookService` - Book search/management
- `commentService` - Comment operations
- `progressService` - Progress tracking

## Custom Hooks

### useAuth

```javascript
const { user, isAuthenticated, login, logout } = useAuth()
```

### useGroups

```javascript
const {
  groups,
  isLoading,
  createGroup,
  joinGroup,
  isCreating,
  isJoining
} = useGroups()
```

### useGroup (single)

```javascript
const { group, isLoading } = useGroup(groupId)
```

### useComments

```javascript
const {
  comments,
  commentsAhead,
  isLoading,
  createComment,
  likeComment,
  reportComment,
  isCreatingComment
} = useComments(groupId, bookId)
```

### useProgress

```javascript
const {
  progress,
  isLoading,
  updateProgress,
  isUpdating
} = useProgress(groupId, bookId)
```

## Routing

### Route Structure

```
/                           → HomePage (public/redirects if authed)
/login                      → LoginPage (public)
/join/:inviteCode           → JoinGroupPage (public, auto-join if authed)
/groups                     → GroupsPage (protected)
/groups/:groupId            → GroupDetailPage (protected)
/groups/:groupId/books/:bookId → BookDiscussionPage (protected)
```

### Protected Routes

Wrapped in `ProtectedRoute` component:
- Checks authentication
- Redirects to `/login` if not authenticated
- Preserves intended destination in location state

## User Flows

### 1. New User Journey

```
1. Click invite link (/join/ABC123)
2. JoinGroupPage → Not authenticated → Show login
3. Click "Sign in with Google"
4. Google OAuth → Success
5. Auto-join group
6. Redirect to /groups/{groupId}
7. See group with book(s)
8. Click book → BookDiscussionPage
9. Prompt to set progress
10. Set progress → See comments
```

### 2. Existing User - Create Group

```
1. Login → /groups
2. Click "Create Group"
3. Fill form (name, description)
4. Submit → Group created
5. Redirect to /groups/{groupId}
6. Click "Add Book" (admin only)
7. Search for book
8. Select book → Added to group
9. Click book → Set progress
10. Start commenting
```

### 3. Posting a Comment

```
1. On BookDiscussionPage
2. User has progress set (e.g., page 150/300)
3. Scroll to CommentInput
4. Type comment
5. See indicator: "Commenting at Page 150 (50%)"
6. Click "Post Comment"
7. Comment appears in feed
8. Other users see it (if they're at ≥47%)
9. Users behind 47% see "+1 comment ahead"
```

### 4. Updating Progress

```
1. On BookDiscussionPage
2. Click "Update" next to progress
3. Modal opens
4. Enter current page & total pages
5. See live percentage calculation
6. See buffer zone preview
7. Click "Update Progress"
8. Progress saved
9. Comment feed refreshes
10. May see new comments
11. "Comments ahead" count updates
```

## Performance Optimizations

### Code Splitting

- Route-based splitting (automatic with React Router)
- Lazy loading of large components
- Dynamic imports for modals

### Caching

- TanStack Query cache (5 min stale time)
- localStorage for auth state
- Optimistic updates for likes

### Image Optimization

- Lazy loading book covers
- Placeholder for missing images
- Optimized image sizes

### Bundle Size

- Tree-shaking unused code
- Minification in production
- Gzip compression

## Error Handling

### API Errors

```javascript
try {
  await api.get('/endpoint')
} catch (error) {
  if (error.response) {
    // Server responded with error
    toast.error(error.response.data.detail)
  } else if (error.request) {
    // No response received
    toast.error('Network error. Please try again.')
  } else {
    // Request setup error
    toast.error('Something went wrong.')
  }
}
```

### Form Validation

- Client-side validation before submission
- Display error messages inline
- Prevent submission if invalid

### Loading States

- Skeleton loaders for data fetching
- Spinner for mutations
- Disabled buttons during submission

## Responsive Design

### Breakpoints

```css
sm:  640px   /* Small tablets */
md:  768px   /* Tablets */
lg:  1024px  /* Laptops */
xl:  1280px  /* Desktops */
```

### Mobile Optimizations

- Touch-friendly targets (44x44px minimum)
- Collapsible navigation
- Stacked layouts on small screens
- Bottom sheet modals on mobile
- Larger fonts on mobile

## Accessibility

### Features

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Focus indicators
- Alt text for images
- Color contrast (WCAG AA)

### Best Practices

- Headings hierarchy (h1 → h2 → h3)
- Form labels associated with inputs
- Error messages announced
- Loading states communicated

## Security

### Authentication

- JWT tokens in localStorage
- HTTP-only cookies (if supported by backend)
- Token refresh on 401
- Automatic logout on invalid token

### Input Sanitization

- All inputs escaped
- No innerHTML (use textContent)
- XSS protection

### CORS

- Backend CORS configured for frontend domain
- Credentials included in requests

## Testing Strategy

### Unit Tests (Recommended)

```bash
# Install testing libraries
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

**Test Components:**
- Button variants and states
- Form validation
- Comment visibility logic
- Progress calculation

### Integration Tests

- User authentication flow
- Create and join group
- Post and view comments
- Update progress and see new comments

### E2E Tests (Playwright)

```bash
npm install -D @playwright/test
```

**Critical Paths:**
1. Sign up → Join group → Set progress → Comment
2. Create group → Add book → Invite member
3. Comment visibility based on progress

## Deployment

### Environment Variables

**Development:**
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=dev_client_id
```

**Production:**
```env
VITE_API_URL=https://api.bookclub.com
VITE_GOOGLE_CLIENT_ID=prod_client_id
```

### Build Process

```bash
npm run build
```

**Output:** `dist/` directory with optimized static files

### Deployment Platforms

**Vercel (Recommended):**
1. Connect GitHub repo
2. Auto-deploy on push to main
3. Set environment variables
4. Custom domain support

**Netlify:**
1. Build command: `npm run build`
2. Publish directory: `dist`
3. Environment variables
4. Deploy

**Railway:**
1. Connect repo
2. Select frontend service
3. Auto-detect Vite config
4. Deploy

## Monitoring & Analytics

### Error Tracking (Future)

- Sentry for error monitoring
- LogRocket for session replay
- Analytics for user behavior

### Performance Monitoring

- Web Vitals tracking
- Lighthouse CI
- Bundle size monitoring

## Future Enhancements

### Phase 2

- [ ] Push notifications for new comments
- [ ] Multiple books per group
- [ ] Friend system
- [ ] Private messages
- [ ] Reading schedules

### Phase 3

- [ ] React Native mobile apps
- [ ] Offline support (PWA)
- [ ] Voice comments
- [ ] Chapter-based progress
- [ ] Book recommendations

### Phase 4

- [ ] Video discussions
- [ ] Live reading sessions
- [ ] Author Q&A integration
- [ ] Reading statistics
- [ ] Gamification (badges, streaks)

## Maintenance

### Dependencies

**Update regularly:**
```bash
npm update
npm audit fix
```

**Check for outdated:**
```bash
npm outdated
```

### Code Quality

```bash
# Run linter
npm run lint

# Format code (if Prettier added)
npm run format
```

### Performance Checks

```bash
# Build and analyze
npm run build
npx vite-bundle-visualizer
```

## Support & Resources

### Documentation

- React: https://react.dev
- Vite: https://vitejs.dev
- TanStack Query: https://tanstack.com/query
- TailwindCSS: https://tailwindcss.com
- React Router: https://reactrouter.com

### Community

- GitHub Issues for bug reports
- Discussions for feature requests
- Stack Overflow for questions

## Conclusion

This frontend is production-ready with:
- ✅ Modern tech stack
- ✅ Clean architecture
- ✅ Responsive design
- ✅ Error handling
- ✅ Performance optimizations
- ✅ Comprehensive documentation

Ready to deploy and scale!
