# BookClub Frontend

A beautiful, production-ready React frontend for the BookClub platform - discuss books without spoilers.

## Features

- **Spoiler-Free Discussions**: Only see comments from readers at or behind your progress
- **Google OAuth Authentication**: Secure, passwordless login
- **Reading Progress Tracking**: Track your progress across different editions
- **Group Management**: Create and join book clubs with invite links
- **Real-time Updates**: Live comment feeds and notifications
- **Responsive Design**: Beautiful on all devices
- **Book Search**: Search and add books via Open Library API

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client
- **Zustand** - State management
- **React Hot Toast** - Notifications
- **Lucide React** - Icon library
- **date-fns** - Date formatting

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Configure environment variables:
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── auth/           # Authentication components
│   ├── books/          # Book-related components
│   ├── comments/       # Comment system components
│   ├── common/         # Reusable UI components
│   ├── groups/         # Group management components
│   └── progress/       # Reading progress components
├── contexts/           # React contexts
├── hooks/              # Custom React hooks
├── pages/              # Page components
├── services/           # API service layer
├── styles/             # Global styles
├── App.jsx             # Main app component
└── main.jsx            # App entry point
```

## Design System

### Colors

- **Primary**: Deep sage green (#2C5F4F)
- **Background**: Warm off-white (#FAF9F6)
- **Accent**: Book leather tan (#C7956D)
- **Text**: Rich blacks and grays
- **Danger**: Muted red (#C85A54)
- **Success**: Forest green (#5A8C6F)

### Typography

- **Headings**: Merriweather (serif)
- **Body**: Inter (sans-serif)
- **Code/Progress**: JetBrains Mono (monospace)

## Key Components

### Authentication
- `GoogleLoginButton` - Google OAuth login
- `ProtectedRoute` - Route protection wrapper

### Groups
- `GroupCard` - Group display card
- `GroupHeader` - Group page header
- `CreateGroupModal` - Group creation form
- `InviteCodeDisplay` - Shareable invite links

### Books
- `BookCard` - Book display with progress
- `BookCover` - Book cover image
- `BookSearch` - Search books via Open Library

### Comments
- `CommentCard` - Individual comment display
- `CommentFeed` - Comment list
- `CommentInput` - Create new comments
- `AheadNotifications` - Show comments ahead of progress

### Progress
- `ProgressIndicator` - Visual progress display
- `UpdateProgressModal` - Update reading progress

### Common
- `Button` - Styled button component
- `Card` - Container card component
- `Input` - Form input component
- `Modal` - Modal dialog component
- `Avatar` - User avatar component
- `LoadingSpinner` - Loading indicator

## Pages

- **LoginPage** - Google OAuth authentication
- **HomePage** - Welcome and onboarding
- **GroupsPage** - List of user's groups
- **GroupDetailPage** - Single group view
- **BookDiscussionPage** - Book discussion and comments
- **JoinGroupPage** - Join via invite link

## Custom Hooks

- `useAuth` - Authentication state and actions
- `useGroups` - Group management
- `useComments` - Comment CRUD operations
- `useProgress` - Reading progress tracking

## API Services

All API calls are abstracted in the `services/` directory:

- `api.js` - Axios instance with interceptors
- `authService.js` - Authentication endpoints
- `groupService.js` - Group management endpoints
- `bookService.js` - Book search and management
- `commentService.js` - Comment operations
- `progressService.js` - Progress tracking

## Features Implementation

### Comment Visibility Logic

Comments are filtered based on the 3% buffer rule:
- Users can only see comments from readers at `current_progress - 3%` or less
- Comments ahead are counted and shown in notifications
- Updates happen in real-time every 30 seconds

### Reading Progress

- Supports different editions with page count conversion
- Calculates percentage automatically
- 3% buffer prevents exact-page spoilers
- Visual progress indicators (bar and ring)

### Group Invites

- 12-character unique invite codes
- Shareable links: `/join/{inviteCode}`
- Auto-join on authentication
- Copy-to-clipboard and native share support

## Environment Variables

- `VITE_API_URL` - Backend API URL
- `VITE_GOOGLE_CLIENT_ID` - Google OAuth client ID

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

### Railway

1. Create new project from GitHub
2. Add environment variables
3. Deploy

### Netlify

1. Connect repository
2. Build command: `npm run build`
3. Publish directory: `dist`
4. Add environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.
