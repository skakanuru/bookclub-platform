# BookClub Frontend - Component Tree

Visual guide to understand how components are organized and used.

## Application Structure

```
App.jsx
├── Routes
│   ├── LoginPage
│   ├── JoinGroupPage
│   ├── HomePage (Protected)
│   ├── GroupsPage (Protected)
│   ├── GroupDetailPage (Protected)
│   └── BookDiscussionPage (Protected)
└── Toaster (react-hot-toast)
```

## Page Component Trees

### LoginPage

```
LoginPage
├── BookOpen (icon)
├── GoogleLoginButton
│   └── GoogleLogin (@react-oauth/google)
└── Feature list (static content)
```

### HomePage

```
HomePage
├── Header
│   ├── BookOpen (icon)
│   └── Welcome text
├── Action Cards
│   ├── Card (Your Groups)
│   │   ├── Users (icon)
│   │   └── Button → navigate to /groups
│   └── Card (Create Group)
│       ├── Plus (icon)
│       └── Button → navigate to /groups
└── How It Works (static content)
```

### GroupsPage

```
GroupsPage
├── Header
│   ├── Title
│   ├── Avatar (user)
│   └── Logout Button
├── Content
│   ├── Create Button
│   └── GroupCard[] (map over groups)
│       ├── Users icon + count
│       ├── BookOpen icon + count
│       └── Link to /groups/:id
└── CreateGroupModal
    ├── Modal
    │   ├── Input (name)
    │   ├── Textarea (description)
    │   └── Footer Buttons
    └── Form submission
```

### GroupDetailPage

```
GroupDetailPage
├── Header
│   └── Back Button
├── GroupHeader
│   ├── Group info
│   ├── Member count
│   ├── Invite code display
│   └── Copy button
├── Main Content (2 columns)
│   ├── Left: Books List
│   │   ├── Add Book Button (admin)
│   │   └── BookCard[] (map over books)
│   │       ├── BookCover
│   │       ├── Book info
│   │       └── ProgressIndicator
│   └── Right: Sidebar
│       └── InviteCodeDisplay
│           ├── Invite link
│           ├── Copy Button
│           └── Share Button
└── Modal (Add Book)
    └── BookSearch
        ├── Search Input
        ├── Book results
        └── BookCover + info for each result
```

### BookDiscussionPage

```
BookDiscussionPage
├── Header
│   └── Back Button
├── Content (2 columns)
│   ├── Left Sidebar (1/3)
│   │   ├── Card (Book Info)
│   │   │   ├── BookCover (large)
│   │   │   ├── Title + Author
│   │   │   └── ISBN
│   │   └── Card (Progress)
│   │       ├── Update Button
│   │       └── ProgressIndicator
│   │           ├── Progress Ring (SVG)
│   │           ├── Progress Bar
│   │           └── Page numbers
│   └── Right Main (2/3)
│       ├── Discussion Header
│       ├── AheadNotifications
│       │   ├── Bell icon
│       │   ├── Count badge
│       │   └── Modal (on click)
│       │       └── List of ahead comments
│       ├── CommentInput
│       │   ├── Textarea
│       │   ├── Progress indicator
│       │   └── Submit Button
│       └── CommentFeed
│           └── CommentCard[] (map over comments)
│               ├── Avatar
│               ├── User name + timestamp
│               ├── Progress badge
│               ├── Comment content
│               └── Actions
│                   ├── Like Button (Heart)
│                   └── Report Button (Flag)
└── UpdateProgressModal
    ├── Modal
    ├── Input (current page)
    ├── Input (total pages)
    ├── Preview (percentage + buffer)
    └── Footer Buttons
```

### JoinGroupPage

```
JoinGroupPage
├── Welcome message
├── GoogleLoginButton (if not authenticated)
└── Loading spinner (if authenticated & joining)
```

## Component Dependency Graph

### Common Components (Used Everywhere)

