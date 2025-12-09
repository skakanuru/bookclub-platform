# Deployment Guide - BookClub Platform

## Deployment Options

### Option 1: Railway (Recommended - Easiest)
### Option 2: Render
### Option 3: Manual VPS Deployment

---

## Option 1: Railway Deployment (Recommended)

**Cost:** ~$10/month ($120/year)
**Setup Time:** 15 minutes
**Difficulty:** Easy

### Prerequisites
1. GitHub account
2. Railway account (https://railway.app/)
3. Google OAuth credentials (production)
4. Cloudinary account

### Step 1: Prepare Your Repository

```bash
# Push your code to GitHub
git remote add origin https://github.com/yourusername/bookclub-platform.git
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `bookclub-platform` repository
5. Railway will detect it's a monorepo

### Step 3: Deploy Database

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically provisions a PostgreSQL database
4. Copy the `DATABASE_URL` from database settings

### Step 4: Deploy Backend

1. Click "New" → "GitHub Repo"
2. Select your repository
3. Set **Root Directory**: `backend`
4. Add environment variables:
   ```
   DATABASE_URL=<from railway postgres>
   GOOGLE_CLIENT_ID=your-production-client-id
   GOOGLE_CLIENT_SECRET=your-production-secret
   GOOGLE_REDIRECT_URI=https://your-backend-url.railway.app/auth/google/callback
   SECRET_KEY=<generate-with-openssl-rand-hex-32>
   FRONTEND_URL=https://your-frontend-url.railway.app
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ENVIRONMENT=production
   ```
5. Click "Deploy"
6. Note your backend URL: `https://bookclub-backend-xyz.railway.app`

### Step 5: Run Database Migrations

1. In Railway backend service, go to "Settings"
2. Add **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
3. Or use Railway CLI:
   ```bash
   railway run alembic upgrade head
   ```

### Step 6: Deploy Frontend

1. Click "New" → "GitHub Repo"
2. Select your repository
3. Set **Root Directory**: `frontend`
4. Add environment variables:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   VITE_GOOGLE_CLIENT_ID=your-production-client-id
   ```
5. Set **Build Command**: `npm install && npm run build`
6. Set **Start Command**: `npm run preview -- --host --port $PORT`
7. Click "Deploy"
8. Note your frontend URL: `https://bookclub-xyz.railway.app`

### Step 7: Update Google OAuth

1. Go to Google Cloud Console
2. Update Authorized redirect URIs:
   - Add: `https://your-backend-url.railway.app/auth/google/callback`
3. Update Authorized JavaScript origins:
   - Add: `https://your-frontend-url.railway.app`

### Step 8: Custom Domain (Optional)

1. Buy domain from Namecheap/Cloudflare (~$12/year)
2. In Railway, go to your frontend service
3. Click "Settings" → "Domains"
4. Add custom domain: `bookclub.yourdomain.com`
5. Update DNS records as instructed
6. Railway automatically provisions SSL

### Step 9: Test Deployment

1. Visit your frontend URL
2. Test login flow
3. Create a test group
4. Verify all features work

**Total Time:** 15-20 minutes
**Total Cost:** ~$10/month

---

## Option 2: Render Deployment

**Cost:** ~$10/month
**Setup Time:** 20 minutes
**Difficulty:** Easy

### Step 1: Create Render Account

Go to https://render.com/ and sign up

### Step 2: Deploy Database

1. Click "New" → "PostgreSQL"
2. Name: `bookclub-db`
3. Region: Choose closest to your users
4. Plan: Free (for testing) or Starter $7/month
5. Click "Create Database"
6. Copy **Internal Database URL**

### Step 3: Deploy Backend

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Settings:
   - **Name**: `bookclub-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (same as Railway)
5. Click "Create Web Service"

### Step 4: Deploy Frontend

1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Settings:
   - **Name**: `bookclub-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add environment variables
5. Click "Create Static Site"

### Step 5: Update URLs

Update your backend `.env` with frontend URL and vice versa, then redeploy.

---

## Option 3: Manual VPS Deployment

**Cost:** $5-10/month (DigitalOcean/Linode)
**Setup Time:** 1-2 hours
**Difficulty:** Advanced

### Prerequisites
- Ubuntu 22.04 VPS
- Domain name
- SSH access

### Step 1: Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip python3-venv nodejs npm postgresql nginx certbot python3-certbot-nginx

# Create app user
adduser bookclub
usermod -aG sudo bookclub
su - bookclub
```

### Step 2: Setup PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE bookclub;
CREATE USER bookclub_user WITH PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE bookclub TO bookclub_user;
\q
```

### Step 3: Deploy Backend

```bash
cd /home/bookclub
git clone https://github.com/yourusername/bookclub-platform.git
cd bookclub-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add all your environment variables

# Run migrations
alembic upgrade head

# Test backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 4: Setup Systemd Service

```bash
sudo nano /etc/systemd/system/bookclub-backend.service
```

```ini
[Unit]
Description=BookClub Backend
After=network.target

[Service]
User=bookclub
WorkingDirectory=/home/bookclub/bookclub-platform/backend
Environment="PATH=/home/bookclub/bookclub-platform/backend/venv/bin"
ExecStart=/home/bookclub/bookclub-platform/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable bookclub-backend
sudo systemctl start bookclub-backend
sudo systemctl status bookclub-backend
```

### Step 5: Deploy Frontend

```bash
cd /home/bookclub/bookclub-platform/frontend

# Install dependencies
npm install

# Create .env
nano .env
# Add VITE_API_URL and VITE_GOOGLE_CLIENT_ID

# Build
npm run build

# Copy to web root
sudo mkdir -p /var/www/bookclub
sudo cp -r dist/* /var/www/bookclub/
sudo chown -R www-data:www-data /var/www/bookclub
```

### Step 6: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/bookclub
```

```nginx
# Backend
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /var/www/bookclub;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/bookclub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

### Step 8: Setup Automatic Backups

```bash
# Create backup script
nano /home/bookclub/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/bookclub/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U bookclub_user bookclub > $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
chmod +x /home/bookclub/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /home/bookclub/backup.sh
```

---

## Post-Deployment Checklist

### All Deployment Methods

- [ ] Backend is accessible at your domain
- [ ] Frontend loads correctly
- [ ] Can log in with Google
- [ ] Database migrations applied
- [ ] Environment variables set correctly
- [ ] SSL certificate active (HTTPS)
- [ ] Google OAuth redirect URIs updated
- [ ] CORS configured for production domain
- [ ] Error logging configured
- [ ] Backup system in place (for VPS)

### Test Full User Flow

1. Visit your production URL
2. Sign in with Google
3. Create a group
4. Copy invite code
5. Open incognito window
6. Join group with invite code
7. Add a book
8. Set progress
9. Post comment
10. Verify comment visibility works

### Monitoring

**Railway/Render:**
- Check service logs in dashboard
- Set up error alerts
- Monitor database usage

**VPS:**
```bash
# View backend logs
sudo journalctl -u bookclub-backend -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor system resources
htop
```

---

## Updating Your Deployment

### Railway/Render (Automatic)

1. Push changes to GitHub
   ```bash
   git add .
   git commit -m "Update feature X"
   git push
   ```
2. Railway/Render automatically deploys
3. Check logs to ensure successful deployment

### VPS (Manual)

```bash
ssh bookclub@your-server-ip

cd /home/bookclub/bookclub-platform

# Pull latest changes
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart bookclub-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/bookclub/
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
railway logs  # Railway
# or
sudo journalctl -u bookclub-backend -n 50  # VPS

# Common issues:
# - Missing environment variables
# - Database connection failed
# - Port already in use
```

### Frontend Shows Blank Page

```bash
# Check browser console for errors
# Common issues:
# - Wrong VITE_API_URL
# - CORS errors (check backend FRONTEND_URL)
# - Build failed
```

### Database Connection Failed

```bash
# Verify DATABASE_URL is correct
# Check database is running
# Verify firewall allows connection
```

### Google OAuth Fails

```bash
# Verify redirect URIs in Google Console match exactly
# Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
# Ensure cookies are enabled
```

---

## Scaling for Growth

### When You Outgrow Free/Starter Tiers

**Database Optimization:**
- Add indexes on frequently queried columns
- Enable connection pooling
- Consider read replicas

**Backend Scaling:**
- Increase dyno/instance size
- Add horizontal scaling (multiple instances)
- Implement caching (Redis)

**Frontend Optimization:**
- Enable CDN (Cloudflare)
- Implement lazy loading
- Optimize images

**Cost at Scale:**
- 100 users: $10-20/month
- 1000 users: $50-100/month
- 10000 users: $200-500/month

---

## Security Best Practices

1. **Never commit .env files**
2. **Rotate secrets regularly**
3. **Keep dependencies updated**
4. **Enable rate limiting** (implement in backend)
5. **Monitor for suspicious activity**
6. **Regular database backups**
7. **Use strong passwords**
8. **Enable 2FA on all accounts**

---

## Support

- **Railway:** https://docs.railway.app/
- **Render:** https://render.com/docs
- **Nginx:** https://nginx.org/en/docs/
- **PostgreSQL:** https://www.postgresql.org/docs/

---

**Deployment Status:** Once deployed, update STATUS.md with production URLs!
