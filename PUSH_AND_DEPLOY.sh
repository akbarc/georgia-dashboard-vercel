#!/bin/bash

echo "🚀 Georgia Dashboard - GitHub Push & Vercel Deploy"
echo "=================================================="
echo ""

# Navigate to directory
cd /Users/akbarchranya/georgia-dashboard-vercel

echo "✅ In directory: $(pwd)"
echo ""

# Add git remote
echo "📝 Adding GitHub remote..."
git remote add origin https://github.com/akbarc/georgia-dashboard-vercel.git 2>/dev/null || echo "Remote already exists"

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Now opening Vercel deployment..."
    sleep 2
    open "https://vercel.com/new/clone?repository-url=https://github.com/akbarc/georgia-dashboard-vercel"
    echo ""
    echo "📋 In Vercel:"
    echo "   1. Click 'Import'"
    echo "   2. Click 'Deploy'"
    echo ""
    echo "⏱️  Deployment takes ~60 seconds"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "❌ Push failed. Make sure you created the GitHub repo!"
    echo ""
fi
