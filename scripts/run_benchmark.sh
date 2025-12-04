#!/bin/bash
# Automated Benchmark Runner for Hybrid Parallel Matrix Multiplication
# Tests both row and block striping with different process counts

# Configuration
MATRIX_SIZE=1024  # Use 1024 for testing, 4096 for full benchmark
WORKERS=4         # Number of local multiprocessing workers
PROCESS_COUNTS=(2 4 8 16)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Hybrid Parallel Matrix Multiplication${NC}"
echo -e "${BLUE}  Benchmark Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Matrix Size: ${GREEN}${MATRIX_SIZE}×${MATRIX_SIZE}${NC}"
echo -e "Local Workers: ${GREEN}${WORKERS}${NC}"
echo -e "Process Counts: ${GREEN}${PROCESS_COUNTS[@]}${NC}"
echo ""

# Check if mpirun is available
if ! command -v mpirun &> /dev/null; then
    echo -e "${RED}Error: mpirun not found. Please install MPI.${NC}"
    exit 1
fi

# Create results directory if it doesn't exist
mkdir -p results

# Clear previous results
echo -e "${BLUE}Clearing previous results...${NC}"
rm -f results/row_results.csv
rm -f results/block_results.csv

# Run benchmarks
for P in "${PROCESS_COUNTS[@]}"; do
    echo -e "\n${GREEN}============================================${NC}"
    echo -e "${GREEN}Testing with $P processes${NC}"
    echo -e "${GREEN}============================================${NC}"
    
    # Row Striping
    echo -e "\n${BLUE}[1/2] Running Row Striping...${NC}"
    mpirun -np $P python3 src/matrix_row_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Row striping failed with $P processes${NC}"
    else
        echo -e "${GREEN}Row striping completed successfully${NC}"
    fi
    
    sleep 2
    
    # Block Striping
    echo -e "\n${BLUE}[2/2] Running Block Striping...${NC}"
    mpirun -np $P python3 src/matrix_block_striping.py --N $MATRIX_SIZE --workers $WORKERS
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Block striping failed with $P processes${NC}"
    else
        echo -e "${GREEN}Block striping completed successfully${NC}"
    fi
    
    sleep 2
done

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Benchmark completed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\nResults saved to:"
echo -e "  - ${BLUE}results/row_results.csv${NC}"
echo -e "  - ${BLUE}results/block_results.csv${NC}"
echo -e "\nTo visualize results, run:"
echo -e "  ${BLUE}python3 plot_results.py${NC}"
echo ""
