# 🎯 Quick Reference Card

## Start Everything
```bash
START_ALL.bat          # Windows CMD
.\START_ALL.ps1        # PowerShell
```

## Access Dashboard
**http://localhost:5001**

## Project Files
```
📁 kangaroo_parallel_vercel/
├── 🚀 START_ALL.bat/.ps1         → Launch everything
├── 🔍 search_engine/            → 10 parallel workers
├── 📊 api/                       → Dashboard & API
├── 💾 work_files/                → Auto-generated saves
├── 📝 README.md                  → Full documentation
├── 🌐 VERCEL_DEPLOY.md          → Deployment guide
├── ⚙️ vercel.json                → Deployment config
└── 📦 requirements.txt           → Dependencies
```

## Quick Commands

### Local Testing
```bash
# Start search only
start_parallel_search.bat

# Start dashboard only
start_dashboard.bat

# View work files
dir work_files\*.json
```

### Deployment
```bash
cd kangaroo_parallel_vercel
vercel login
vercel
```

## Key Locations

### Found Keys
`work_files/FOUND_KEYS_KANGAROO.txt`

### Work Progress
`work_files/kangaroo_work_puzzle{N}_{zone}.json`

### Dashboard API
`http://localhost:5001/api/status`

## Configuration

### Edit Targets
`search_engine/kangaroo_search.py` line ~800

### Change Workers
`search_engine/kangaroo_search.py` line ~845

### Change Port
`start_dashboard.bat` line 4

## Monitor Progress

- **Dashboard:** http://localhost:5001
- **Console:** See search window
- **Files:** Check work_files/ directory
- **API:** GET http://localhost:5001/api/status

## Stop Everything

1. Close search window
2. Close dashboard window
3. Or: Ctrl+C in each terminal

Work files auto-save every 10,000 iterations!

---

**Ready to search?** Run `START_ALL.bat` 🚀
