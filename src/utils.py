"""
Utility functions for hybrid parallel matrix multiplication.
Provides timing helpers and multiprocessing-based local computation.
"""

import time
import numpy as np
from multiprocessing import Pool
from functools import partial


def now():
    """Return high-resolution timestamp for timing measurements."""
    return time.perf_counter()


def multiply_row_chunk(args):
    """
    Multiply a chunk of rows from matrix A with full matrix B.
    
    Args:
        args: tuple of (A_chunk, B, start_row, end_row)
        
    Returns:
        Result matrix chunk
    """
    A_chunk, B = args
    return np.dot(A_chunk, B)


def parallel_matmul_local(A_local, B, n_workers):
    """
    Perform parallel matrix multiplication using multiprocessing.
    
    Splits A_local into chunks and distributes to worker processes.
    Each worker computes its chunk @ B.
    
    Args:
        A_local: Local portion of matrix A (rows × N)
        B: Full matrix B (N × N)
        n_workers: Number of worker processes
        
    Returns:
        Result matrix (rows × N)
    """
    if n_workers <= 1:
        # No parallelism, just compute directly
        return np.dot(A_local, B)
    
    rows = A_local.shape[0]
    if rows == 0:
        return A_local @ B
    
    # For small workloads, don't use multiprocessing to avoid overhead
    if rows < n_workers * 10:
        return np.dot(A_local, B)
    
    # Split rows among workers
    chunk_size = max(1, rows // n_workers)
    chunks = []
    
    for i in range(0, rows, chunk_size):
        end = min(i + chunk_size, rows)
        chunks.append((A_local[i:end], B))
    
    try:
        # Use multiprocessing pool with error handling
        with Pool(processes=n_workers) as pool:
            results = pool.map(multiply_row_chunk, chunks)
        
        # Concatenate results
        return np.vstack(results)
    except Exception as e:
        # Fallback to serial computation if multiprocessing fails
        import warnings
        warnings.warn(f"Multiprocessing failed: {e}. Falling back to serial computation.")
        return np.dot(A_local, B)


def create_test_matrices(N, seed=42):
    """
    Create test matrices A and B of size N×N.
    
    Args:
        N: Matrix dimension
        seed: Random seed for reproducibility
        
    Returns:
        tuple of (A, B) matrices
    """
    np.random.seed(seed)
    A = np.random.rand(N, N).astype(np.float64)
    B = np.random.rand(N, N).astype(np.float64)
    return A, B


def save_results_to_csv(filepath, results):
    """
    Save timing results to CSV file.
    
    Args:
        filepath: Output CSV file path
        results: Dictionary containing timing metrics
    """
    import csv
    
    # Check if file exists to determine if we need headers
    try:
        with open(filepath, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    
    with open(filepath, 'a', newline='') as f:
        fieldnames = ['method', 'n_processes', 'n_workers', 'matrix_size', 
                      'scatter_time', 'broadcast_time', 'compute_time', 
                      'gather_time', 'communication_time', 'total_time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(results)


def calculate_process_grid(P):
    """
    Calculate a 2D process grid for block distribution.
    Tries to find pr × pc where pr*pc = P and grid is as square as possible.
    
    Args:
        P: Total number of processes
        
    Returns:
        tuple of (pr, pc) - rows and columns in process grid
    """
    import math
    
    # Find the closest square grid
    sqrt_p = int(math.sqrt(P))
    
    # Try to find factors close to sqrt
    for pr in range(sqrt_p, 0, -1):
        if P % pr == 0:
            pc = P // pr
            return (pr, pc)
    
    # Fallback: linear arrangement
    return (P, 1)


def distribute_rows(N, P, rank):
    """
    Calculate row distribution for a given rank.
    
    Args:
        N: Total number of rows
        P: Total number of processes
        rank: Current process rank
        
    Returns:
        tuple of (start_row, end_row, count)
    """
    base_rows = N // P
    remainder = N % P
    
    # First 'remainder' processes get one extra row
    if rank < remainder:
        count = base_rows + 1
        start = rank * count
    else:
        count = base_rows
        start = remainder * (base_rows + 1) + (rank - remainder) * base_rows
    
    end = start + count
    return start, end, count


def print_timing_summary(rank, method, n_processes, n_workers, N, 
                         scatter_time, broadcast_time, compute_time, 
                         gather_time, total_time):
    """
    Print formatted timing summary (only from rank 0).
    
    Args:
        rank: MPI rank
        method: Method name (Row/Block)
        n_processes: Number of MPI processes
        n_workers: Number of local workers
        N: Matrix size
        scatter_time: Time for scatter operation
        broadcast_time: Time for broadcast operation
        compute_time: Time for local computation
        gather_time: Time for gather operation
        total_time: Total execution time
    """
    if rank == 0:
        comm_time = scatter_time + broadcast_time + gather_time
        print(f"\n{'='*70}")
        print(f"  {method} STRIPING - TIMING SUMMARY")
        print(f"{'='*70}")
        print(f"  Matrix Size:              {N} × {N}")
        print(f"  MPI Processes:            {n_processes}")
        print(f"  Local Workers:            {n_workers}")
        print(f"{'-'*70}")
        print(f"  Scatter Time:             {scatter_time:.6f} s")
        print(f"  Broadcast Time:           {broadcast_time:.6f} s")
        print(f"  Compute Time:             {compute_time:.6f} s")
        print(f"  Gather Time:              {gather_time:.6f} s")
        print(f"{'-'*70}")
        print(f"  Total Communication Time: {comm_time:.6f} s")
        print(f"  Total Execution Time:     {total_time:.6f} s")
        print(f"  Compute/Total Ratio:      {(compute_time/total_time)*100:.2f}%")
        print(f"  Communication/Total:      {(comm_time/total_time)*100:.2f}%")
        print(f"{'='*70}\n")
