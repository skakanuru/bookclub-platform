# BookClub Frontend - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Node.js 18+ installed
- npm installed
- Backend running (optional for initial setup)

## Installation (3 Steps)

### 1. Install Dependencies

```bash
cd C:\Users\Surface\projects\bookclub-platform\frontend
npm install
```

This will install all required packages (~300MB, takes 2-3 minutes).

### 2. Configure Environment

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and set your values:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
```

**Google Client ID Setup:**
1. Go to https://console.cloud.google.com/
2. Create project (or select existing)
3. Enable "Google+ API"
4. Create OAuth 2.0 Client ID
5. Add origin: `http://localhost:3000`
6. Copy Client ID to `.env`

### 3. Start Development Server

```bash
npm run dev
```

App will start at: **http://localhost:3000**

## First Run

When you first open the app:

1. You'll see the **LoginPage**
2. Click "Continue with Google"
3. Authenticate with Google
4. You'll be redirected to **HomePage**
5. Click "View My Groups" or "Create Group"

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components (6 pages)
│   ├── services/       # API integration (6 services)
│   ├── hooks/          # Custom React hooks
│   ├── contexts/       # React contexts
│   └── styles/         # Global CSS
├── package.json        # Dependencies
├── vite.config.js      # Build configuration
└── tailwind.config.js  # Styling configuration
```

## Available Commands

```bash
# Development server (hot reload)
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Testing Without Backend

The frontend will show error messages if the backend is not running, but you can still:
- View the UI/UX design
- See the page layouts
- Test navigation
- Inspect components

To fully test, you need the backend running at `http://localhost:8000`.

## Common Issues

### Port 3000 Already in Use

Change port in `vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 3001, // Change this
  }
})
```

### Google OAuth Error

1. Check `VITE_GOOGLE_CLIENT_ID` is set correctly
2. Verify authorized origins in Google Cloud Console
3. Clear browser cache

### API Connection Failed

1. Check backend is running on port 8000
2. Verify `VITE_API_URL` in `.env`
3. Check browser console for errors

## Development Workflow

### 1. Make Changes

Edit files in `src/` directory. Changes will hot-reload instantly.

### 2. Check Browser

Open browser console (F12) to see any errors.

### 3. Test Features

Navigate through the app to test your changes.

### 4. Build

Before deploying, test the production build:

```bash
npm run build
npm run preview
```

## File Locations

**Pages:**
- `src/pages/LoginPage.jsx` - Login screen
- `src/pages/HomePage.jsx` - Welcome page
- `src/pages/GroupsPage.jsx` - List of groups
- `src/pages/GroupDetailPage.jsx` - Single group view
- `src/pages/BookDiscussionPage.jsx` - Main discussion
- `src/pages/JoinGroupPage.jsx` - Join via invite

**Key Components:**
- `src/components/common/` - Buttons, cards, inputs
- `src/components/groups/` - Group management
- `src/components/comments/` - Comment system
- `src/components/progress/` - Progress tracking

**Services:**
- `src/services/api.js` - HTTP client setup
- `src/services/authService.js` - Authentication
- `src/services/groupService.js` - Group operations
- `src/services/commentService.js` - Comment operations

## Design System

**Colors:**
- Primary: `#2C5F4F` (Deep sage green)
- Background: `#FAF9F6` (Warm off-white)
- Accent: `#C7956D` (Book leather)

**Typography:**
- Headings: Merriweather (serif)
- Body: Inter (sans-serif)

**Components:**
- Button: 5 variants (primary, secondary, outline, ghost, danger)
- Card: Reusable container with optional hover
- Modal: Responsive dialog
- Input: Form input with validation

## Key Features

### 1. Authentication
- Google OAuth only
- Token-based (JWT)
- Protected routes

### 2. Groups
- Create new groups
- Join via invite code
- Share invite links

### 3. Books
- Search Open Library API
- Add to groups
- Display covers

### 4. Progress
- Track page & percentage
- Different editions support
- 3% buffer zone

### 5. Comments
- Post at current progress
- Filtered visibility (spoiler-free)
- Like and report
- Real-time updates

## Next Steps

1. **Backend Setup**: Get the backend API running
2. **Google OAuth**: Configure properly in Google Cloud Console
3. **Test Flows**: Try creating groups, joining, commenting
4. **Customize**: Modify components to your needs
5. **Deploy**: Build and deploy to production

## Resources

**Documentation:**
- `README.md` - Overview
- `SETUP.md` - Detailed setup
- `FRONTEND_OVERVIEW.md` - Technical deep dive
- `COMPONENT_TREE.md` - Component structure

**External:**
- React: https://react.dev
- Vite: https://vitejs.dev
- TailwindCSS: https://tailwindcss.com
- React Query: https://tanstack.com/query

## Support

**Issues?**
1. Check console for errors
2. Review documentation
3. Check backend connection
4. Open GitHub issue

## Production Deployment

### Quick Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel deploy
```

Set environment variables in Vercel dashboard:
- `VITE_API_URL` - Your API URL
- `VITE_GOOGLE_CLIENT_ID` - Production Client ID

### Quick Deploy to Netlify

1. Build: `npm run build`
2. Upload `dist/` folder to Netlify
3. Set environment variables
4. Done!

## Summary

You now have:
- ✅ Complete React frontend
- ✅ All components built
- ✅ API integration ready
- ✅ Beautiful UI/UX
- ✅ Production-ready code

**Start building your book club!** 📚

---

**Need Help?** Check the other documentation files or open an issue.
