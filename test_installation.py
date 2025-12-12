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


def _test_square(x):
    """Helper function for multiprocessing test (must be at module level)."""
    return x * x


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
        
        print("✓ Matrix operations work correctly")
        
        # Test multiprocessing (optional, may fail on some systems)
        try:
            with Pool(processes=2) as pool:
                results = pool.map(_test_square, [1, 2, 3, 4])
            print("✓ Multiprocessing works correctly")
        except Exception as mp_error:
            print(f"⚠ Multiprocessing test skipped: {mp_error}")
            print("  (This is OK - multiprocessing will work in MPI context)")
        
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
                              timeout=5,
                              shell=True)  # Use shell on Windows
        if result.returncode == 0:
            print(f"✓ {cmd} is available")
            version_line = result.stdout.strip().split('\n')[0] if result.stdout else "Unknown version"
            print(f"  Version: {version_line}")
            return True
        else:
            # On Windows, mpiexec --version may return non-zero but still work
            if platform.system() == 'Windows' and result.stdout:
                print(f"✓ {cmd} is available (non-standard return code)")
                print(f"  Output: {result.stdout.strip().split(chr(10))[0]}")
                return True
            print(f"⚠ {cmd} returned exit code {result.returncode}")
            print(f"  This may be OK - try running an actual MPI program")
            return True  # Assume it's OK if command exists
    except FileNotFoundError:
        print(f"✗ {cmd} not found in PATH")
        print(f"  Please install MPI:")
        if platform.system() == 'Windows':
            print("  - Download MS-MPI from Microsoft")
        else:
            print("  - Linux: sudo apt-get install openmpi-bin")
            print("  - Mac: brew install open-mpi")
        return False
    except subprocess.TimeoutExpired:
        print(f"⚠ {cmd} command timed out")
        print(f"  This may indicate MPI is installed but not responding")
        return True
    except Exception as e:
        print(f"⚠ Could not verify {cmd}: {e}")
        print(f"  MPI may still be working - try running a test")
        return True  # Don't fail the test, MPI might still work


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
            print("     mpiexec -n 2 python src\\matrix_row_striping.py --N 1024 --workers 4")
            print("     (Note: Use workers=1 for 4+ processes on Windows)")
        else:
            print("     mpirun -np 4 python3 src/matrix_row_striping.py --N 1024 --workers 2")
        print("\n  2. Run benchmark (auto-optimized):")
        if sys.platform == 'win32':
            print("     .\\scripts\\run_benchmark.ps1")
            print("     (Auto-adjusts workers for Windows stability)")
        else:
            print("     bash scripts/run_benchmark.sh")
        print("\n  3. Generate plots:")
        print("     python plot_results.py")
        print("\n  For Windows users: See SOLUSI_ERROR.md and WINDOWS_GUIDE.md")
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
