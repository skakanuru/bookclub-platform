# Frontend Setup Guide

Complete guide to get the BookClub frontend up and running.

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

## Detailed Setup

### 1. Install Dependencies

```bash
npm install
```

This will install:
- React & React DOM
- Vite (build tool)
- TailwindCSS (styling)
- React Router (routing)
- TanStack Query (data fetching)
- Axios (HTTP client)
- Google OAuth library
- Zustand (state management)
- Date-fns (date formatting)
- React Hot Toast (notifications)
- Lucide React (icons)

### 2. Configure Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
```

**Getting Google Client ID:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Choose "Web application"
6. Add authorized JavaScript origins:
   - `http://localhost:3000` (development)
   - Your production domain
7. Add authorized redirect URIs:
   - `http://localhost:3000` (development)
   - Your production domain
8. Copy the Client ID

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Verify Backend Connection

Make sure the backend is running at `http://localhost:8000` (or your configured API URL).

Test the connection:
- Open the frontend
- Try to login
- Check browser console for errors

## Available Scripts

### `npm run dev`
Starts the Vite development server with hot reload.

### `npm run build`
Builds the app for production to the `dist/` folder.

### `npm run preview`
Preview the production build locally.

### `npm run lint`
Run ESLint to check code quality.

## Troubleshooting

### Port 3000 Already in Use

Change the port in `vite.config.js`:

```js
export default defineConfig({
  server: {
    port: 3001, // or any other port
  }
})
```

### Google OAuth Not Working

1. Check that `VITE_GOOGLE_CLIENT_ID` is set correctly
2. Verify authorized origins in Google Cloud Console
3. Clear browser cache and cookies
4. Check browser console for specific errors

### API Connection Issues

1. Verify backend is running
2. Check `VITE_API_URL` in `.env`
3. Check CORS settings on backend
4. Verify API endpoints match frontend services

### Build Errors

1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`

### Styling Not Applied

1. Verify TailwindCSS is configured correctly
2. Check that `index.css` is imported in `main.jsx`
3. Clear browser cache
4. Restart dev server

## Development Tips

### Hot Reload

Vite provides instant hot module replacement (HMR). Changes to React components will update instantly without losing state.

### Browser DevTools

Use React DevTools browser extension for debugging:
- [Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [Firefox](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

### API Debugging

Check the Network tab in browser DevTools to see all API requests and responses.

### State Management

Use the React Query DevTools (automatically enabled in development) to inspect cache state.

## Production Build

### 1. Build

```bash
npm run build
```

### 2. Test Build Locally

```bash
npm run preview
```

### 3. Deploy

The `dist/` folder contains the production build. Deploy it to:

- **Vercel**: `vercel deploy`
- **Netlify**: Drag & drop `dist/` folder
- **Railway**: Connect GitHub repo
- **Static hosting**: Upload `dist/` contents

### Environment Variables in Production

Set these environment variables in your hosting platform:

```
VITE_API_URL=https://your-api-domain.com
VITE_GOOGLE_CLIENT_ID=your_production_google_client_id
```

**Important**: Don't forget to update Google OAuth authorized origins with your production domain!

## Project Dependencies

### Core
- `react@^18.3.1`
- `react-dom@^18.3.1`

### Routing
- `react-router-dom@^6.22.0`

### Data Fetching
- `@tanstack/react-query@^5.20.0`
- `axios@^1.6.7`

### Authentication
- `@react-oauth/google@^0.12.1`

### State Management
- `zustand@^4.5.0`

### UI & Styling
- `tailwindcss@^3.4.1`
- `lucide-react@^0.323.0`
- `react-hot-toast@^2.4.1`

### Utilities
- `date-fns@^3.3.1`

### Build Tools
- `vite@^5.4.10`
- `@vitejs/plugin-react@^4.3.3`

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Performance Optimization

The app includes:
- Code splitting by route
- Lazy loading of images
- React Query caching
- Optimized re-renders
- Production build minification

## Security

- HTTPS in production
- HTTP-only cookies for tokens
- CORS configuration
- Input sanitization
- XSS protection

## Next Steps

1. Set up backend API
2. Configure Google OAuth
3. Test all user flows
4. Deploy to production
5. Monitor errors and performance

## Support

If you encounter issues:
1. Check this guide
2. Review console errors
3. Check backend logs
4. Open an issue on GitHub
