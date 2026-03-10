#!/bin/bash

# Test script for Stock Market Platform

echo "======================================"
echo "Stock Market Platform - Test Suite"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

# Function to check if service is running
check_service() {
    local name=$1
    local url=$2

    echo -n "Testing $name... "

    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|301\|302"; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

# Function to test API endpoint
test_endpoint() {
    local name=$1
    local endpoint=$2
    local expected_status=$3

    echo -n "Testing $name... "

    status=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL$endpoint")

    if [ "$status" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status)"
        return 1
    fi
}

echo "1. Testing Service Availability"
echo "--------------------------------"

check_service "Backend API" "$API_URL/health"
check_service "Frontend" "$FRONTEND_URL"
check_service "API Documentation" "$API_URL/docs"

echo ""
echo "2. Testing API Endpoints"
echo "------------------------"

test_endpoint "Root endpoint" "/" 200
test_endpoint "Health check" "/health" 200
test_endpoint "Get stocks" "/api/v1/stocks" 200
test_endpoint "Get indices" "/api/v1/indices" 200
test_endpoint "Get news" "/api/v1/news" 200
test_endpoint "Get reports" "/api/v1/reports" 200
test_endpoint "Market overview" "/api/v1/indices/market/overview" 200

echo ""
echo "3. Testing Data Endpoints"
echo "-------------------------"

# Test stock data
echo -n "Testing stock data retrieval... "
response=$(curl -s "$API_URL/api/v1/stocks?limit=5")
if echo "$response" | jq -e '. | length > 0' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (No data or invalid JSON)"
fi

# Test market overview
echo -n "Testing market overview... "
response=$(curl -s "$API_URL/api/v1/indices/market/overview")
if echo "$response" | jq -e 'type == "object"' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (Invalid response format)"
fi

echo ""
echo "4. Testing Database Connection"
echo "-------------------------------"

echo -n "Testing database connectivity... "
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

echo ""
echo "5. Testing Redis Connection"
echo "----------------------------"

echo -n "Testing Redis connectivity... "
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

echo ""
echo "======================================"
echo "Test Suite Complete"
echo "======================================"
echo ""
echo "For more detailed API testing, visit:"
echo "  - Swagger UI: $API_URL/docs"
echo "  - ReDoc: $API_URL/redoc"
echo ""
