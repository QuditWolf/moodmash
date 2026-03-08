#!/bin/bash
# Master test runner for all container orchestration tests
# This script runs all test scripts in sequence and provides a summary

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Test results tracking
declare -A test_results
test_count=0
passed_count=0
failed_count=0

# Function to run a test and track results
run_test() {
    local test_name=$1
    local test_script=$2
    
    test_count=$((test_count + 1))
    
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}Running Test $test_count: $test_name${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Run the test and capture exit code
    if bash "$test_script"; then
        test_results["$test_name"]="PASSED"
        passed_count=$((passed_count + 1))
        echo ""
        echo -e "${GREEN}✓ Test $test_count PASSED: $test_name${NC}"
    else
        test_results["$test_name"]="FAILED"
        failed_count=$((failed_count + 1))
        echo ""
        echo -e "${RED}✗ Test $test_count FAILED: $test_name${NC}"
        
        # Ask if user wants to continue
        echo ""
        read -p "Continue with remaining tests? [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
            echo "Test suite aborted by user."
            display_summary
            exit 1
        fi
    fi
    
    echo ""
    echo -e "${YELLOW}Press Enter to continue to next test...${NC}"
    read
}

# Function to display final summary
display_summary() {
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}Test Suite Summary${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Display individual test results
    for test_name in "${!test_results[@]}"; do
        result="${test_results[$test_name]}"
        if [ "$result" = "PASSED" ]; then
            echo -e "  ${GREEN}✓${NC} $test_name: ${GREEN}PASSED${NC}"
        else
            echo -e "  ${RED}✗${NC} $test_name: ${RED}FAILED${NC}"
        fi
    done
    
    echo ""
    echo -e "${BOLD}Total Tests: $test_count${NC}"
    echo -e "${GREEN}Passed: $passed_count${NC}"
    echo -e "${RED}Failed: $failed_count${NC}"
    echo ""
    
    # Overall result
    if [ $failed_count -eq 0 ]; then
        echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BOLD}${GREEN}ALL TESTS PASSED! 🎉${NC}"
        echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "Your VibeGraph containerized system is working correctly!"
        echo ""
        echo "Next steps:"
        echo "  - Run 'make monitor' to start health monitoring"
        echo "  - Access frontend at http://localhost:3000"
        echo "  - Access backend API at http://localhost:8000"
        echo "  - View API docs at http://localhost:8000/docs"
        return 0
    else
        echo -e "${BOLD}${RED}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BOLD}${RED}SOME TESTS FAILED${NC}"
        echo -e "${BOLD}${RED}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "Please review the failed tests and check:"
        echo "  - Container logs: make logs"
        echo "  - Container status: make ps"
        echo "  - Diagnostics: make diagnose"
        echo ""
        echo "For help, see:"
        echo "  - scripts/README.md"
        echo "  - docs/TROUBLESHOOTING.md"
        return 1
    fi
}

# Main execution
echo -e "${BOLD}${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║   VibeGraph Container Orchestration Test Suite           ║${NC}"
echo -e "${BOLD}${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "This script will run all container orchestration tests in sequence."
echo "Each test validates a different aspect of the system."
echo ""
echo "Tests to run:"
echo "  1. Build Process Validation"
echo "  2. Container Startup and Health Checks"
echo "  3. Health Check Endpoints"
echo "  4. Inter-Container Communication"
echo "  5. Connection Resilience"
echo "  6. API Endpoints End-to-End"
echo ""
echo -e "${YELLOW}Note: Some tests will temporarily stop containers to simulate failures.${NC}"
echo -e "${YELLOW}This is expected behavior.${NC}"
echo ""
read -p "Press Enter to start the test suite..."

# Run all tests in sequence
run_test "Build Process Validation" "./scripts/test-build.sh"
run_test "Container Startup and Health Checks" "./scripts/test-startup.sh"
run_test "Health Check Endpoints" "./scripts/test-health-endpoints.sh"
run_test "Inter-Container Communication" "./scripts/test-inter-container.sh"
run_test "Connection Resilience" "./scripts/test-resilience.sh"
run_test "API Endpoints End-to-End" "./scripts/test-api-endpoints.sh"

# Display final summary
display_summary

# Exit with appropriate code
if [ $failed_count -eq 0 ]; then
    exit 0
else
    exit 1
fi
