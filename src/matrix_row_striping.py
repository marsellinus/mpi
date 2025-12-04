"""
Row Striping Matrix Multiplication using MPI + Multiprocessing.

This implementation distributes rows of matrix A across MPI processes,
broadcasts matrix B to all processes, and uses multiprocessing for local computation.

Usage:
    mpirun -np <P> python matrix_row_striping.py --N 4096 --workers 4
    mpirun -np <P> python matrix_row_striping.py --N 1024 --workers 2 --simulate-failure 1
"""

import argparse
import os
import sys
import numpy as np
from mpi4py import MPI

# Import utility functions
sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    now, parallel_matmul_local, create_test_matrices,
    save_results_to_csv, distribute_rows, print_timing_summary
)


def row_striping_matmul(N, n_workers, simulate_failure_rank=None):
    """
    Perform matrix multiplication using row striping approach.
    
    Args:
        N: Matrix dimension (N×N)
        n_workers: Number of local multiprocessing workers
        simulate_failure_rank: Rank to simulate failure (optional)
        
    Returns:
        Dictionary with timing results
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Simulate failure if requested
    if simulate_failure_rank is not None and rank == simulate_failure_rank:
        if rank == 0:
            print(f"\n[SIMULATION] Rank {rank} simulating failure...")
        comm.Barrier()
        os._exit(1)
    
    # Initialize timing variables
    scatter_time = 0.0
    broadcast_time = 0.0
    compute_time = 0.0
    gather_time = 0.0
    
    # Start total timing
    t_start = now()
    
    # Rank 0 creates matrices
    if rank == 0:
        A, B = create_test_matrices(N)
        print(f"\n[Row Striping] Starting with {size} processes, {n_workers} workers each")
        print(f"[Row Striping] Matrix size: {N}×{N}")
    else:
        A = None
        B = np.empty((N, N), dtype=np.float64)
    
    # Calculate row distribution
    start_row, end_row, local_rows = distribute_rows(N, size, rank)
    
    # Prepare send counts and displacements for Scatterv
    if rank == 0:
        sendcounts = []
        displs = []
        for r in range(size):
            s, e, count = distribute_rows(N, size, r)
            sendcounts.append(count * N)
            displs.append(s * N)
        sendcounts = np.array(sendcounts, dtype=np.int32)
        displs = np.array(displs, dtype=np.int32)
    else:
        sendcounts = None
        displs = None
    
    # Allocate receive buffer
    A_local = np.empty((local_rows, N), dtype=np.float64)
    
    # Scatter rows of A
    t_scatter_start = now()
    comm.Scatterv([A, sendcounts, displs, MPI.DOUBLE], A_local, root=0)
    t_scatter_end = now()
    scatter_time = t_scatter_end - t_scatter_start
    
    # Broadcast matrix B
    t_bcast_start = now()
    if rank == 0:
        comm.Bcast(B, root=0)
    else:
        comm.Bcast(B, root=0)
    t_bcast_end = now()
    broadcast_time = t_bcast_end - t_bcast_start
    
    # Local computation using multiprocessing
    t_compute_start = now()
    C_local = parallel_matmul_local(A_local, B, n_workers)
    t_compute_end = now()
    compute_time = t_compute_end - t_compute_start
    
    # Gather results
    if rank == 0:
        C = np.empty((N, N), dtype=np.float64)
    else:
        C = None
    
    t_gather_start = now()
    comm.Gatherv(C_local, [C, sendcounts, displs, MPI.DOUBLE], root=0)
    t_gather_end = now()
    gather_time = t_gather_end - t_gather_start
    
    # End total timing
    t_end = now()
    total_time = t_end - t_start
    
    # Collect timing data from all processes (max values)
    scatter_time = comm.allreduce(scatter_time, op=MPI.MAX)
    broadcast_time = comm.allreduce(broadcast_time, op=MPI.MAX)
    compute_time = comm.allreduce(compute_time, op=MPI.MAX)
    gather_time = comm.allreduce(gather_time, op=MPI.MAX)
    total_time = comm.allreduce(total_time, op=MPI.MAX)
    
    # Print summary and save results
    print_timing_summary(rank, "ROW", size, n_workers, N,
                        scatter_time, broadcast_time, compute_time,
                        gather_time, total_time)
    
    # Save to CSV
    if rank == 0:
        results = {
            'method': 'Row',
            'n_processes': size,
            'n_workers': n_workers,
            'matrix_size': N,
            'scatter_time': scatter_time,
            'broadcast_time': broadcast_time,
            'compute_time': compute_time,
            'gather_time': gather_time,
            'communication_time': scatter_time + broadcast_time + gather_time,
            'total_time': total_time
        }
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'results', 'row_results.csv')
        save_results_to_csv(csv_path, results)
        print(f"[Row Striping] Results saved to {csv_path}")
    
    return {
        'scatter_time': scatter_time,
        'broadcast_time': broadcast_time,
        'compute_time': compute_time,
        'gather_time': gather_time,
        'total_time': total_time
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Row Striping Matrix Multiplication (MPI + Multiprocessing)'
    )
    parser.add_argument('--N', type=int, default=1024,
                        help='Matrix dimension (default: 1024)')
    parser.add_argument('--workers', type=int, default=2,
                        help='Number of local multiprocessing workers (default: 2)')
    parser.add_argument('--simulate-failure', type=int, default=None,
                        help='Simulate failure at specified rank (optional)')
    
    args = parser.parse_args()
    
    # Run the computation
    try:
        row_striping_matmul(args.N, args.workers, args.simulate_failure)
    except Exception as e:
        rank = MPI.COMM_WORLD.Get_rank()
        print(f"[ERROR] Rank {rank}: {e}", file=sys.stderr)
        MPI.COMM_WORLD.Abort(1)


if __name__ == '__main__':
    main()
