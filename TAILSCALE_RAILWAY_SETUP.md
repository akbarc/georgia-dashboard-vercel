# 🔐 Add Tailscale to Railway - Step by Step

## Prerequisites

✅ Backend deployed to Railway
✅ Windows desktop running Tailscale (advertises 10.1.10.0/24)

---

## Step 1: Get Tailscale Auth Key

1. **Go to:** https://login.tailscale.com/admin/settings/keys

2. **Click "Generate auth key"**

3. **Configure the key:**
   - ✅ Check "**Reusable**" (so Railway can restart)
   - ✅ Check "**Ephemeral**" (cleans up when Railway stops)
   - Description: "Railway Backend"
   - Tags: (leave empty)
   - Expiration: 90 days (or longer)

4. **Click "Generate key"**

5. **Copy the key** - looks like: `tskey-auth-xxxxxxxxxxxxx`
   - Save it somewhere, you'll need it in Step 2

---

## Step 2: Add Tailscale to Railway Project

### Option A: Add as Environment Variable (Simplest)

1. **In Railway dashboard:**
   - Go to your backend service
   - Click "**Variables**" tab
   - Click "**+ New Variable**"

2. **Add variable:**
   - Key: `TAILSCALE_AUTHKEY`
   - Value: `tskey-auth-xxxxxxxxxxxxx` (paste your key)
   - Click "**Add**"

3. **Deploy with Tailscale:**

   Update `backend/app.py` startup to include Tailscale:

   ```python
   # Add at the very top of app.py
   import subprocess
   import os

   # Start Tailscale if auth key exists
   if os.environ.get('TAILSCALE_AUTHKEY'):
       try:
           subprocess.run(['tailscale', 'up', '--authkey', os.environ['TAILSCALE_AUTHKEY']],
                         check=True, timeout=30)
           print("✅ Connected to Tailscale")
       except Exception as e:
           print(f"⚠️ Tailscale connection failed: {e}")
   ```

### Option B: Use Railway Tailscale Template (Recommended)

1. **In your Railway project, click "New" (top right)**

2. **Search for "Tailscale"** in the template search

3. **Click "Deploy" on the Tailscale template**

4. **Configure Tailscale service:**
   - It will ask for `TAILSCALE_AUTHKEY`
   - Paste your key from Step 1
   - Click "Deploy"

5. **Wait for Tailscale to connect** (~30 seconds)
   - Check logs, should see: "Connected to Tailscale"

---

## Step 3: Verify Tailscale Connection

### Check Railway Logs:

1. **Go to Tailscale service in Railway**
2. **Click "Deployments"**
3. **Click latest deployment**
4. **View logs** - should see:
   ```
   Starting Tailscale...
   Connected to Tailscale network
   IP: 100.x.x.x
   ```

### Check Tailscale Admin Console:

1. **Go to:** https://login.tailscale.com/admin/machines
2. **Find your Railway machine** - should show as online
3. **Note its Tailscale IP** (100.x.x.x)

---

## Step 4: Test Backend Connection to SQL Server

1. **In Railway dashboard, go to your backend service**

2. **Click "Settings" → "Domains"**

3. **Copy your Railway URL** (e.g., `https://georgia-xxx.railway.app`)

4. **Test the health endpoint:**
   ```bash
   curl https://your-railway-url.railway.app/health
   ```

5. **Should return:**
   ```json
   {
     "status": "healthy",
     "database": {
       "connected": true,
       "database": "GAWDB"
     }
   }
   ```

---

## Troubleshooting

### "Tailscale not connecting"

**Check Windows Desktop:**
```bash
# On Windows, verify subnet routing is enabled
tailscale status
```

Should show:
```
# Subnets advertised: 10.1.10.0/24
```

**If not, run:**
```cmd
tailscale up --advertise-routes=10.1.10.0/24
```

Then approve in Tailscale admin console.

### "Database connection timeout"

**Check Tailscale routes are approved:**
1. Go to: https://login.tailscale.com/admin/machines
2. Find Windows desktop machine
3. Click "..." → "Edit route settings"
4. Ensure `10.1.10.0/24` is **Approved** (green checkmark)

### "Auth key expired"

Generate a new key with longer expiration:
1. Go to: https://login.tailscale.com/admin/settings/keys
2. Generate new key with 90 days
3. Update `TAILSCALE_AUTHKEY` in Railway
4. Redeploy

---

## Architecture After Setup

```
RAILWAY BACKEND (with Tailscale)
Tailscale IP: 100.x.x.x
        ↓
   Tailscale Network (encrypted)
        ↓
WINDOWS DESKTOP (Subnet Router)
Tailscale IP: 100.84.221.9
Advertises: 10.1.10.0/24
        ↓
SQL SERVER
Local IP: 10.1.10.105:1433
```

---

## ✅ Success Checklist

- [ ] Tailscale auth key generated
- [ ] Auth key added to Railway environment variables
- [ ] Tailscale service deployed on Railway
- [ ] Railway machine shows in Tailscale admin console
- [ ] Windows desktop has subnet routing enabled
- [ ] Routes approved in Tailscale admin
- [ ] `/health` endpoint returns `"connected": true`

---

## Next Steps

Once Tailscale is working:
1. ✅ Backend can reach SQL Server at 10.1.10.105
2. ✅ Update Vercel frontend to use Railway backend URL
3. ✅ Test full stack deployment

**Total setup time: ~5 minutes**
