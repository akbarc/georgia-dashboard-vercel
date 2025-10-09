# 🚀 Deploy Backend to Railway

Your repo now has:
- **Frontend** → Vercel (already deployed) ✅
- **Backend** → Railway (deploy now)

## Quick Deploy (3 Steps)

### 1. Push to GitHub

```bash
cd /Users/akbarchranya/georgia-dashboard-vercel
git add .
git commit -m "Add backend for Railway deployment"
git push
```

### 2. Deploy Backend to Railway

1. Go to: **https://railway.app**
2. Click "**New Project**"
3. Select "**Deploy from GitHub repo**"
4. Choose: `georgia-dashboard-vercel`
5. **IMPORTANT**: Set Root Directory to: `backend`
6. Click "**Deploy**"

### 3. Add Tailscale & Environment Variables

**Add Tailscale:**
- In Railway project → "**New**" → "**Service**"
- Search for "**Tailscale**"
- Set `TAILSCALE_AUTHKEY` from https://login.tailscale.com/admin/settings/keys

**Set Environment Variables:**
In Railway → Your backend service → Variables:
```
DB_SERVER=10.1.10.105
DB_PORT=1433
DB_USERNAME=amchranya
DB_PASSWORD=2000Akbar!
DB_DATABASE=GAWDB
```

## Test Your Backend

Railway will give you a URL like:
`https://georgia-dashboard-vercel-backend.railway.app`

Visit:
- `/health` - Should show database connected
- `/api/test` - Should return success
- `/api/executive-summary` - Should return dashboard data

## Update Frontend to Use Backend

Once backend is deployed, update your Vercel site:

In `test.html` and `dashboard.html`, change:
```javascript
const API_BASE = 'https://your-railway-url.railway.app';
```

Push to GitHub, Vercel auto-deploys!

---

## Architecture

```
USER
 ↓
VERCEL (Frontend)
 ↓ API calls
RAILWAY (Backend with Tailscale)
 ↓ Tailscale VPN
SQL SERVER (10.1.10.105)
```

**Perfect separation:** Frontend globally accessible, backend securely connects to database!
