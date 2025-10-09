# Railway Deployment Info

**Project ID:** `aee039b0-ece2-4327-86b9-63de3cad93b9`

**Status:** ✅ Connected to GitHub and Vercel

---

## Get Your Railway Backend URL

### Option 1: Railway Dashboard
1. Go to: https://railway.app/project/aee039b0-ece2-4327-86b9-63de3cad93b9
2. Click on your **backend** service (not tailscale-vpn)
3. Go to **Settings** → **Domains**
4. Copy the public URL (looks like: `https://georgia-xxx.railway.app`)

### Option 2: Railway CLI
```bash
railway status --project aee039b0-ece2-4327-86b9-63de3cad93b9
```

---

## Test Endpoints

Once you have the URL, test:

```bash
# Replace YOUR-URL with actual Railway URL

# Test 1: API is running
curl https://YOUR-URL.railway.app/api/test

# Test 2: Database connectivity through Tailscale
curl https://YOUR-URL.railway.app/health

# Test 3: Full dashboard data
curl https://YOUR-URL.railway.app/api/executive-summary
```

---

## Services in This Project

1. **backend** - Flask API with pymssql
   - Connects to SQL Server via Tailscale
   - Endpoints: `/health`, `/api/test`, `/api/executive-summary`

2. **tailscale-vpn** - Tailscale VPN client
   - Provides secure connection to on-premise network
   - Advertises routes from Windows desktop (10.1.10.0/24)

---

## Direct Link

**Open Project:** https://railway.app/project/aee039b0-ece2-4327-86b9-63de3cad93b9
