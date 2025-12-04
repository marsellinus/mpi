# Perkalian Matriks Paralel Hybrid
## Analisis Komparatif: Row Striping vs Block Striping

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MPI](https://img.shields.io/badge/MPI-mpi4py-green.svg)](https://mpi4py.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Analisis komparatif komprehensif tentang **perkalian matriks paralel hybrid** menggunakan **MPI (Message Passing Interface)** dan **Python multiprocessing**. Proyek ini mengimplementasikan dan membandingkan dua strategi distribusi data:

1. **Row Striping** - Mendistribusikan baris matriks A ke seluruh proses
2. **Block Striping** - Mendistribusikan blok matriks A menggunakan grid proses 2D

---

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Struktur Proyek](#-struktur-proyek)
- [Kebutuhan Sistem](#-kebutuhan-sistem)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Metodologi](#-metodologi)
- [Metrik Waktu](#-metrik-waktu)
- [Benchmarking](#-benchmarking)
- [Visualisasi Hasil](#-visualisasi-hasil)
- [Contoh Output](#-contoh-output)
- [Simulasi Kegagalan](#-simulasi-kegagalan)
- [Analisis Performa](#-analisis-performa)

---

## ✨ Fitur

- **Paralelisme Hybrid**: Menggabungkan paralelisme distributed-memory (MPI) dan shared-memory (multiprocessing)
- **Dua Strategi Distribusi**: 
  - Row striping untuk distribusi baris yang detail
  - Block striping dengan optimasi grid proses 2D
- **Pengukuran Waktu Komprehensif**: Mengukur waktu scatter, broadcast, compute, gather, dan total eksekusi
- **Benchmarking Otomatis**: Skrip untuk menguji berbagai jumlah proses
- **Visualisasi Lengkap**: Menghasilkan 6+ plot komparatif dan tabel ringkasan
- **Simulasi Kegagalan**: Testing kegagalan node opsional untuk analisis fault tolerance
- **Skalabel**: Mendukung ukuran matriks dari 1024×1024 hingga 4096×4096 dan lebih besar

---

## 📁 Struktur Proyek

```
project/
├── src/
│   ├── matrix_row_striping.py      # Implementasi row striping
│   ├── matrix_block_striping.py    # Implementasi block striping
│   └── utils.py                     # Fungsi utilitas dan helper
├── scripts/
│   ├── run_benchmark.sh             # Skrip benchmark Bash (Linux/Mac)
│   └── run_benchmark.ps1            # Skrip benchmark PowerShell (Windows)
├── results/
│   ├── row_results.csv              # Hasil waktu row striping
│   ├── block_results.csv            # Hasil waktu block striping
│   └── *.png                        # Plot yang dihasilkan
├── plot_results.py                  # Skrip visualisasi
├── requirements.txt                 # Dependensi Python
└── README.md                        # File ini
```

---

## 🔧 Kebutuhan Sistem

### Kebutuhan Sistem
- **Python**: 3.8 atau lebih tinggi
- **Implementasi MPI**: 
  - **Linux/Mac**: OpenMPI, MPICH, atau Intel MPI
  - **Windows**: Microsoft MPI (MS-MPI)
- **RAM**: Minimum 8GB (16GB+ direkomendasikan untuk matriks besar)
- **CPU**: Prosesor multi-core (4+ core direkomendasikan)

### Paket Python
- `numpy >= 1.21.0` - Komputasi numerik
- `mpi4py >= 3.1.0` - Binding Python untuk MPI
- `matplotlib >= 3.5.0` - Plotting dan visualisasi
- `pandas >= 1.3.0` - Analisis data dan penanganan CSV

---

## 📦 Instalasi

### Langkah 1: Instalasi MPI

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y openmpi-bin openmpi-common libopenmpi-dev
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install -y openmpi openmpi-devel
```

#### macOS
```bash
brew install open-mpi
```

#### Windows
1. Download and install [Microsoft MPI](https://www.microsoft.com/en-us/download/details.aspx?id=105289)
2. Install both `msmpisetup.exe` (runtime) and `msmpisdk.msi` (SDK)

### Langkah 2: Clone atau Buat Proyek

```bash
# Navigasi ke workspace Anda
cd "d:\belajar\pararel\kelompok py"

# Atau clone jika dari repository
# git clone <repository-url>
# cd <project-directory>
```

### Langkah 3: Buat Virtual Environment (Direkomendasikan)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Langkah 4: Instalasi Dependensi Python

```bash
pip install -r requirements.txt
```

### Langkah 5: Verifikasi Instalasi

```bash
# Test MPI installation
mpirun --version    # Linux/Mac
mpiexec --version   # Windows

# Test Python MPI bindings
python -c "from mpi4py import MPI; print(f'MPI Version: {MPI.Get_version()}')"
```

---

## 🚀 Cara Penggunaan

### Eksekusi Dasar

#### Row Striping
```bash
# Linux/Mac
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2

# Windows
mpiexec -n 4 python src\matrix_row_striping.py --N 1024 --workers 2
```

#### Block Striping
```bash
# Linux/Mac
mpirun -np 4 python3 src/matrix_block_striping.py --N 1024 --workers 2

# Windows
mpiexec -n 4 python src\matrix_block_striping.py --N 1024 --workers 2
```

### Argumen Command-Line

| Argumen | Tipe | Default | Deskripsi |
|---------|------|---------|--------|
| `--N` | int | 1024 | Dimensi matriks (N×N) |
| `--workers` | int | 2 | Jumlah worker multiprocessing lokal |
| `--simulate-failure` | int | None | Rank untuk simulasi kegagalan node |

### Contoh

```bash
# Test dengan matriks 2048×2048 pada 8 proses dengan 4 worker masing-masing
mpirun -np 8 python3 src/matrix_row_striping.py --N 2048 --workers 4

# Benchmark penuh dengan matriks 4096×4096
mpirun -np 16 python3 src/matrix_block_striping.py --N 4096 --workers 4

# Simulasi kegagalan pada rank 2
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2 --simulate-failure 2
```

---

## 🧪 Metodologi

### Pendekatan Row Striping

1. **Distribusi**: Matriks A dibagi menjadi strip horizontal (baris)
2. **Scatter**: Proses root menyebarkan potongan baris menggunakan `MPI.Scatterv`
3. **Broadcast**: Matriks B lengkap di-broadcast ke semua proses
4. **Compute**: Setiap proses menghitung `A_local @ B` menggunakan multiprocessing
5. **Gather**: Hasil dikumpulkan kembali menggunakan `MPI.Gatherv`

**Keuntungan**: 
- Load balancing yang sederhana
- Baik untuk matriks persegi panjang
- Efisien untuk jumlah baris yang besar

**Representasi Matematis**:
```
Proses i menerima baris [start_i : end_i] dimana:
  start_i = i * (N/P) + min(i, N%P)
  count_i = (N/P) + (1 jika i < N%P selain itu 0)
```

### Pendekatan Block Striping

1. **Formasi Grid**: Membuat grid proses pr × pc dimana pr*pc = P
2. **Distribusi**: Matriks A dibagi menjadi blok-blok
3. **Scatter**: Proses root mendistribusikan blok menggunakan `MPI.Scatterv`
4. **Broadcast**: Matriks B lengkap di-broadcast ke semua proses
5. **Compute**: Setiap proses mengalikan bloknya menggunakan multiprocessing
6. **Gather**: Hasil blok dikumpulkan menggunakan `MPI.Gatherv`

**Keuntungan**:
- Cache locality yang lebih baik untuk pola akses 2D
- Skalabel untuk jumlah proses yang besar
- Mengoptimalkan pola komunikasi

**Perhitungan Grid Proses**:
```python
pr = closest_divisor_to_sqrt(P)
pc = P / pr
```

### Komputasi Lokal

Kedua metode menggunakan **multiprocessing** untuk paralelisme intra-node:

```python
def parallel_matmul_local(A_local, B, n_workers):
    # Split A_local into chunks
    chunks = split_rows(A_local, n_workers)
    
    # Parallel computation
    with Pool(n_workers) as pool:
        results = pool.map(matmul_chunk, chunks)
    
    return concatenate(results)
```

---

## ⏱️ Metrik Waktu

Setiap implementasi mengukur metrik berikut:

### 1. **Waktu Scatter**
Waktu untuk mendistribusikan bagian matriks A dari root ke semua proses
```python
t_start = now()
comm.Scatterv([A, sendcounts, displs, MPI.DOUBLE], A_local, root=0)
t_end = now()
scatter_time = t_end - t_start
```

### 2. **Waktu Broadcast**
Waktu untuk broadcast matriks B lengkap ke semua proses
```python
t_start = now()
comm.Bcast(B, root=0)
t_end = now()
broadcast_time = t_end - t_start
```

### 3. **Waktu Komputasi**
Waktu komputasi lokal murni (multiprocessing)
```python
t_start = now()
C_local = parallel_matmul_local(A_local, B, n_workers)
t_end = now()
compute_time = t_end - t_start
```

### 4. **Waktu Gather**
Waktu untuk mengumpulkan hasil kembali ke root
```python
t_start = now()
comm.Gatherv(C_local, [C, sendcounts, displs, MPI.DOUBLE], root=0)
t_end = now()
gather_time = t_end - t_start
```

### 5. **Waktu Total**
Waktu eksekusi end-to-end
```python
communication_time = scatter_time + broadcast_time + gather_time
total_time = communication_time + compute_time
```

Semua proses melaporkan waktu maksimum mereka menggunakan `MPI.Allreduce`:
```python
scatter_time = comm.allreduce(scatter_time, op=MPI.MAX)
```

---

## 📊 Benchmarking

### Runner Benchmark Otomatis

#### Linux/Mac (Bash)
```bash
# Edit konfigurasi di scripts/run_benchmark.sh
MATRIX_SIZE=1024
WORKERS=4
PROCESS_COUNTS=(2 4 8 16)

# Jalankan benchmark
bash scripts/run_benchmark.sh
```

#### Windows (PowerShell)
```powershell
# Edit konfigurasi di scripts/run_benchmark.ps1
$MATRIX_SIZE = 1024
$WORKERS = 4
$PROCESS_COUNTS = @(2, 4, 8, 16)

# Jalankan benchmark
.\scripts\run_benchmark.ps1
```

### Benchmarking Manual

```bash
# Test berbagai jumlah proses
for P in 2 4 8 16; do
  echo "Testing dengan $P proses..."
  mpirun -np $P python3 src/matrix_row_striping.py --N 1024 --workers 4
  mpirun -np $P python3 src/matrix_block_striping.py --N 1024 --workers 4
done
```

### Penyimpanan Hasil

Hasil otomatis disimpan ke file CSV:
- `results/row_results.csv` - Hasil row striping
- `results/block_results.csv` - Hasil block striping

**CSV Format**:
```csv
method,n_processes,n_workers,matrix_size,scatter_time,broadcast_time,compute_time,gather_time,communication_time,total_time
Row,4,4,1024,0.021534,0.043210,0.982341,0.018923,0.083667,1.066008
```

---

## 📈 Visualisasi Hasil

### Generate Plot

```bash
python plot_results.py
```

### Visualisasi yang Dihasilkan

1. **total_time_comparison.png**
   - Line plot membandingkan waktu eksekusi total
   - Row vs Block striping di berbagai jumlah proses

2. **compute_vs_communication.png**
   - Bar chart menampilkan waktu compute vs komunikasi
   - Plot terpisah untuk setiap metode

3. **communication_breakdown.png**
   - Breakdown detail: scatter, broadcast, gather
   - Perbandingan side-by-side

4. **speedup_analysis.png**
   - Speedup relatif terhadap baseline (P terkecil)
   - Termasuk garis speedup ideal

5. **efficiency_analysis.png**
   - Persentase efisiensi paralel
   - Menampilkan efisiensi scaling

6. **time_percentage.png**
   - Stacked bar chart menampilkan breakdown persentase
   - Rasio compute vs komunikasi

7. **summary_table.txt**
   - Ringkasan berbasis teks dari semua hasil
   - Tabel terformat dengan semua metrik

---

## 📝 Contoh Output

### Output Console (Row Striping)

```
[Row Striping] Starting with 4 processes, 4 workers each
[Row Striping] Matrix size: 1024×1024

======================================================================
  ROW STRIPING - TIMING SUMMARY
======================================================================
  Matrix Size:              1024 × 1024
  MPI Processes:            4
  Local Workers:            4
----------------------------------------------------------------------
  Scatter Time:             0.021534 s
  Broadcast Time:           0.043210 s
  Compute Time:             0.982341 s
  Gather Time:              0.018923 s
----------------------------------------------------------------------
  Total Communication Time: 0.083667 s
  Total Execution Time:     1.066008 s
  Compute/Total Ratio:      92.15%
  Communication/Total:      7.85%
======================================================================

[Row Striping] Results saved to results/row_results.csv
```

### Contoh Hasil Benchmark

| Metode | Proses | Workers | Ukuran Matriks | Waktu Total (s) | Speedup | Efisiensi |
|--------|--------|---------|----------------|-----------------|---------|----------|
| Row    | 2      | 4       | 1024           | 1.834           | 1.00×   | 100.0%   |
| Row    | 4      | 4       | 1024           | 1.066           | 1.72×   | 86.0%    |
| Row    | 8      | 4       | 1024           | 0.623           | 2.94×   | 73.5%    |
| Block  | 2      | 4       | 1024           | 1.821           | 1.00×   | 100.0%   |
| Block  | 4      | 4       | 1024           | 1.043           | 1.75×   | 87.5%    |
| Block  | 8      | 4       | 1024           | 0.598           | 3.05×   | 76.2%    |

---

## 🔧 Simulasi Kegagalan

Test fault tolerance dengan mensimulasikan kegagalan node:

```bash
# Simulasi kegagalan pada rank 2
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2 --simulate-failure 2
```

**Output**:
```
[SIMULATION] Rank 2 simulating failure...
[ERROR] MPI process terminated unexpectedly
```

**Kasus Penggunaan**:
- Testing penanganan error
- Menganalisis dampak kegagalan node
- Mengembangkan strategi fault-tolerant

---

## 📊 Analisis Performa

### Observasi Utama

#### Overhead Komunikasi
- **Row Striping**: Overhead scatter/gather lebih rendah untuk baris yang kontinu
- **Block Striping**: Overhead berpotensi lebih tinggi tapi cache locality lebih baik

#### Skalabilitas
- **Strong Scaling**: Ukuran masalah tetap, proses bertambah
- **Ekspektasi**: Speedup mendekati linear sampai komunikasi mendominasi
- **Bottleneck**: Broadcast matriks B (data O(N²))

#### Konfigurasi Optimal
```
Performa Terbaik = f(Ukuran_Matriks, Proses, Workers)
```

**Panduan Umum**:
- Matriks kecil (≤1024): Gunakan 2-4 proses, 2-4 workers
- Matriks sedang (2048): Gunakan 4-8 proses, 4 workers
- Matriks besar (≥4096): Gunakan 8-16 proses, 4-8 workers

#### Analisis Hukum Amdahl
```
Speedup_max = 1 / (s + p/P)
dimana:
  s = fraksi serial (komunikasi)
  p = fraksi paralel (komputasi)
  P = jumlah proses
```

---

## 🛠️ Troubleshooting

### Masalah Umum

#### 1. `mpirun: command not found`
**Solusi**: Instalasi implementasi MPI
```bash
# Linux
sudo apt-get install openmpi-bin

# Mac
brew install open-mpi

# Windows - Install MS-MPI dari Microsoft
```

#### 2. `ImportError: No module named 'mpi4py'`
**Solusi**: Instalasi paket Python
```bash
pip install mpi4py
```

#### 3. Error memory dengan matriks besar
**Solusi**: Kurangi ukuran matriks atau tambah RAM
```bash
# Gunakan ukuran test yang lebih kecil
mpirun -np 4 python3 src/matrix_row_striping.py --N 512 --workers 2
```

#### 4. Windows: `mpiexec` tidak dikenali
**Solusi**: Tambahkan MS-MPI ke PATH
```powershell
$env:PATH += ";C:\Program Files\Microsoft MPI\Bin"
```

---

## 📚 Referensi

### Makalah Akademik
- Fox, G. C., et al. (1994). *Solving Problems on Concurrent Processors*
- Kumar, V., et al. (1994). *Introduction to Parallel Computing*

### Dokumentasi
- [Dokumentasi mpi4py](https://mpi4py.readthedocs.io/)
- [Python Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Dokumentasi NumPy](https://numpy.org/doc/)

### Standar MPI
- [MPI Forum](https://www.mpi-forum.org/)
- [OpenMPI](https://www.open-mpi.org/)

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Area untuk pengembangan:
- Algoritma distribusi blok 2D yang sebenarnya
- Implementasi algoritma Cannon
- Akselerasi GPU (CUDA/OpenCL)
- Mekanisme fault tolerance
- Dynamic load balancing

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License.

---

## 👥 Penulis

Dibuat untuk analisis komparatif pendekatan hybrid parallel computing dalam perkalian matriks.

---

## 🙏 Ucapan Terima Kasih

- Komunitas OpenMPI dan MPICH
- Developer mpi4py
- Kontributor Python multiprocessing

---

## 📞 Dukungan

Untuk masalah, pertanyaan, atau kontribusi:
1. Periksa dokumentasi yang ada
2. Tinjau bagian troubleshooting
3. Buka issue pada repository

---

**Selamat Parallel Computing! 🚀**
