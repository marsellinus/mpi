"""
Simple test script to verify the installation and basic functionality.
Run this without MPI to check if all dependencies are properly installed.

Usage:
    python test_installation.py
"""

import sys

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    tests = {
        'numpy': None,
        'mpi4py': None,
        'matplotlib': None,
        'pandas': None,
        'multiprocessing': None
    }
    
    # Test numpy
    try:
        import numpy as np
        tests['numpy'] = f"✓ NumPy {np.__version__}"
    except ImportError as e:
        tests['numpy'] = f"✗ NumPy import failed: {e}"
    
    # Test mpi4py
    try:
        from mpi4py import MPI
        tests['mpi4py'] = f"✓ mpi4py (MPI Standard {MPI.Get_version()})"
    except ImportError as e:
        tests['mpi4py'] = f"✗ mpi4py import failed: {e}"
    
    # Test matplotlib
    try:
        import matplotlib
        tests['matplotlib'] = f"✓ matplotlib {matplotlib.__version__}"
    except ImportError as e:
        tests['matplotlib'] = f"✗ matplotlib import failed: {e}"
    
    # Test pandas
    try:
        import pandas as pd
        tests['pandas'] = f"✓ pandas {pd.__version__}"
    except ImportError as e:
        tests['pandas'] = f"✗ pandas import failed: {e}"
    
    # Test multiprocessing
    try:
        import multiprocessing
        tests['multiprocessing'] = f"✓ multiprocessing (built-in)"
    except ImportError as e:
        tests['multiprocessing'] = f"✗ multiprocessing import failed: {e}"
    
    return tests


def test_basic_functionality():
    """Test basic matrix operations."""
    print("\nTesting basic functionality...")
    
    try:
        import numpy as np
        from multiprocessing import Pool
        
        # Test matrix creation
        A = np.random.rand(100, 100)
        B = np.random.rand(100, 100)
        
        # Test matrix multiplication
        C = np.dot(A, B)
        
        # Test multiprocessing
        def square(x):
            return x * x
        
        with Pool(processes=2) as pool:
            results = pool.map(square, [1, 2, 3, 4])
        
        print("✓ Matrix operations work correctly")
        print("✓ Multiprocessing works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False


def check_mpi_command():
    """Check if MPI command is available."""
    import subprocess
    import platform
    
    print("\nChecking MPI installation...")
    
    if platform.system() == 'Windows':
        cmd = 'mpiexec'
    else:
        cmd = 'mpirun'
    
    try:
        result = subprocess.run([cmd, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ {cmd} is available")
            print(f"  Version info: {result.stdout.split(chr(10))[0]}")
            return True
        else:
            print(f"✗ {cmd} returned error code {result.returncode}")
            return False
    except FileNotFoundError:
        print(f"✗ {cmd} not found in PATH")
        print(f"  Please install MPI:")
        if platform.system() == 'Windows':
            print("  - Download MS-MPI from Microsoft")
        else:
            print("  - Linux: sudo apt-get install openmpi-bin")
            print("  - Mac: brew install open-mpi")
        return False
    except Exception as e:
        print(f"✗ Error checking {cmd}: {e}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("  Hybrid Parallel Matrix Multiplication - Installation Test")
    print("="*70)
    
    # Test imports
    import_results = test_imports()
    
    print("\n" + "-"*70)
    print("Package Import Results:")
    print("-"*70)
    
    all_passed = True
    for package, result in import_results.items():
        print(f"  {package:15} : {result}")
        if '✗' in result:
            all_passed = False
    
    # Test functionality
    print("\n" + "-"*70)
    func_passed = test_basic_functionality()
    
    # Check MPI
    print("-"*70)
    mpi_passed = check_mpi_command()
    
    # Summary
    print("\n" + "="*70)
    print("  Test Summary")
    print("="*70)
    
    if all_passed and func_passed and mpi_passed:
        print("✓ All tests passed! You're ready to run the benchmarks.")
        print("\nNext steps:")
        print("  1. Run a quick test:")
        if sys.platform == 'win32':
            print("     mpiexec -n 4 python src\\matrix_row_striping.py --N 1024 --workers 2")
        else:
            print("     mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2")
        print("\n  2. Run full benchmark:")
        if sys.platform == 'win32':
            print("     .\\scripts\\run_benchmark.ps1")
        else:
            print("     bash scripts/run_benchmark.sh")
        print("\n  3. Generate plots:")
        print("     python plot_results.py")
        return 0
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        if not all_passed:
            print("\n  Install missing packages:")
            print("    pip install -r requirements.txt")
        if not mpi_passed:
            print("\n  Install MPI implementation for your system")
        return 1


if __name__ == '__main__':
    sys.exit(main())
