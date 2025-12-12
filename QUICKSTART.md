# Quick Start Guide

## 🚀 Fast Setup and Execution

### 1. Install Dependencies (One-Time Setup)

#### Windows
```powershell
# Install Python packages
pip install -r requirements.txt

# Verify MPI installation
mpiexec --version
```

#### Linux/Mac
```bash
# Install Python packages
pip install -r requirements.txt

# Verify MPI installation
mpirun --version
```

---

### 2. Run Quick Test (1024×1024 matrix)

#### Windows
```powershell
# Test row striping
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 2

# Test block striping
mpiexec -n 4 python src\matrix_block_striping.py --N 1024 --workers 2
```

#### Linux/Mac
```bash
# Test row striping
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2

# Test block striping
mpirun -np 4 python3 src/matrix_block_striping.py --N 1024 --workers 2
```

---

### 3. Run Full Benchmark

#### Windows
```powershell
# Auto-adjusts workers for Windows stability
.\scripts\run_benchmark.ps1
```

#### Linux/Mac
```bash
bash scripts/run_benchmark.sh
```

---

### 4. Generate Plots

```bash
python plot_results.py
```

Results will be saved in `results/` directory.

---

## 📋 Configuration Options

Edit benchmark scripts to customize:

- **Matrix Size**: Change `MATRIX_SIZE` (default: 1024)
- **Workers**: Change `WORKERS` (default: 4)
- **Process Counts**: Modify `PROCESS_COUNTS` array

---

## 🎯 Expected Execution Time

| Matrix Size | Processes | Workers | Approx. Time |
|-------------|-----------|---------|--------------|
| 1024        | 4         | 2       | ~2-3 seconds |
| 1024        | 4         | 4       | ~1-2 seconds |
| 2048        | 8         | 4       | ~5-8 seconds |
| 4096        | 16        | 4       | ~30-60 sec   |

*Times vary based on hardware*

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] MPI installed (MS-MPI for Windows, OpenMPI for Linux/Mac)
- [ ] All packages from requirements.txt installed
- [ ] Can run single test successfully
- [ ] Benchmark script executes without errors
- [ ] CSV files generated in results/
- [ ] Plots generated successfully

---

## 🐛 Quick Troubleshooting

**Issue**: "mpiexec not found"
**Fix**: Install MS-MPI from Microsoft website (Windows)

**Issue**: "No module named 'mpi4py'"
**Fix**: `pip install mpi4py`

**Issue**: Out of memory
**Fix**: Use smaller matrix size `--N 512`

---

For detailed documentation, see [README.md](README.md)
