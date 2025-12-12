# Automated Benchmark Runner for Hybrid Parallel Matrix Multiplication
# PowerShell version for Windows
# Automatically adjusts worker count based on number of MPI processes for stability

# Configuration
$MATRIX_SIZE = 1024  # Use 1024 for testing, 4096 for full benchmark
$PROCESS_COUNTS = @(2, 4, 8)  # Tested and working on Windows

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Hybrid Parallel Matrix Multiplication" -ForegroundColor Blue
Write-Host "  Benchmark Runner (Windows-Optimized)" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Matrix Size: $MATRIX_SIZE×$MATRIX_SIZE" -ForegroundColor Green
Write-Host "Process Counts: $($PROCESS_COUNTS -join ', ')" -ForegroundColor Green
Write-Host "Workers: Auto-adjusted (P≤2: 4 workers, P>2: 1 worker)" -ForegroundColor Yellow
Write-Host ""

# Check if mpiexec is available
if (-not (Get-Command mpiexec -ErrorAction SilentlyContinue)) {
    Write-Host "Error: mpiexec not found. Please install MS-MPI." -ForegroundColor Red
    exit 1
}

# Create results directory if it doesn't exist
if (-not (Test-Path "results")) {
    New-Item -ItemType Directory -Path "results" | Out-Null
}

# Clear previous results
Write-Host "Clearing previous results..." -ForegroundColor Blue
if (Test-Path "results\row_results.csv") { Remove-Item "results\row_results.csv" }
if (Test-Path "results\block_results.csv") { Remove-Item "results\block_results.csv" }

# Run benchmarks
foreach ($P in $PROCESS_COUNTS) {
    # Auto-adjust workers: more processes = fewer workers (Windows MS-MPI limitation)
    if ($P -le 2) {
        $WORKERS = 4
        $STATUS = "Hybrid (4 workers/process)"
    } else {
        $WORKERS = 1
        $STATUS = "MPI-Dominant (1 worker/process)"
    }
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "Testing with $P processes, $WORKERS workers" -ForegroundColor Green
    Write-Host "Configuration: $STATUS" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Green
    
    # Row Striping
    Write-Host ""
    Write-Host "[1/2] Running Row Striping..." -ForegroundColor Blue
    mpiexec -n $P python src\matrix_row_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Row striping failed with $P processes" -ForegroundColor Red
        Write-Host "Tip: Try reducing workers or using fewer processes" -ForegroundColor Yellow
    } else {
        Write-Host "Row striping completed successfully" -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 2
    
    # Block Striping
    Write-Host ""
    Write-Host "[2/2] Running Block Striping..." -ForegroundColor Blue
    mpiexec -n $P python src\matrix_block_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Block striping failed with $P processes" -ForegroundColor Red
        Write-Host "Tip: Try reducing workers or using fewer processes" -ForegroundColor Yellow
    } else {
        Write-Host "Block striping completed successfully" -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Benchmark completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Results saved to:"
Write-Host "  - results\row_results.csv" -ForegroundColor Blue
Write-Host "  - results\block_results.csv" -ForegroundColor Blue
Write-Host ""
Write-Host "To visualize results, run:"
Write-Host "  python plot_results.py" -ForegroundColor Blue
Write-Host ""
Write-Host "Note: Script uses auto-adjusted workers for Windows stability." -ForegroundColor Yellow
Write-Host "      P≤2: 4 workers (hybrid), P>2: 1 worker (MPI-dominant)" -ForegroundColor Yellow
Write-Host ""
