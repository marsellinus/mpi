# Hybrid Parallel Matrix Multiplication
## Analisis Komparatif: Row Striping vs Block Striping

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MPI](https://img.shields.io/badge/MPI-mpi4py-green.svg)](https://mpi4py.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive comparative analysis of **hybrid parallel matrix multiplication** using **MPI (Message Passing Interface)** and **Python multiprocessing**. This project implements and benchmarks two data distribution strategies:

1. **Row Striping** - Distributes rows of matrix A across processes
2. **Block Striping** - Distributes blocks of matrix A using 2D process grid

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Methodology](#-methodology)
- [Timing Metrics](#-timing-metrics)
- [Benchmarking](#-benchmarking)
- [Results Visualization](#-results-visualization)
- [Example Output](#-example-output)
- [Failure Simulation](#-failure-simulation)
- [Performance Analysis](#-performance-analysis)

---

## ✨ Features

- **Hybrid Parallelism**: Combines distributed-memory (MPI) and shared-memory (multiprocessing) parallelism
- **Two Distribution Strategies**: 
  - Row striping for fine-grained row distribution
  - Block striping with 2D process grid optimization
- **Comprehensive Timing**: Measures scatter, broadcast, compute, gather, and total execution time
- **Automated Benchmarking**: Scripts for testing multiple process counts
- **Rich Visualization**: Generates 6+ comparative plots and summary tables
- **Failure Simulation**: Optional node failure testing for fault tolerance analysis
- **Scalable**: Supports matrix sizes from 1024×1024 to 4096×4096 and beyond

---

## 📁 Project Structure

```
project/
├── src/
│   ├── matrix_row_striping.py      # Row striping implementation
│   ├── matrix_block_striping.py    # Block striping implementation
│   └── utils.py                     # Utility functions and helpers
├── scripts/
│   ├── run_benchmark.sh             # Bash benchmark script (Linux/Mac)
│   └── run_benchmark.ps1            # PowerShell benchmark script (Windows)
├── results/
│   ├── row_results.csv              # Row striping timing results
│   ├── block_results.csv            # Block striping timing results
│   └── *.png                        # Generated plots
├── plot_results.py                  # Visualization script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🔧 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **MPI Implementation**: 
  - **Linux/Mac**: OpenMPI, MPICH, or Intel MPI
  - **Windows**: Microsoft MPI (MS-MPI)
- **RAM**: Minimum 8GB (16GB+ recommended for large matrices)
- **CPU**: Multi-core processor (4+ cores recommended)

### Python Packages
- `numpy >= 1.21.0` - Numerical computing
- `mpi4py >= 3.1.0` - MPI Python bindings
- `matplotlib >= 3.5.0` - Plotting and visualization
- `pandas >= 1.3.0` - Data analysis and CSV handling

---

## 📦 Installation

### Step 1: Install MPI

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

### Step 2: Clone or Create Project

```bash
# Navigate to your workspace
cd "d:\belajar\pararel\kelompok py"

# Or clone if from repository
# git clone <repository-url>
# cd <project-directory>
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Test MPI installation
mpirun --version    # Linux/Mac
mpiexec --version   # Windows

# Test Python MPI bindings
python -c "from mpi4py import MPI; print(f'MPI Version: {MPI.Get_version()}')"
```

---

## 🚀 Usage

### Basic Execution

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

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--N` | int | 1024 | Matrix dimension (N×N) |
| `--workers` | int | 2 | Number of local multiprocessing workers |
| `--simulate-failure` | int | None | Rank to simulate node failure |

### Examples

```bash
# Test with 2048×2048 matrix on 8 processes with 4 workers each
mpirun -np 8 python3 src/matrix_row_striping.py --N 2048 --workers 4

# Full benchmark with 4096×4096 matrix
mpirun -np 16 python3 src/matrix_block_striping.py --N 4096 --workers 4

# Simulate failure at rank 2
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2 --simulate-failure 2
```

---

## 🧪 Methodology

### Row Striping Approach

1. **Distribution**: Matrix A is divided into horizontal strips (rows)
2. **Scatter**: Root process scatters row chunks using `MPI.Scatterv`
3. **Broadcast**: Full matrix B is broadcast to all processes
4. **Compute**: Each process computes `A_local @ B` using multiprocessing
5. **Gather**: Results are gathered back using `MPI.Gatherv`

**Advantages**: 
- Simple load balancing
- Good for rectangular matrices
- Efficient for large row counts

**Mathematical Representation**:
```
Process i receives rows [start_i : end_i] where:
  start_i = i * (N/P) + min(i, N%P)
  count_i = (N/P) + (1 if i < N%P else 0)
```

### Block Striping Approach

1. **Grid Formation**: Creates pr × pc process grid where pr*pc = P
2. **Distribution**: Matrix A is divided into blocks
3. **Scatter**: Root process distributes blocks using `MPI.Scatterv`
4. **Broadcast**: Full matrix B is broadcast to all processes
5. **Compute**: Each process multiplies its block using multiprocessing
6. **Gather**: Block results are gathered using `MPI.Gatherv`

**Advantages**:
- Better cache locality for 2D access patterns
- Scalable for large process counts
- Optimizes communication patterns

**Process Grid Calculation**:
```python
pr = closest_divisor_to_sqrt(P)
pc = P / pr
```

### Local Computation

Both methods use **multiprocessing** for intra-node parallelism:

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

## ⏱️ Timing Metrics

Each implementation measures the following metrics:

### 1. **Scatter Time**
Time to distribute matrix A portions from root to all processes
```python
t_start = now()
comm.Scatterv([A, sendcounts, displs, MPI.DOUBLE], A_local, root=0)
t_end = now()
scatter_time = t_end - t_start
```

### 2. **Broadcast Time**
Time to broadcast full matrix B to all processes
```python
t_start = now()
comm.Bcast(B, root=0)
t_end = now()
broadcast_time = t_end - t_start
```

### 3. **Compute Time**
Pure local computation time (multiprocessing)
```python
t_start = now()
C_local = parallel_matmul_local(A_local, B, n_workers)
t_end = now()
compute_time = t_end - t_start
```

### 4. **Gather Time**
Time to collect results back to root
```python
t_start = now()
comm.Gatherv(C_local, [C, sendcounts, displs, MPI.DOUBLE], root=0)
t_end = now()
gather_time = t_end - t_start
```

### 5. **Total Time**
End-to-end execution time
```python
communication_time = scatter_time + broadcast_time + gather_time
total_time = communication_time + compute_time
```

All processes report their maximum time using `MPI.Allreduce`:
```python
scatter_time = comm.allreduce(scatter_time, op=MPI.MAX)
```

---

## 📊 Benchmarking

### Automated Benchmark Runner

#### Linux/Mac (Bash)
```bash
# Edit configuration in scripts/run_benchmark.sh
MATRIX_SIZE=1024
WORKERS=4
PROCESS_COUNTS=(2 4 8 16)

# Run benchmark
bash scripts/run_benchmark.sh
```

#### Windows (PowerShell)
```powershell
# Edit configuration in scripts/run_benchmark.ps1
$MATRIX_SIZE = 1024
$WORKERS = 4
$PROCESS_COUNTS = @(2, 4, 8, 16)

# Run benchmark
.\scripts\run_benchmark.ps1
```

### Manual Benchmarking

```bash
# Test different process counts
for P in 2 4 8 16; do
  echo "Testing with $P processes..."
  mpirun -np $P python3 src/matrix_row_striping.py --N 1024 --workers 4
  mpirun -np $P python3 src/matrix_block_striping.py --N 1024 --workers 4
done
```

### Results Storage

Results are automatically saved to CSV files:
- `results/row_results.csv` - Row striping results
- `results/block_results.csv` - Block striping results

**CSV Format**:
```csv
method,n_processes,n_workers,matrix_size,scatter_time,broadcast_time,compute_time,gather_time,communication_time,total_time
Row,4,4,1024,0.021534,0.043210,0.982341,0.018923,0.083667,1.066008
```

---

## 📈 Results Visualization

### Generate Plots

```bash
python plot_results.py
```

### Generated Visualizations

1. **total_time_comparison.png**
   - Line plot comparing total execution time
   - Row vs Block striping across process counts

2. **compute_vs_communication.png**
   - Bar charts showing compute vs communication time
   - Separate plots for each method

3. **communication_breakdown.png**
   - Detailed breakdown: scatter, broadcast, gather
   - Side-by-side comparison

4. **speedup_analysis.png**
   - Speedup relative to baseline (smallest P)
   - Includes ideal speedup line

5. **efficiency_analysis.png**
   - Parallel efficiency percentage
   - Shows scaling efficiency

6. **time_percentage.png**
   - Stacked bar chart showing percentage breakdown
   - Compute vs communication ratios

7. **summary_table.txt**
   - Text-based summary of all results
   - Formatted table with all metrics

---

## 📝 Example Output

### Console Output (Row Striping)

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

### Sample Benchmark Results

| Method | Processes | Workers | Matrix Size | Total Time (s) | Speedup | Efficiency |
|--------|-----------|---------|-------------|----------------|---------|------------|
| Row    | 2         | 4       | 1024        | 1.834          | 1.00×   | 100.0%     |
| Row    | 4         | 4       | 1024        | 1.066          | 1.72×   | 86.0%      |
| Row    | 8         | 4       | 1024        | 0.623          | 2.94×   | 73.5%      |
| Block  | 2         | 4       | 1024        | 1.821          | 1.00×   | 100.0%     |
| Block  | 4         | 4       | 1024        | 1.043          | 1.75×   | 87.5%      |
| Block  | 8         | 4       | 1024        | 0.598          | 3.05×   | 76.2%      |

---

## 🔧 Failure Simulation

Test fault tolerance by simulating node failures:

```bash
# Simulate failure at rank 2
mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2 --simulate-failure 2
```

**Output**:
```
[SIMULATION] Rank 2 simulating failure...
[ERROR] MPI process terminated unexpectedly
```

**Use Cases**:
- Testing error handling
- Analyzing impact of node failures
- Developing fault-tolerant strategies

---

## 📊 Performance Analysis

### Key Observations

#### Communication Overhead
- **Row Striping**: Lower scatter/gather overhead for contiguous rows
- **Block Striping**: Potentially higher overhead but better cache locality

#### Scalability
- **Strong Scaling**: Fixed problem size, increasing processes
- **Expected**: Near-linear speedup until communication dominates
- **Bottleneck**: Broadcast of matrix B (O(N²) data)

#### Optimal Configuration
```
Best Performance = f(Matrix_Size, Processes, Workers)
```

**General Guidelines**:
- Small matrices (≤1024): Use 2-4 processes, 2-4 workers
- Medium matrices (2048): Use 4-8 processes, 4 workers
- Large matrices (≥4096): Use 8-16 processes, 4-8 workers

#### Amdahl's Law Analysis
```
Speedup_max = 1 / (s + p/P)
where:
  s = serial fraction (communication)
  p = parallel fraction (compute)
  P = number of processes
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. `mpirun: command not found`
**Solution**: Install MPI implementation
```bash
# Linux
sudo apt-get install openmpi-bin

# Mac
brew install open-mpi

# Windows - Install MS-MPI from Microsoft
```

#### 2. `ImportError: No module named 'mpi4py'`
**Solution**: Install Python packages
```bash
pip install mpi4py
```

#### 3. Memory errors with large matrices
**Solution**: Reduce matrix size or increase RAM
```bash
# Use smaller test size
mpirun -np 4 python3 src/matrix_row_striping.py --N 512 --workers 2
```

#### 4. Windows: `mpiexec` not recognized
**Solution**: Add MS-MPI to PATH
```powershell
$env:PATH += ";C:\Program Files\Microsoft MPI\Bin"
```

---

## 📚 References

### Academic Papers
- Fox, G. C., et al. (1994). *Solving Problems on Concurrent Processors*
- Kumar, V., et al. (1994). *Introduction to Parallel Computing*

### Documentation
- [mpi4py Documentation](https://mpi4py.readthedocs.io/)
- [Python Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [NumPy Documentation](https://numpy.org/doc/)

### MPI Standards
- [MPI Forum](https://www.mpi-forum.org/)
- [OpenMPI](https://www.open-mpi.org/)

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- True 2D block distribution algorithm
- Cannon's algorithm implementation
- GPU acceleration (CUDA/OpenCL)
- Fault tolerance mechanisms
- Dynamic load balancing

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

Created for comparative analysis of hybrid parallel computing approaches in matrix multiplication.

---

## 🙏 Acknowledgments

- OpenMPI and MPICH communities
- mpi4py developers
- Python multiprocessing contributors

---

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Open an issue on the repository

---

**Happy Parallel Computing! 🚀**
