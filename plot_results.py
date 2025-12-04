"""
Visualization Script for Hybrid Parallel Matrix Multiplication Results.

Generates comparative plots showing:
1. Total execution time vs number of processes (Row vs Block)
2. Compute vs Communication time breakdown
3. Speedup analysis
4. Communication overhead comparison

Usage:
    python plot_results.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_results():
    """Load results from CSV files."""
    results_dir = 'results'
    
    row_file = os.path.join(results_dir, 'row_results.csv')
    block_file = os.path.join(results_dir, 'block_results.csv')
    
    if not os.path.exists(row_file):
        raise FileNotFoundError(f"Row results not found: {row_file}")
    if not os.path.exists(block_file):
        raise FileNotFoundError(f"Block results not found: {block_file}")
    
    row_df = pd.read_csv(row_file)
    block_df = pd.read_csv(block_file)
    
    # Add method column if not present
    if 'method' not in row_df.columns:
        row_df['method'] = 'Row'
    if 'method' not in block_df.columns:
        block_df['method'] = 'Block'
    
    # Combine dataframes
    df = pd.concat([row_df, block_df], ignore_index=True)
    
    return df


def plot_total_time_comparison(df, output_dir='results'):
    """Plot total execution time comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for method in df['method'].unique():
        method_df = df[df['method'] == method].sort_values('n_processes')
        ax.plot(method_df['n_processes'], method_df['total_time'], 
                marker='o', linewidth=2, markersize=8, label=f'{method} Striping')
    
    ax.set_xlabel('Number of MPI Processes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Total Execution Time: Row vs Block Striping', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(df['n_processes'].unique())
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'total_time_comparison.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'total_time_comparison.png')}")
    plt.close()


def plot_compute_vs_communication(df, output_dir='results'):
    """Plot compute time vs communication time breakdown."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    methods = df['method'].unique()
    
    for idx, method in enumerate(methods):
        method_df = df[df['method'] == method].sort_values('n_processes')
        
        x = np.arange(len(method_df))
        width = 0.35
        
        compute = axes[idx].bar(x - width/2, method_df['compute_time'], 
                                width, label='Compute Time', color='#2ecc71')
        comm = axes[idx].bar(x + width/2, method_df['communication_time'], 
                            width, label='Communication Time', color='#e74c3c')
        
        axes[idx].set_xlabel('Number of MPI Processes', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{method} Striping: Compute vs Communication', 
                           fontsize=12, fontweight='bold')
        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(method_df['n_processes'].values)
        axes[idx].legend(fontsize=10)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'compute_vs_communication.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'compute_vs_communication.png')}")
    plt.close()


def plot_communication_breakdown(df, output_dir='results'):
    """Plot detailed communication time breakdown."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    methods = df['method'].unique()
    
    for idx, method in enumerate(methods):
        method_df = df[df['method'] == method].sort_values('n_processes')
        
        x = np.arange(len(method_df))
        width = 0.25
        
        axes[idx].bar(x - width, method_df['scatter_time'], 
                     width, label='Scatter', color='#3498db')
        axes[idx].bar(x, method_df['broadcast_time'], 
                     width, label='Broadcast', color='#9b59b6')
        axes[idx].bar(x + width, method_df['gather_time'], 
                     width, label='Gather', color='#e67e22')
        
        axes[idx].set_xlabel('Number of MPI Processes', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{method} Striping: Communication Breakdown', 
                           fontsize=12, fontweight='bold')
        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(method_df['n_processes'].values)
        axes[idx].legend(fontsize=10)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'communication_breakdown.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'communication_breakdown.png')}")
    plt.close()


def plot_speedup(df, output_dir='results'):
    """Plot speedup analysis."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for method in df['method'].unique():
        method_df = df[df['method'] == method].sort_values('n_processes')
        
        # Calculate speedup relative to smallest process count
        baseline_time = method_df['total_time'].iloc[0]
        speedup = baseline_time / method_df['total_time']
        
        ax.plot(method_df['n_processes'], speedup, 
                marker='o', linewidth=2, markersize=8, label=f'{method} Striping')
    
    # Plot ideal speedup
    processes = df['n_processes'].unique()
    baseline_p = processes.min()
    ideal_speedup = processes / baseline_p
    ax.plot(processes, ideal_speedup, 
            'k--', linewidth=2, label='Ideal Speedup', alpha=0.5)
    
    ax.set_xlabel('Number of MPI Processes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speedup', fontsize=12, fontweight='bold')
    ax.set_title('Speedup Analysis: Row vs Block Striping', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(processes)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'speedup_analysis.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'speedup_analysis.png')}")
    plt.close()


def plot_efficiency(df, output_dir='results'):
    """Plot parallel efficiency."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for method in df['method'].unique():
        method_df = df[df['method'] == method].sort_values('n_processes')
        
        # Calculate efficiency
        baseline_time = method_df['total_time'].iloc[0]
        baseline_p = method_df['n_processes'].iloc[0]
        speedup = baseline_time / method_df['total_time']
        efficiency = (speedup * baseline_p / method_df['n_processes']) * 100
        
        ax.plot(method_df['n_processes'], efficiency, 
                marker='o', linewidth=2, markersize=8, label=f'{method} Striping')
    
    # Add 100% efficiency line
    ax.axhline(y=100, color='k', linestyle='--', linewidth=2, 
               label='Ideal (100%)', alpha=0.5)
    
    ax.set_xlabel('Number of MPI Processes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Parallel Efficiency (%)', fontsize=12, fontweight='bold')
    ax.set_title('Parallel Efficiency: Row vs Block Striping', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(df['n_processes'].unique())
    ax.set_ylim([0, 110])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'efficiency_analysis.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'efficiency_analysis.png')}")
    plt.close()


def plot_time_percentage(df, output_dir='results'):
    """Plot percentage of compute vs communication time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    methods = df['method'].unique()
    processes = sorted(df['n_processes'].unique())
    x = np.arange(len(processes))
    width = 0.35
    
    for idx, method in enumerate(methods):
        method_df = df[df['method'] == method].sort_values('n_processes')
        
        compute_pct = (method_df['compute_time'] / method_df['total_time']) * 100
        comm_pct = (method_df['communication_time'] / method_df['total_time']) * 100
        
        offset = width * (idx - 0.5)
        ax.bar(x + offset, compute_pct, width * 0.45, 
               label=f'{method} Compute %', alpha=0.8)
        ax.bar(x + offset, comm_pct, width * 0.45, 
               bottom=compute_pct, label=f'{method} Comm %', alpha=0.8)
    
    ax.set_xlabel('Number of MPI Processes', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Time Distribution: Compute vs Communication', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(processes)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 100])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'time_percentage.png'), dpi=300)
    print(f"✓ Saved: {os.path.join(output_dir, 'time_percentage.png')}")
    plt.close()


def generate_summary_table(df, output_dir='results'):
    """Generate a summary table of results."""
    summary_file = os.path.join(output_dir, 'summary_table.txt')
    
    with open(summary_file, 'w') as f:
        f.write("="*100 + "\n")
        f.write("HYBRID PARALLEL MATRIX MULTIPLICATION - SUMMARY RESULTS\n")
        f.write("="*100 + "\n\n")
        
        for method in df['method'].unique():
            method_df = df[df['method'] == method].sort_values('n_processes')
            
            f.write(f"\n{method.upper()} STRIPING\n")
            f.write("-"*100 + "\n")
            f.write(f"{'Procs':<8} {'Workers':<10} {'Size':<10} {'Scatter':<12} {'Broadcast':<12} "
                   f"{'Compute':<12} {'Gather':<12} {'Total':<12}\n")
            f.write("-"*100 + "\n")
            
            for _, row in method_df.iterrows():
                f.write(f"{row['n_processes']:<8} {row['n_workers']:<10} "
                       f"{row['matrix_size']:<10} {row['scatter_time']:<12.6f} "
                       f"{row['broadcast_time']:<12.6f} {row['compute_time']:<12.6f} "
                       f"{row['gather_time']:<12.6f} {row['total_time']:<12.6f}\n")
            
            f.write("\n")
    
    print(f"✓ Saved: {summary_file}")


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("  Hybrid Parallel Matrix Multiplication - Visualization")
    print("="*70 + "\n")
    
    try:
        # Load results
        print("Loading results from CSV files...")
        df = load_results()
        print(f"✓ Loaded {len(df)} result entries\n")
        
        # Create output directory
        output_dir = 'results'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate plots
        print("Generating plots...")
        plot_total_time_comparison(df, output_dir)
        plot_compute_vs_communication(df, output_dir)
        plot_communication_breakdown(df, output_dir)
        plot_speedup(df, output_dir)
        plot_efficiency(df, output_dir)
        plot_time_percentage(df, output_dir)
        
        # Generate summary table
        print("\nGenerating summary table...")
        generate_summary_table(df, output_dir)
        
        print("\n" + "="*70)
        print("  Visualization Complete!")
        print("="*70)
        print(f"\nAll plots saved to: {output_dir}/")
        print("\nGenerated files:")
        print("  1. total_time_comparison.png")
        print("  2. compute_vs_communication.png")
        print("  3. communication_breakdown.png")
        print("  4. speedup_analysis.png")
        print("  5. efficiency_analysis.png")
        print("  6. time_percentage.png")
        print("  7. summary_table.txt")
        print("")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease run the benchmark script first:")
        print("  Linux/Mac: bash scripts/run_benchmark.sh")
        print("  Windows:   powershell scripts/run_benchmark.ps1")
        print("")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
