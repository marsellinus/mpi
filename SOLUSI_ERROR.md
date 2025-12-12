# ✅ SOLUSI: MS-MPI Bootstrap Queue Error di Windows

## 🔴 Masalah yang Terjadi

Error yang Anda alami:
```
Fatal error in MPI_Send: Other MPI error, error stack:
failed to attach to a bootstrap queue
```

**Penyebab**: MS-MPI di Windows memiliki keterbatasan dalam menangani banyak MPI processes yang masing-masing menggunakan multiple multiprocessing workers.

---

## ✅ Solusi yang Berhasil

### Konfigurasi yang BERHASIL ✓

| MPI Processes | Workers | Status | Waktu Eksekusi |
|---------------|---------|--------|----------------|
| 2             | 4       | ✅ BERHASIL | ~2.9s |
| 4             | 1       | ✅ BERHASIL | ~0.09s |
| 8             | 1       | ✅ Seharusnya berhasil | - |

### Konfigurasi yang GAGAL ✗

| MPI Processes | Workers | Status |
|---------------|---------|--------|
| 4             | 4       | ❌ GAGAL (bootstrap queue error) |
| 8             | 4       | ❌ GAGAL (bootstrap queue error) |
| 16            | 4       | ❌ GAGAL (bootstrap queue error) |

---

## 🚀 Cara Menjalankan (yang BENAR)

### Option 1: Gunakan Benchmark Script (RECOMMENDED)


```powershell
# Script otomatis menyesuaikan jumlah workers
.\scripts\run_benchmark.ps1
```

Script ini akan otomatis:
- **2 processes** → 4 workers (hybrid optimal)
- **4+ processes** → 1 worker (MPI-dominant, stabil)

### Option 2: Manual Execution

#### Untuk 2-4 Proses (Testing)
```powershell
# 2 proses dengan 4 workers (optimal untuk development)
mpiexec -n 2 python src\matrix_row_striping.py --N 1024 --workers 4

# 4 proses dengan 1 worker (stabil)
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1
```

#### Untuk 8+ Proses (Production)
```powershell
# Gunakan workers=1 untuk stabilitas
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 8 python src\matrix_block_striping.py --N 1024 --workers 1
```

---

## 📊 Hasil dari Konfigurasi yang Berhasil

Dari test Anda yang berhasil (2 processes, 4 workers):

**Row Striping:**
- Total Time: 2.87s
- Compute Time: 2.69s (93.82%)
- Communication: 0.22s (7.71%)

**Block Striping:**
- Total Time: 3.06s
- Compute Time: 2.90s (94.86%)
- Communication: 0.18s (5.97%)

**Kesimpulan**: Block striping memiliki overhead komunikasi yang lebih rendah!

---

## 🎯 Benchmark Lengkap yang Direkomendasikan

Jalankan ini untuk mendapatkan data lengkap:

```powershell
# Clear hasil sebelumnya
Remove-Item results\*.csv -ErrorAction SilentlyContinue

# Test dengan berbagai konfigurasi
# 2 proses, 4 workers (hybrid optimal)
mpiexec -n 2 python src\matrix_row_striping.py --N 1024 --workers 4
mpiexec -n 2 python src\matrix_block_striping.py --N 1024 --workers 4

# 4 proses, 1 worker (stabil)
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 4 python src\matrix_block_striping.py --N 1024 --workers 1

# 8 proses, 1 worker (scaling test)
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 8 python src\matrix_block_striping.py --N 1024 --workers 1

# Generate plots
python plot_results.py
```

---

## 📈 Visualisasi Hasil

Setelah benchmark selesai, jalankan:

```powershell
python plot_results.py
```

Ini akan menghasilkan:
1. `total_time_comparison.png` - Perbandingan waktu total
2. `compute_vs_communication.png` - Breakdown compute vs komunikasi
3. `communication_breakdown.png` - Detail scatter/broadcast/gather
4. `speedup_analysis.png` - Analisis speedup
5. `efficiency_analysis.png` - Efisiensi paralel
6. `time_percentage.png` - Distribusi waktu
7. `summary_table.txt` - Ringkasan dalam teks

---

## 💡 Penjelasan: Kenapa Workers=1 Berhasil?

### Dengan Workers=1 (Pure MPI-Dominant)
```
Total Processes = MPI_Processes × 1 worker = 4 × 1 = 4 processes
✅ Windows dapat handle dengan baik
```

### Dengan Workers=4 (Hybrid)
```
Total Processes = MPI_Processes × 4 workers = 4 × 4 = 16 processes
❌ Terlalu banyak untuk MS-MPI bootstrap queue di Windows
```

**MS-MPI di Windows** memiliki batasan internal pada jumlah concurrent processes yang dapat di-manage secara bersamaan.

---

## 🔧 Alternatif untuk Scaling Lebih Baik

### Option A: Gunakan WSL2 (Windows Subsystem for Linux)

```bash
# Install di WSL2 Ubuntu
sudo apt update
sudo apt install -y openmpi-bin python3-pip
pip3 install -r requirements.txt

# Jalankan dengan OpenMPI (lebih stabil untuk banyak proses)
mpirun -np 16 python3 src/matrix_row_striping.py --N 2048 --workers 4
```

### Option B: Gunakan Matrix yang Lebih Besar

```powershell
# Matrix besar = lebih banyak compute, less overhead
mpiexec -n 8 python src\matrix_row_striping.py --N 2048 --workers 1
mpiexec -n 8 python src\matrix_row_striping.py --N 4096 --workers 1
```

### Option C: Fokus pada Pure MPI

```powershell
# Disable multiprocessing completely, pure MPI
mpiexec -n 16 python src\matrix_row_striping.py --N 2048 --workers 1
```

---

## 📝 Ringkasan Quick Commands

### ✅ Perintah yang AMAN untuk Windows

```powershell
# Quick test (2 proses)
mpiexec -n 2 python src\matrix_row_striping.py --N 1024 --workers 4

# Balanced (4 proses)
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1

# Scaling test (8 proses)
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1

# Full benchmark (auto-adjusted workers)
.\scripts\run_benchmark.ps1

# Visualisasi
python plot_results.py
```

### ❌ Perintah yang TIDAK AMAN (akan error)

```powershell
# JANGAN jalankan ini di Windows!
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 4
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 4
.\scripts\run_benchmark.ps1  # (menggunakan workers=4 untuk semua)
```

---

## 🎓 Lesson Learned

1. **MS-MPI di Windows** memiliki keterbatasan untuk hybrid parallelism
2. **Rule of thumb**: 
   - ≤ 2 MPI processes: gunakan 2-4 workers
   - \> 2 MPI processes: gunakan 1 worker
3. **Untuk scaling serius** (>8 processes): gunakan Linux/WSL2/HPC
4. **Trade-off**: Workers=1 lebih stabil, tapi kurang optimal untuk per-process computation

---

## ✅ Next Steps

1. **Jalankan benchmark**:
   ```powershell
   .\scripts\run_benchmark.ps1
   ```

2. **Generate visualisasi**:
   ```powershell
   python plot_results.py
   ```

3. **Lihat hasil**:
   - Check `results\*.csv` untuk data
   - Check `results\*.png` untuk grafik
   - Check `results\summary_table.txt` untuk ringkasan

4. **Untuk eksperimen lebih lanjut**:
   - Test dengan matrix size berbeda (2048, 4096)
   - Bandingkan row vs block striping
   - Analisis scaling efficiency

---

**Selamat mencoba! 🚀**
