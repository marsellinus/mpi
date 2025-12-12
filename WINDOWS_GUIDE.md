# Panduan Khusus Windows

## Masalah Umum MS-MPI di Windows

### Error: "failed to attach to a bootstrap queue"

**Penyebab**: 
- MS-MPI memiliki keterbatasan dalam menangani banyak proses yang masing-masing menggunakan multiprocessing
- Konflik resource antara MPI processes dan multiprocessing workers
- Batasan sistem Windows dalam handle concurrent processes

**Solusi**:

### 1. Kurangi Jumlah Workers (RECOMMENDED)

Gunakan 1-2 workers per MPI process:

```powershell
# Untuk 4+ MPI processes, gunakan 1-2 workers
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1
```

### 2. Kurangi Jumlah MPI Processes

Test dengan jumlah proses yang lebih sedikit:

```powershell
# Test dengan 2-4 proses saja
mpiexec -n 2 python src\matrix_row_striping.py --N 1024 --workers 4
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 2
```

### 3. Gunakan Matrix Size yang Lebih Besar

Untuk proses banyak, gunakan matrix yang lebih besar:

```powershell
# Matrix besar mengurangi overhead komunikasi
mpiexec -n 8 python src\matrix_row_striping.py --N 2048 --workers 1
```

### 4. Set Environment Variables

Tambahkan environment variable MS-MPI:

```powershell
# PowerShell
$env:MSMPI_DISABLE_SHM = "1"
$env:MSMPI_PRECONNECT = "1"

# Kemudian jalankan
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 2
```

### 5. Jalankan Tanpa Multiprocessing

Set workers ke 1 untuk pure MPI:

```powershell
# Pure MPI tanpa multiprocessing
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 16 python src\matrix_row_striping.py --N 2048 --workers 1
```

---

## Konfigurasi Optimal untuk Windows

### Untuk Testing (Matrix 1024×1024)

| MPI Processes | Workers | Status | Keterangan |
|---------------|---------|--------|------------|
| 2             | 4       | ✅ Stabil | Ideal untuk development |
| 4             | 2       | ✅ Stabil | Good balance |
| 4             | 1       | ✅ Stabil | Pure MPI |
| 8             | 1       | ⚠️ Coba | Minimal workers |
| 16            | 1       | ⚠️ Coba | Hanya jika perlu |

### Untuk Benchmark Serius (Matrix 2048×2048 atau lebih)

```powershell
# Recommended configuration
$MATRIX_SIZE = 2048
$WORKERS = 1
$PROCESS_COUNTS = @(2, 4, 6, 8)

# Edit run_benchmark.ps1 dengan konfigurasi di atas
```

---

## Modified Benchmark Script untuk Windows

Buat file `run_benchmark_windows_safe.ps1`:

```powershell
# Safe benchmark configuration for Windows
$MATRIX_SIZE = 1024
$PROCESS_COUNTS = @(2, 4)  # Reduced for stability

Write-Host "Windows-Safe Benchmark Runner" -ForegroundColor Green
Write-Host "Matrix Size: $MATRIX_SIZE" -ForegroundColor Cyan

# Create results directory
if (-not (Test-Path "results")) {
    New-Item -ItemType Directory -Path "results" | Out-Null
}

# Clear previous results
if (Test-Path "results\row_results.csv") { Remove-Item "results\row_results.csv" }
if (Test-Path "results\block_results.csv") { Remove-Item "results\block_results.csv" }

foreach ($P in $PROCESS_COUNTS) {
    # Calculate safe worker count: more processes = fewer workers
    if ($P -le 2) {
        $WORKERS = 4
    } elseif ($P -le 4) {
        $WORKERS = 2
    } else {
        $WORKERS = 1
    }
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Testing: $P processes, $WORKERS workers" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Green
    
    # Row Striping
    Write-Host "`n[Row Striping]" -ForegroundColor Blue
    mpiexec -n $P python src\matrix_row_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    Start-Sleep -Seconds 2
    
    # Block Striping
    Write-Host "`n[Block Striping]" -ForegroundColor Blue
    mpiexec -n $P python src\matrix_block_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    Start-Sleep -Seconds 2
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Benchmark Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
```

---

## Quick Test Commands

### Test 1: Verify Installation (2 processes, safe)
```powershell
mpiexec -n 2 python src\matrix_row_striping.py --N 512 --workers 2
```

### Test 2: Production Run (4 processes)
```powershell
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1
```

### Test 3: Large Matrix (minimal processes)
```powershell
mpiexec -n 2 python src\matrix_row_striping.py --N 2048 --workers 2
```

---

## Alternatif: Gunakan WSL2 (Windows Subsystem for Linux)

Jika masalah terus berlanjut, pertimbangkan menggunakan WSL2:

```bash
# Di WSL2 Ubuntu
sudo apt-get update
sudo apt-get install -y openmpi-bin python3-pip
pip3 install -r requirements.txt

# Run dengan OpenMPI (lebih stabil)
mpirun -np 8 python3 src/matrix_row_striping.py --N 1024 --workers 4
```

---

## Performance Notes

**MS-MPI Limitations**:
- Optimal untuk 2-4 processes dengan multiprocessing
- Untuk > 4 processes, gunakan workers=1 atau WSL2
- Hybrid parallelism bekerja lebih baik di Linux/Mac

**Recommended Approach**:
1. Development: 2-4 processes, 2-4 workers
2. Testing: 4 processes, 1-2 workers  
3. Production: Gunakan Linux/HPC cluster untuk scaling > 8 processes

---

## Troubleshooting Checklist

- [ ] MS-MPI terinstal dengan benar (runtime + SDK)
- [ ] Python packages terinstal (`pip install -r requirements.txt`)
- [ ] Gunakan workers ≤ 2 untuk processes ≥ 4
- [ ] Test dengan matrix kecil (512 atau 1024) terlebih dahulu
- [ ] Pastikan tidak ada proses Python lain yang berjalan
- [ ] Restart terminal setelah mengubah environment variables
- [ ] Pertimbangkan WSL2 untuk scaling yang lebih baik

---

## Hasil Test Anda

Dari output Anda:
- ✅ **2 processes berhasil** - konfigurasi ini stabil
- ❌ **4+ processes gagal** - MS-MPI bootstrap queue error

**Rekomendasi**:
```powershell
# Jalankan ulang dengan konfigurasi aman
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 1
mpiexec -n 8 python src\matrix_row_striping.py --N 1024 --workers 1
```

Atau edit `scripts\run_benchmark.ps1` dan ubah:
```powershell
$WORKERS = 1  # Ubah dari 4 ke 1
```

---

**Kesimpulan**: Untuk Windows dengan MS-MPI, gunakan **workers=1** atau maksimal **workers=2** ketika menggunakan 4+ MPI processes.
