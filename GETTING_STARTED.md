# Getting Started - BookClub Platform MVP

## 🎯 You're Almost Ready to Launch!

This guide will get you from zero to running MVP in **under 30 minutes**.

---

## Prerequisites Check

Before you start, make sure you have:

- [ ] **Windows PC** (you're on Surface - perfect!)
- [ ] **Python 3.10+** installed
- [ ] **Node.js 18+** installed
- [ ] **Docker Desktop** installed (or PostgreSQL)
- [ ] **Google account** for OAuth setup
- [ ] **Text editor** (VS Code recommended)
- [ ] **30 minutes** of focused time

---

## Step-by-Step Setup

### Step 1: Verify Installation (2 minutes)

Open PowerShell or Command Prompt:

```bash
# Check Python
python --version
# Should show: Python 3.10.x or higher

# Check Node
node --version
# Should show: v18.x.x or higher

# Check Docker (optional)
docker --version
# Should show: Docker version 20.x.x or higher
```

**If anything is missing:**
- Python: https://www.python.org/downloads/
- Node: https://nodejs.org/
- Docker Desktop: https://www.docker.com/products/docker-desktop

### Step 2: Navigate to Project (1 minute)

```bash
cd C:\Users\Surface\projects\bookclub-platform
```

### Step 3: Set Up Google OAuth (5 minutes)

This is the most important step!

1. **Go to Google Cloud Console:**
   https://console.cloud.google.com/

2. **Create New Project:**
   - Click "Select a project" → "New Project"
   - Name: "BookClub Platform"
   - Click "Create"

3. **Enable Google+ API:**
   - Search for "Google+ API" in search bar
   - Click "Enable"

4. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - User Type: **External**
   - App name: "BookClub Platform"
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com
   - Click "Save and Continue"
   - Scopes: Keep defaults
   - Test users: Add your email and book club members' emails
   - Click "Save and Continue"

5. **Create OAuth Credentials:**
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: **Web application**
   - Name: "BookClub Web App"
   - Authorized JavaScript origins:
     - `http://localhost:5173`
     - `http://localhost:8000`
   - Authorized redirect URIs:
     - `http://localhost:8000/auth/google/callback`
   - Click "Create"
   - **COPY** your Client ID and Client Secret (you'll need these!)

### Step 4: Set Up Cloudinary (3 minutes)

For avatar uploads:

1. **Create Account:**
   https://cloudinary.com/users/register/free

2. **Go to Dashboard:**
   https://console.cloudinary.com/

3. **Copy Credentials:**
   - Cloud Name
   - API Key
   - API Secret

### Step 5: Configure Backend (3 minutes)

```bash
cd backend

# Copy environment template
copy .env.example .env

# Open .env in notepad
notepad .env
```

**Edit these values in .env:**

```env
# Database (use this for local development)
DATABASE_URL=postgresql://postgres:password@localhost:5432/bookclub

# Google OAuth (paste your credentials from Step 3)
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Generate this: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=paste-generated-secret-key-here

# Leave these as-is for local development
FRONTEND_URL=http://localhost:5173
OPEN_LIBRARY_API_URL=https://openlibrary.org

# Cloudinary (paste your credentials from Step 4)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Environment
ENVIRONMENT=development
```

**Save and close.**

### Step 6: Generate SECRET_KEY (1 minute)

Open a new terminal:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as your `SECRET_KEY` in backend/.env

### Step 7: Set Up Backend Dependencies (3 minutes)

```bash
# Still in backend/ directory
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

You should see packages installing. This may take 2-3 minutes.

### Step 8: Start Database (2 minutes)

**Option A: Using Docker (Recommended)**

```bash
# In a NEW terminal (keep backend terminal open)
docker run -d --name bookclub-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bookclub -p 5432:5432 postgres:15
```

**Option B: Using Local PostgreSQL**

If you installed PostgreSQL locally:
```bash
# Create database
createdb bookclub
```

### Step 9: Run Database Migrations (1 minute)

Back in your backend terminal (with venv activated):

```bash
# Still in backend/ directory
alembic upgrade head
```

You should see:
```
INFO  [alembic.runtime.migration] Running upgrade  -> xxx, Initial schema
```

### Step 10: Start Backend (1 minute)

```bash
# Still in backend/ directory with venv activated
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Backend is running!**

Keep this terminal open and visit: http://localhost:8000/docs
You should see the API documentation.

### Step 11: Set Up Frontend (3 minutes)

Open a **NEW** terminal:

```bash
cd C:\Users\Surface\projects\bookclub-platform\frontend

# Copy environment template
copy .env.example .env

# Open .env
notepad .env
```

**Edit frontend/.env:**

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
```

Use the **same Google Client ID** from Step 3.

**Save and close.**

### Step 12: Install Frontend Dependencies (3 minutes)

```bash
# Still in frontend/ directory
npm install
```

This will take 2-3 minutes to install all packages.

### Step 13: Start Frontend (1 minute)

```bash
# Still in frontend/ directory
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**✅ Frontend is running!**

---

## 🎉 You're Ready!

### Open Your Browser

Visit: **http://localhost:5173**

You should see the BookClub Platform homepage!

### First Steps in the App

1. **Click "Sign in with Google"**
   - Choose your Google account
   - Grant permissions
   - You'll be redirected back to the app

2. **Create Your First Group**
   - Click "Create Group"
   - Name: "My Book Club"
   - Description: "Testing the MVP"
   - Click "Create"

3. **Copy the Invite Code**
   - You'll see a code like: `ABC123XYZ`
   - Share this with your book club members!

4. **Add a Book**
   - Click "Add Book"
   - Search for a book (e.g., "Harry Potter")
   - Select from results
   - Click "Add to Group"

5. **Set Your Progress**
   - Click "Update Progress"
   - Enter your edition's total pages (e.g., 300)
   - Enter your current page (e.g., 50)
   - Click "Save"

6. **Post Your First Comment**
   - Scroll to the comment box
   - Write: "Testing the MVP! This is awesome 🎉"
   - Click "Post"

7. **Invite Your Book Club**
   - Share the invite code with friends
   - Or share the direct link: `http://localhost:5173/join/ABC123XYZ`

---

## Testing Spoiler Protection

To test the core feature:

1. **In your browser:**
   - Set progress to page 50
   - Post comment: "Chapter 3 is great!"

2. **Open incognito/private window:**
   - Go to http://localhost:5173
   - Sign in with a different Google account (or test account)
   - Join the same group
   - Set progress to page 100
   - Post comment: "Plot twist in chapter 8!"

3. **Back in your main browser:**
   - Refresh the page
   - You should **NOT** see the chapter 8 comment
   - You should see a badge: "1 comment ahead"

4. **Update your progress to page 100:**
   - Now you can see the chapter 8 comment!

**If this works, your MVP is functioning correctly! 🎊**

---

## Troubleshooting

### "Database connection failed"
- Make sure Docker container is running: `docker ps`
- Or PostgreSQL service is running if installed locally

### "Google OAuth error"
- Check GOOGLE_CLIENT_ID matches in both backend/.env and frontend/.env
- Verify redirect URI in Google Console: http://localhost:8000/auth/google/callback

### "Port already in use"
- Backend: Kill process using port 8000
  ```bash
  netstat -ano | findstr :8000
  taskkill /PID <process-id> /F
  ```
- Frontend: Kill process using port 5173 (same as above, replace 8000 with 5173)

### "Module not found" errors
- Backend: Make sure venv is activated: `venv\Scripts\activate`
- Frontend: Run `npm install` again

### "CORS error" in browser console
- Check FRONTEND_URL in backend/.env is http://localhost:5173
- Restart backend server

---

## Next Steps

Once everything works locally:

1. **Test with your book club** (all on local network or same computer)
2. **Fix any bugs** you find
3. **Deploy to production** (see DEPLOYMENT.md)
4. **Share with your book club** and start reading!

---

## Quick Reference

**Backend:**
- Directory: `C:\Users\Surface\projects\bookclub-platform\backend`
- Start: `venv\Scripts\activate && uvicorn app.main:app --reload`
- API Docs: http://localhost:8000/docs

**Frontend:**
- Directory: `C:\Users\Surface\projects\bookclub-platform\frontend`
- Start: `npm run dev`
- App: http://localhost:5173

**Database:**
- Docker: `docker start bookclub-db` (if stopped)
- Connect: `psql -U postgres -h localhost -d bookclub`

---

## Getting Help

If you're stuck:

1. Check the error message in terminal
2. Check browser console (F12 → Console tab)
3. Review QUICKSTART.md for more details
4. Check TESTING_GUIDE.md for common issues
5. Ask for help!

---

**Time to Complete:** ~30 minutes
**Difficulty:** Beginner-friendly
**Result:** Fully functional MVP ready to test!

**Happy reading! 📚**