```
Button
├── Used in: All pages, all modals
└── Variants: primary, secondary, outline, ghost, danger

Card
├── Used in: GroupCard, BookCard, all page layouts
└── Props: hover, className

Modal
├── Used in: CreateGroupModal, UpdateProgressModal, Report modal
└── Features: backdrop, close button, header, footer

Input
├── Used in: All forms
└── Features: label, error, helper text

Avatar
├── Used in: User displays, comment cards
└── Fallback: User icon

LoadingSpinner
├── Used in: All pages during data fetch
└── Sizes: sm, md, lg
```

### Feature-Specific Components

```
Auth Components
├── GoogleLoginButton
│   └── Uses: @react-oauth/google
└── ProtectedRoute
    └── Uses: useAuth, Navigate

Group Components
├── GroupCard
│   └── Uses: Card, Users icon, BookOpen icon
├── GroupHeader
│   └── Uses: Copy button, Settings button
├── CreateGroupModal
│   └── Uses: Modal, Input, Button
└── InviteCodeDisplay
    └── Uses: Card, Copy button, Share button

Book Components
├── BookCard
│   └── Uses: Card, BookCover, ProgressIndicator
├── BookCover
│   └── Fallback: BookOpen icon
└── BookSearch
    └── Uses: Input, Card, BookCover

Comment Components
├── CommentCard
│   └── Uses: Avatar, Heart icon, Flag icon, Modal
├── CommentFeed
│   └── Uses: CommentCard[], LoadingSpinner
├── CommentInput
│   └── Uses: Card, Button, Textarea
└── AheadNotifications
    └── Uses: Card, Modal, Bell icon

Progress Components
├── ProgressIndicator
│   ├── Compact mode: Progress bar only
│   └── Full mode: Ring + bar + numbers
└── UpdateProgressModal
    └── Uses: Modal, Input, Button
```

## Data Flow

### Authentication Flow

```
main.jsx
├── GoogleOAuthProvider
│   └── clientId from env
├── AuthProvider (Context)
│   ├── Manages user state
│   ├── login() function
│   ├── logout() function
│   └── Persists to localStorage
└── Components
    ├── useAuth() hook
    └── Access user, isAuthenticated
```

### API Data Flow

```
Component
├── Custom Hook (useGroups, useComments, etc.)
│   ├── useQuery / useMutation (TanStack Query)
│   │   ├── Query Key
│   │   ├── Query Function → Service
│   │   │   └── Service → api.js → Backend
│   │   └── Caching + Refetch
│   └── Returns data, loading, error
└── Render based on state
```

### Comment Visibility Flow

```
BookDiscussionPage
├── useProgress(groupId, bookId)
│   └── Fetches user's current progress
├── useComments(groupId, bookId)
│   ├── Sends user progress to backend
│   ├── Backend filters comments (progress - 3%)
│   ├── Returns visible comments
│   └── Returns ahead count
├── Render CommentFeed
│   └── Shows filtered comments
└── Render AheadNotifications
    └── Shows count of hidden comments
```

## State Management

### Global State (Context)

```
AuthContext
├── user: User | null
├── isLoading: boolean
├── isAuthenticated: boolean
├── login(credential): Promise
└── logout(): Promise
```

### Server State (React Query)

```
Query Keys
├── ['groups'] → User's groups
├── ['group', id] → Single group
├── ['groupBooks', id] → Books in group
├── ['book', id] → Single book
├── ['progress', groupId, bookId] → User progress
├── ['comments', groupId, bookId] → Visible comments
└── ['commentsAhead', groupId, bookId] → Ahead count

Mutations
├── createGroup
├── joinGroup
├── addBookToGroup
├── updateProgress
├── createComment
├── likeComment
└── reportComment
```

### Local State (useState)

```
Modals
├── showCreateModal
├── showAddBookModal
├── showProgressModal
└── showReportModal

Forms
├── Input values
├── Validation errors
└── Submission status

UI
├── copied (for copy buttons)
├── expanded (for collapsible)
└── activeTab (for tabs)
```

## Routing Tree

