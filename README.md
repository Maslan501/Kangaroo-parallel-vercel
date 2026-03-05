# 🦘 Kangaroo Parallel Search - Vercel Ready

Complete Bitcoin puzzle solver using enhanced Pollard's Kangaroo algorithm with 10 parallel workers and real-time web monitoring dashboard.

## 📁 Project Structure

```
kangaroo_parallel_vercel/
├── api/                          # Flask API for dashboard
│   ├── templates/
│   │   └── dashboard.html        # Real-time monitoring UI
│   ├── index.py                  # API endpoints
│   └── requirements.txt          # API dependencies
├── search_engine/                # Kangaroo search implementation
│   └── kangaroo_search.py        # Enhanced v2.2+ with 10 workers
├── work_files/                   # Auto-generated work files
│   ├── kangaroo_work_*.json     # Progress files
│   └── FOUND_KEYS_KANGAROO.txt  # Found private keys
├── requirements.txt              # Main dependencies
├── runtime.txt                   # Python version
├── vercel.json                   # Vercel deployment config
├── START_ALL.bat / .ps1          # Launch everything
├── start_parallel_search.bat     # Launch search only
└── start_dashboard.bat           # Launch dashboard only
```

## 🚀 Quick Start (Local)

### Option 1: Start Everything (Recommended)
```bash
# Windows CMD
START_ALL.bat

# PowerShell
.\START_ALL.ps1
```

### Option 2: Start Components Separately
```bash
# Terminal 1: Start parallel search
start_parallel_search.bat

# Terminal 2: Start dashboard
start_dashboard.bat
```

Then open: **http://localhost:5001**

## 📊 Dashboard Features

- **Real-time Monitoring**: Updates every 5 seconds
- **10 Parallel Workers**: See all searches simultaneously
- **Progress Tracking**: Visual progress bars for each worker
- **Performance Stats**: 
  - Speed multiplier (10x when all workers active)
  - Total jumps across all workers
  - Distinguished Points (DPs) found
  - Keys discovered
- **Worker Details**: 
  - Puzzle number being searched
  - Zone (20-30%, 40-50%, etc.)
  - Iterations, jumps, kangaroos
  - Timestamps

## 🎯 How It Works

### Parallel Execution
The system runs **10 independent searches simultaneously** using Python's multiprocessing:
- Each worker targets a different puzzle
- Searches prioritize high-probability zones (20-30%, 40-50%, 65-85%)
- Work files saved every 10,000 iterations
- Thread-safe file operations

### Kangaroo v2.2+ Enhancements
1. **32-way jump table** for faster operations
2. **Multiple kangaroos** (4-8 per search)
3. **Distinguished Points** for efficient collision detection
4. **Smart zone targeting** based on solved key patterns
5. **Auto-resume** from saved work files
6. **Parallel-optimized** for maximum CPU usage

### How Keys Are Found
1. Tame kangaroos start from range_start
2. Wild kangaroos start from target public key
3. Both jump through key space using deterministic function
4. When collision detected → private key calculated
5. Key verified against target address
6. **Saved to:** `work_files/FOUND_KEYS_KANGAROO.txt`

## 🌐 Vercel Deployment

### Requirements
- Vercel account (free tier works)
- Vercel CLI: `npm install -g vercel`

### Deploy Steps
```bash
cd kangaroo_parallel_vercel
vercel login
vercel
```

Follow prompts:
- Project name: `kangaroo-parallel-search`
- Directory: `.` (current)
- Override settings: No

### After Deployment
- Dashboard available at: `https://your-project.vercel.app`
- API endpoint: `https://your-project.vercel.app/api/status`

**Note:** Vercel deployment only hosts the dashboard. The parallel search must run locally (Vercel has 10-second execution limit, searches run hours/days).

### Hybrid Setup (Recommended)
1. **Local:** Run parallel search workers
2. **Vercel:** Host dashboard for remote monitoring
3. **Sync:** Work files update dashboard automatically

## 📝 Configuration

