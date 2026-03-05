# 🚀 Quick Vercel Deployment Guide

## Prerequisites
```bash
npm install -g vercel
```

## Deploy in 3 Steps

### 1. Login to Vercel
```bash
vercel login
```

### 2. Deploy
```bash
cd kangaroo_parallel_vercel
vercel
```

Answer prompts:
- **Set up and deploy?** Yes
- **Link to existing project?** No
- **Project name:** kangaroo-parallel-search (or your choice)
- **Directory:** . (current directory)
- **Override settings?** No

### 3. Access Dashboard
After deployment completes:
```
✅ Production: https://kangaroo-parallel-search.vercel.app
```

## Important Notes

### What Gets Deployed
- ✅ Dashboard UI (real-time monitoring)
- ✅ API endpoints (/api/status, /health)
- ✅ Static HTML/CSS/JavaScript

### What Stays Local
- ❌ Parallel search workers (Vercel has 10s execution limit)
- ❌ Long-running computations
- ❌ Heavy CPU operations

## Hybrid Setup (Recommended)

### Option A: Dashboard Only (Simple)
1. Deploy to Vercel → Get dashboard URL
2. Run search workers locally
3. Work files stay local only
4. Good for: Personal monitoring

### Option B: Synced Monitoring (Advanced)
1. Deploy to Vercel → Get dashboard URL
2. Run search workers locally
3. Upload work files to cloud storage (S3/Dropbox/etc)
4. Configure dashboard to read from cloud
5. Good for: Remote monitoring

### Option C: Local Only (Full Control)
1. Skip Vercel entirely
2. Run `START_ALL.bat` locally
3. Access: http://localhost:5001
4. Good for: Testing, development

## Update Deployment

After making changes:
```bash
vercel --prod
```

## Environment Variables (if needed)

Set in Vercel dashboard:
1. Go to project settings
2. Environment Variables
3. Add:
   - `WORK_FILES_PATH` = `/tmp/work_files` (if using cloud storage)
   - `CLOUD_STORAGE_URL` = your storage URL

## Monitoring Deployed Dashboard

### Check if it's working
```bash
curl https://your-project.vercel.app/api/status
```

Expected response:
```json
{
  "active_searches": 0,
  "total_jumps": 0,
  "found_keys": 0,
  "searches": [],
  "timestamp": "2026-03-05T12:00:00"
}
```

### View logs
```bash
vercel logs
```

## Troubleshooting

### "No work files found"
- Normal for fresh deployment
- Run search workers locally to generate work files
- If using cloud sync, check storage connection

### "500 Internal Server Error"
```bash
vercel logs  # Check error details
```

Common causes:
- Missing dependencies in requirements.txt
- Path issues in index.py
- Python version mismatch

### "Dashboard not updating"
- Work files directory is local only by default
- Deploy only shows dashboard; searches run locally
- Consider cloud storage sync for remote monitoring

## Production Checklist

Before deploying:
- [ ] Test locally first: `START_ALL.bat`
- [ ] Verify dashboard loads: http://localhost:5001
- [ ] Check API response: http://localhost:5001/api/status
- [ ] Ensure requirements.txt is complete
- [ ] Verify vercel.json routes are correct
- [ ] Test with sample work files

## Cost

**Free tier includes:**
- Unlimited deployments
- 100GB bandwidth/month
- Serverless function execution
- Custom domains

Perfect for this dashboard! 🎉

## Next Steps

After successful deployment:
1. Test dashboard URL
2. Run local search workers
3. See searches appear in dashboard (if using cloud sync)
4. Share URL for remote monitoring

---

**Need help?** Check main README.md for full documentation.