```
/ (root)
├── /login
│   └── Public
├── /join/:inviteCode
│   ├── Public (shows login if not authenticated)
│   └── Auto-joins if authenticated
├── / (home)
│   └── Protected → HomePage
├── /groups
│   └── Protected → GroupsPage
├── /groups/:groupId
│   └── Protected → GroupDetailPage
│       └── Dynamic: Load group by ID
└── /groups/:groupId/books/:bookId
    └── Protected → BookDiscussionPage
        └── Dynamic: Load book & comments by IDs
```

## Hook Usage Map

### useAuth

```
Used in:
├── App.jsx (check loading)
├── LoginPage.jsx (redirect if authenticated)
├── GroupsPage.jsx (display user, logout)
├── BookDiscussionPage.jsx (get current user ID)
└── ProtectedRoute.jsx (check authentication)
```

### useGroups

```
Used in:
├── GroupsPage.jsx
│   ├── Get all groups
│   ├── Create new group
│   └── Display group list
└── JoinGroupPage.jsx
    └── Join group by invite code
```

### useGroup (single)

```
Used in:
├── GroupDetailPage.jsx
│   └── Load group details
└── (Any page needing single group info)
```

### useComments

```
Used in:
├── BookDiscussionPage.jsx
│   ├── Load visible comments
│   ├── Load ahead count
│   ├── Create new comment
│   ├── Like comment
│   └── Report comment
└── (Nowhere else)
```

### useProgress

```
Used in:
├── BookDiscussionPage.jsx
│   ├── Load user progress
│   ├── Update progress
│   └── Determine comment visibility
└── (Passed to child components)
```

## Icon Usage

### Lucide React Icons Used

```
Navigation & Actions
├── ArrowLeft (back buttons)
├── Plus (create/add buttons)
├── Edit (edit buttons)
├── LogOut (logout)
├── Copy (copy invite)
├── Share2 (share invite)
├── Send (send comment)
└── Check (success states)

Content
├── BookOpen (book/reading)
├── Users (groups/members)
├── MessageSquare (comments)
├── Bell (notifications)
├── Heart (likes)
└── Flag (reports)

UI
├── X (close modals)
├── ChevronRight (navigation)
├── MoreVertical (menus)
├── Loader2 (loading)
├── Search (search)
├── Settings (settings)
└── User (avatar fallback)
```

## CSS Class Patterns

### TailwindCSS Patterns

```
Layout
├── flex items-center justify-between
├── grid md:grid-cols-2 lg:grid-cols-3
├── max-w-5xl mx-auto px-4 py-8
└── space-y-6 (vertical spacing)

Colors
├── bg-primary text-white
├── bg-surface border-border
├── text-text-primary / secondary / tertiary
└── hover:bg-primary-dark

Effects
├── rounded-lg shadow-md
├── transition-all duration-200
├── hover:shadow-lg
└── focus:ring-2 focus:ring-primary

Responsive
├── hidden sm:block
├── md:flex-row
└── lg:col-span-2
```

## Props Patterns

### Common Props

```
Button
├── variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
├── size: 'sm' | 'md' | 'lg'
├── loading: boolean
├── disabled: boolean
├── icon: ReactNode
└── onClick: () => void

Card
├── className: string
├── hover: boolean
└── children: ReactNode

Modal
├── isOpen: boolean
├── onClose: () => void
├── title: string
├── size: 'sm' | 'md' | 'lg' | 'full'
├── children: ReactNode
└── footer: ReactNode

Input
├── label: string
├── value: string
├── onChange: (e) => void
├── error: string
├── helper: string
└── ...props (spread to input)
```

## Summary

This component tree shows:
- ✅ Clear hierarchy and relationships
- ✅ Reusable component patterns
- ✅ Separation of concerns
- ✅ Data flow paths
- ✅ State management strategy
- ✅ Routing structure
- ✅ Hook usage
- ✅ Icon organization
- ✅ CSS patterns

The architecture is:
- **Modular**: Components are independent
- **Composable**: Components build on each other
- **Reusable**: Common components used everywhere
- **Maintainable**: Clear structure and naming
- **Scalable**: Easy to add new features

Perfect for understanding how everything connects!