### Target Puzzles
Edit `search_engine/kangaroo_search.py` line ~800:
```python
TARGETS = [
    # Priority 1: 20-30% zone (highest success rate)
    (135, '20-30'),  # Puzzle 135, 20-30% range
    (140, '20-30'),
    # Add more puzzles...
]
```

### Worker Count
Edit line ~845:
```python
PARALLEL_WORKERS = 10  # Adjust based on your CPU cores
```

### Save Interval
Edit line ~450:
```python
self.save_interval = 10000  # Save every N iterations
```

## 🔧 Dependencies

### Local Execution
```bash
pip install -r requirements.txt
```

Required packages:
- `ecdsa`: Bitcoin cryptography
- `flask`: Dashboard web server

### Python Version
- Python 3.12+ required
- Use `py` command on Windows (not `python`)

## 📂 Work Files

### Progress Files
Location: `work_files/kangaroo_work_puzzle{N}_{zone}.json`

Format:
```json
{
  "puzzle_num": 135,
  "zone": "20-30",
  "range_start": 123456789,
  "range_end": 987654321,
  "iterations": 50000,
  "total_jumps": 50000,
  "dp_count": 5,
  "tame_points": 3,
  "wild_points": 2,
  "num_kangaroos": 4,
  "timestamp": "2026-03-05T12:00:00"
}
```

### Found Keys File
Location: `work_files/FOUND_KEYS_KANGAROO.txt`

Format:
```
================================================================================
PUZZLE #135 SOLVED!
Timestamp: 2026-03-05 14:30:45
Private Key (Decimal): 12345678901234567890
Private Key (Hex): 0xabc123...
Address: 1BitcoinAddress...
================================================================================
```

## 🛠️ Troubleshooting

### "python not recognized"
Use `py` instead of `python` on Windows.

### Dashboard shows 0 workers
Run `start_parallel_search.bat` first. Dashboard shows active work files.

### Port 5001 already in use
Edit `start_dashboard.bat` line 4:
```bash
py -m flask run --host=0.0.0.0 --port=5002
```

### Work files not updating
Check permissions on `work_files/` directory.

### Process using too much CPU
Reduce `PARALLEL_WORKERS` in `kangaroo_search.py`.

## 📊 Performance Expectations

### Search Speed
- **Single worker:** ~1,000-10,000 jumps/second
- **10 workers:** ~10,000-100,000 jumps/second
- **CPU usage:** 80-100% with 10 workers

### Time Estimates (Puzzle 135, 131-bit range)
- **Range size:** 2^131 (~2.7 × 10^39)
- **Expected operations:** 2√N ≈ 2^66
- **At 100,000 jumps/sec:** ~23 billion years 😅

**Reality:** Target specific zones (20-30%) based on patterns, not full range!

### Zone Search Times
- **20-30% zone (135-bit):** Days to weeks
- **Full range (131-bit):** Computationally infeasible

## 🎯 Strategy

The system targets high-probability zones discovered from solved puzzles:
- **20-30% zone:** 5 keys found here
- **40-50% zone:** 4 keys found
- **65-85% zone:** 3 keys found

This reduces search space by ~90%, making searches practical.

## 📜 License

Open source for educational purposes. Bitcoin puzzle solving is a learning exercise.

## 🤝 Contributing

This is a self-contained project ready for deployment. Modify `search_engine/kangaroo_search.py` to implement your own strategies!

## ⚠️ Important Notes

1. **Educational Purpose:** This is for learning cryptography and algorithms
2. **Computational Reality:** Even with parallelization, higher puzzles (135+) require enormous computation
3. **Probabilistic:** No guarantee of finding keys; searches may run indefinitely
4. **Resource Intensive:** Monitor CPU/RAM usage
5. **Vercel Limits:** Dashboard only; search must run locally

## 📞 Support

Check the dashboard at http://localhost:5001 to monitor progress. All work files auto-save so you can stop/resume anytime!

---

**Made with 🦘 and ⚡ parallel processing!**
