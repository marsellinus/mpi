# Automated Benchmark Runner for Hybrid Parallel Matrix Multiplication
# PowerShell version for Windows
# Tests both row and block striping with different process counts

# Configuration
$MATRIX_SIZE = 1024  # Use 1024 for testing, 4096 for full benchmark
$WORKERS = 4         # Number of local multiprocessing workers
$PROCESS_COUNTS = @(2, 4, 8, 16)

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Hybrid Parallel Matrix Multiplication" -ForegroundColor Blue
Write-Host "  Benchmark Runner" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Matrix Size: $MATRIX_SIZE×$MATRIX_SIZE" -ForegroundColor Green
Write-Host "Local Workers: $WORKERS" -ForegroundColor Green
Write-Host "Process Counts: $($PROCESS_COUNTS -join ', ')" -ForegroundColor Green
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
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "Testing with $P processes" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    
    # Row Striping
    Write-Host ""
    Write-Host "[1/2] Running Row Striping..." -ForegroundColor Blue
    mpiexec -n $P python src\matrix_row_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Row striping failed with $P processes" -ForegroundColor Red
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
