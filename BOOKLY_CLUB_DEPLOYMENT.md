# Complete Deployment Guide for bookly.club

## Quick Start Summary

**What you need:**
1. Domain: bookly.club (purchased)
2. GitHub account
3. Vercel account (frontend hosting - FREE)
4. Railway/Render account (backend + database - ~$5-10/month)
5. Google OAuth credentials (production)
6. Cloudinary account (avatar uploads - FREE tier)

**Total Setup Time:** 30-45 minutes
**Monthly Cost:** $5-10 (Railway) or $7+ (Render)

---

## Step-by-Step Deployment for bookly.club

### 1️⃣ Push Code to GitHub (5 minutes)

```bash
# Navigate to your project
cd c:\Users\Surface\projects\bookclub-platform

# Initialize git (if not already done)
git init
git branch -M main

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create GitHub repository
# Go to github.com → New Repository → Name it "bookclub-platform"
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/bookclub-platform.git
git push -u origin main
```

---

### 2️⃣ Set Up Google OAuth for Production (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project or create new one: "BookClub Production"
3. **APIs & Services** → **Credentials** → **OAuth 2.0 Client IDs**
4. Click your OAuth client (or create new one)
5. Add **Authorized JavaScript origins:**
   - `https://bookly.club`
   - `https://www.bookly.club`
6. Add **Authorized redirect URIs:**
   - `https://api.bookly.club/auth/google/callback`
   - `https://bookly.club`
7. **Save** and copy your:
   - Client ID: `12345.apps.googleusercontent.com`
   - Client Secret: `GOCSPX-xxxxx`

---

### 3️⃣ Set Up Cloudinary (2 minutes)

