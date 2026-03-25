#!/bin/bash
# Health Check Monitoring Script (Task 21.7)
# This script continuously monitors all health endpoints and displays status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
POLL_INTERVAL=10
LOG_FILE="logs/health-monitor.log"
ALERT_FILE="logs/health-alerts.log"

# Create logs directory if it doesn't exist
mkdir -p logs

# Initialize previous status tracking
declare -A prev_status

# Function to get current timestamp
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Function to log to file
log_to_file() {
    local message=$1
    echo "[$(get_timestamp)] $message" >> "$LOG_FILE"
}

# Function to log alerts
log_alert() {
    local message=$1
    echo "[$(get_timestamp)] ALERT: $message" >> "$ALERT_FILE"
}

# Function to check a health endpoint
check_endpoint() {
    local name=$1
    local url=$2
    
    # Make request with timeout
    response=$(curl -s -w "\n%{http_code}" --max-time 5 "$url" 2>/dev/null)
    status_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    # Determine health status
    if [ "$status_code" = "200" ]; then
        echo "healthy|$status_code"
    elif [ "$status_code" = "503" ]; then
        echo "unhealthy|$status_code"
    elif [ -z "$status_code" ]; then
        echo "unreachable|000"
    else
        echo "degraded|$status_code"
    fi
}

# Function to display status with color
display_status() {
    local name=$1
    local status=$2
    local code=$3
    
    case $status in
        "healthy")
            echo -e "${GREEN}●${NC} $name: ${GREEN}HEALTHY${NC} (${code})"
            ;;
        "unhealthy")
            echo -e "${RED}●${NC} $name: ${RED}UNHEALTHY${NC} (${code})"
            ;;
        "degraded")
            echo -e "${YELLOW}●${NC} $name: ${YELLOW}DEGRADED${NC} (${code})"
            ;;
        "unreachable")
            echo -e "${RED}●${NC} $name: ${RED}UNREACHABLE${NC}"
            ;;
        *)
            echo -e "${YELLOW}●${NC} $name: ${YELLOW}UNKNOWN${NC}"
            ;;
    esac
}

# Function to check for status changes and alert
check_status_change() {
    local name=$1
    local current_status=$2
    local prev="${prev_status[$name]}"
    
    if [ -n "$prev" ] && [ "$prev" != "$current_status" ]; then
        # Status changed - log alert
        local alert_msg="$name status changed: $prev → $current_status"
        log_alert "$alert_msg"
        
        # Display alert in terminal
        echo ""
        echo -e "${BOLD}${YELLOW}⚠ ALERT: $alert_msg${NC}"
        echo ""
    fi
    
    # Update previous status
    prev_status[$name]=$current_status
}

# Function to display header
display_header() {
    clear
    echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${BLUE}║         VibeGraph Health Monitoring Dashboard              ║${NC}"
    echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Last updated: $(get_timestamp)${NC}"
    echo -e "${CYAN}Refresh interval: ${POLL_INTERVAL}s${NC}"
    echo -e "${CYAN}Log file: $LOG_FILE${NC}"
    echo ""
}

# Function to display container status
display_container_status() {
    echo -e "${BOLD}Container Status:${NC}"
    echo ""
    
    # Get container status
    containers=$(docker-compose ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | tail -n +2)
    
    if [ -z "$containers" ]; then
        echo -e "${RED}No containers running${NC}"
    else
        while IFS=$'\t' read -r name status; do
            if echo "$status" | grep -qi "up.*healthy"; then
                echo -e "  ${GREEN}●${NC} $name: ${GREEN}Running (healthy)${NC}"
            elif echo "$status" | grep -qi "up"; then
                echo -e "  ${YELLOW}●${NC} $name: ${YELLOW}Running (no health check)${NC}"
            else
                echo -e "  ${RED}●${NC} $name: ${RED}$status${NC}"
            fi
        done <<< "$containers"
    fi
    echo ""
}

# Function to display health endpoints
display_health_endpoints() {
    echo -e "${BOLD}Health Endpoints:${NC}"
    echo ""
    
    # Check each endpoint
    endpoints=(
        "Basic Health|http://localhost:8000/health"
        "Readiness|http://localhost:8000/health/ready"
        "Database|http://localhost:8000/health/db"
        "Bedrock|http://localhost:8000/health/bedrock"
        "Cache|http://localhost:8000/health/cache"
        "Status|http://localhost:8000/health/status"
    )
    
    for endpoint in "${endpoints[@]}"; do
        IFS='|' read -r name url <<< "$endpoint"
        result=$(check_endpoint "$name" "$url")
        IFS='|' read -r status code <<< "$result"
        
        echo -n "  "
        display_status "$name" "$status" "$code"
        
        # Check for status change
        check_status_change "$name" "$status"
        
        # Log to file
        log_to_file "$name: $status ($code)"
    done
    echo ""
}

# Function to display service connectivity
display_service_connectivity() {
    echo -e "${BOLD}Service Connectivity:${NC}"
    echo ""
    
    # Test frontend → backend
    if docker exec vibegraph-frontend wget --spider -q http://backend-api:8000/health 2>/dev/null; then
        echo -e "  ${GREEN}●${NC} Frontend → Backend: ${GREEN}OK${NC}"
    else
        echo -e "  ${RED}●${NC} Frontend → Backend: ${RED}FAILED${NC}"
    fi
    
    # Test backend → DynamoDB
    if docker exec vibegraph-backend-api curl -sf http://dynamodb-local:8000 > /dev/null 2>&1; then
        echo -e "  ${GREEN}●${NC} Backend → DynamoDB: ${GREEN}OK${NC}"
    else
        echo -e "  ${RED}●${NC} Backend → DynamoDB: ${RED}FAILED${NC}"
    fi
    
    # Test backend → LocalStack
    if docker exec vibegraph-backend-api curl -sf http://localstack:4566/_localstack/health > /dev/null 2>&1; then
        echo -e "  ${GREEN}●${NC} Backend → LocalStack: ${GREEN}OK${NC}"
    else
        echo -e "  ${RED}●${NC} Backend → LocalStack: ${RED}FAILED${NC}"
    fi
    
    echo ""
}

# Function to display recent alerts
display_recent_alerts() {
    if [ -f "$ALERT_FILE" ]; then
        local alert_count=$(wc -l < "$ALERT_FILE")
        if [ "$alert_count" -gt 0 ]; then
            echo -e "${BOLD}${YELLOW}Recent Alerts (last 5):${NC}"
            echo ""
            tail -n 5 "$ALERT_FILE" | while read -r line; do
                echo -e "  ${YELLOW}⚠${NC} $line"
            done
            echo ""
        fi
    fi
}

# Function to display footer
display_footer() {
    echo -e "${CYAN}────────────────────────────────────────────────────────────${NC}"
    echo -e "${CYAN}Press Ctrl+C to exit${NC}"
    echo ""
}

# Trap Ctrl+C to exit gracefully
trap 'echo ""; echo "Monitoring stopped."; exit 0' INT

# Main monitoring loop
echo "Starting health monitoring..."
log_to_file "Health monitoring started"

while true; do
    display_header
    display_container_status
    display_health_endpoints
    display_service_connectivity
    display_recent_alerts
    display_footer
    
    # Wait for next poll
    sleep $POLL_INTERVAL
done