1. Go to [cloudinary.com](https://cloudinary.com)
2. Sign up for free account
3. From dashboard, copy:
   - Cloud Name
   - API Key
   - API Secret

---

### 4️⃣ Deploy Backend to Railway (10 minutes)

**Recommended: Railway is easiest and most reliable**

#### Step A: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

#### Step B: Deploy PostgreSQL Database
1. Click **"New Project"**
2. Select **"Provision PostgreSQL"**
3. Database is created automatically
4. Click on PostgreSQL service → **"Variables"** tab
5. Copy the `DATABASE_URL` (you'll need this)

#### Step C: Deploy Backend Service
1. In your Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose `bookclub-platform` repository
4. Railway will auto-detect the Dockerfile in `/backend`
5. Set **Root Directory** to `backend`

#### Step D: Configure Environment Variables
Click on backend service → **"Variables"** tab → Add all these:

```
DATABASE_URL=<paste from PostgreSQL service>
ENVIRONMENT=production
FRONTEND_URL=https://bookly.club
GOOGLE_CLIENT_ID=<from Google Console>
GOOGLE_CLIENT_SECRET=<from Google Console>
GOOGLE_REDIRECT_URI=https://api.bookly.club/auth/google/callback
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
OPEN_LIBRARY_API_URL=https://openlibrary.org
CLOUDINARY_CLOUD_NAME=<from Cloudinary>
CLOUDINARY_API_KEY=<from Cloudinary>
CLOUDINARY_API_SECRET=<from Cloudinary>
```

**Generate SECRET_KEY:**
```bash
# On Windows (PowerShell):
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})

# Or use this online: https://randomkeygen.com/ (choose 256-bit key)
```

Add as environment variable:
```
SECRET_KEY=<your-generated-64-character-key>
```

#### Step E: Set Up Custom Domain for Backend
1. In Railway, click backend service → **"Settings"** → **"Domains"**
2. Click **"Custom Domain"**
3. Enter: `api.bookly.club`
4. Railway will give you a CNAME value (like `bookclub-backend.up.railway.app`)
5. **Save this** - you'll add it to DNS later

#### Step F: Deploy
1. Click **"Deploy"** (if not auto-deployed)
2. Wait 2-3 minutes for build
3. Check logs to ensure it started successfully
4. Test: Visit `https://api.bookly.club/health` (after DNS is set up)

---

### 5️⃣ Deploy Frontend to Vercel (10 minutes)

#### Step A: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

#### Step B: Import Project
1. Click **"Add New..."** → **"Project"**
2. Import `bookclub-platform` from GitHub
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

#### Step C: Add Environment Variables
Click **"Environment Variables"** and add:

```
VITE_API_URL=https://api.bookly.club
VITE_GOOGLE_CLIENT_ID=<same as backend Google Client ID>
```

#### Step D: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Vercel will give you a URL like `bookclub-platform-xyz.vercel.app`

#### Step E: Set Up Custom Domain
1. Go to project → **"Settings"** → **"Domains"**
2. Add domain: `bookly.club`
3. Add domain: `www.bookly.club`
4. Vercel will show DNS records to add
5. **Save these** - you'll add them to DNS next

---

### 6️⃣ Configure DNS at Your Domain Registrar (5 minutes)

**Go to where you bought bookly.club** (Namecheap, GoDaddy, Cloudflare, etc.)

#### Add these DNS records:

**For Frontend (bookly.club):**
```
Type: CNAME
Name: @  (or bookly.club)
Value: cname.vercel-dns.com
TTL: Automatic
```

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: Automatic
```

**For Backend (api.bookly.club):**
```
Type: CNAME
Name: api
Value: <from Railway, e.g., bookclub-backend.up.railway.app>
TTL: Automatic
```

**Note:** DNS changes can take 5 minutes to 24 hours to propagate (usually ~15 minutes)

---

### 7️⃣ Test Your Deployment (5 minutes)

#### Wait for DNS Propagation
Check if domains are live:
```bash
# On Windows Command Prompt:
nslookup bookly.club
nslookup api.bookly.club
```

#### Test Backend
1. Visit: `https://api.bookly.club/health`
2. Should return:
```json
{
  "status": "healthy",
  "database": "healthy",
  "environment": "production"
}
```

#### Test Frontend
1. Visit: `https://bookly.club`
2. Should load the BookClub homepage
3. Click **"Sign in with Google"**
4. Complete OAuth flow
5. Create a test group
6. Add a book
7. Post a comment

#### Verify Everything Works
- [ ] Can log in with Google
- [ ] Can create a group
- [ ] Can join a group with invite code
- [ ] Can add books
- [ ] Can update reading progress
- [ ] Can post comments
- [ ] Comments show/hide based on progress
- [ ] Can upload avatar (Cloudinary)

---

## 🎉 You're Live!

Your BookClub platform is now running at:
- **Frontend:** https://bookly.club
- **Backend API:** https://api.bookly.club

---

## Making Updates After Deployment

### Option 1: Work with Claude Code (Recommended)

```bash
# Make changes locally with Claude Code
# Test locally first
npm run dev  # frontend
python -m uvicorn app.main:app  # backend

# Commit and push
git add .
git commit -m "Add new feature X"
git push origin main

# Vercel and Railway auto-deploy!
```

### Option 2: Manual Updates

Same process - just make your changes, commit, and push. Both platforms auto-deploy when you push to `main` branch.

---

## Monitoring Your App

### Railway (Backend)
1. Go to Railway dashboard
2. Click your backend service
3. View **"Deployments"** tab for build logs
4. View **"Metrics"** tab for performance
5. View **"Logs"** tab for real-time logs

### Vercel (Frontend)
1. Go to Vercel dashboard
2. Click your project
3. View **"Deployments"** for build history
4. View **"Logs"** for runtime logs
5. View **"Analytics"** for traffic (free tier)

### Database
1. In Railway, click PostgreSQL service
2. View **"Metrics"** for database usage
3. Set up automated backups in Railway settings

---

## Costs Breakdown

| Service | What It Does | Cost |
|---------|-------------|------|
| Vercel | Frontend hosting | **FREE** |
| Railway | Backend + PostgreSQL | **$5-10/month** |
| Google OAuth | Authentication | **FREE** |
| Cloudinary | Avatar uploads | **FREE** (25 credits/month) |
| bookly.club domain | Your domain | **~$12/year** |
| **Total** | | **~$7-13/month** |

---

## Troubleshooting

### "API request failed" on frontend
- Check `VITE_API_URL` in Vercel environment variables
- Ensure backend is running on Railway
- Check CORS settings (FRONTEND_URL in backend)

### Google OAuth fails
- Verify redirect URIs in Google Console match exactly
- Check `GOOGLE_CLIENT_ID` matches in both frontend and backend
- Ensure domain is using HTTPS (not HTTP)

### Database connection error
- Check `DATABASE_URL` in Railway backend variables
- Ensure PostgreSQL service is running
- Verify database migrations ran (check Railway logs)

### 404 errors on page refresh
- Frontend: Vercel should handle this automatically with `vercel.json`
- If not working, check that `vercel.json` was deployed

### Images not uploading
- Verify Cloudinary credentials in backend
- Check Cloudinary dashboard for usage
- Ensure image size is under 2MB

---

## Security Checklist

- [x] Using HTTPS (SSL) on both domains
- [x] Environment variables not in code
- [x] `.env` files in `.gitignore`
- [x] Google OAuth restricted to production domains
- [x] Database not publicly accessible
- [ ] Set up error monitoring (optional: Sentry)
- [ ] Enable rate limiting (future enhancement)
- [ ] Regular dependency updates

---

## Next Steps (Optional)

### Set Up Email Notifications
- Add email service (SendGrid, Mailgun)
- Notify users of new comments in their groups

### Add Analytics
- Google Analytics
- PostHog (open source)

### Set Up Error Tracking
- Sentry for backend errors
- Sentry for frontend errors

### Add More Features
- Book recommendations
- Reading streaks
- Group leaderboards
- Mobile app (React Native)

---

## Support & Resources

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Docs:** https://react.dev

---

## Emergency Rollback

If deployment breaks something:

### Vercel (Frontend)
1. Go to **"Deployments"**
2. Find last working deployment
3. Click **"..."** → **"Promote to Production"**

### Railway (Backend)
1. Go to **"Deployments"**
2. Find last working deployment
3. Click **"..."** → **"Redeploy"**

---

**🚀 Your BookClub platform is ready for the world!**
