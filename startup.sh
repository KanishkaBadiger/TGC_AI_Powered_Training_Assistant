#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI Training Assistant Startup${NC}"
echo "=================================="

# Check Python installation
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -r backend/requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Backend dependencies installed${NC}"

pip install -r frontend/requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Check if database exists, if not create it
if [ ! -f "database/sqlite/training_assistant.db" ]; then
    echo -e "${YELLOW}🗄️  Creating database...${NC}"
    mkdir -p database/sqlite
    sqlite3 database/sqlite/training_assistant.db < database/schema.sql
    echo -e "${GREEN}✅ Database created${NC}"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Creating .env file...${NC}"
    cp .env.example .env 2>/dev/null || echo "GROQ_API_KEY=your_api_key_here" > .env
    echo -e "${YELLOW}⚠️  Please set your GROQ_API_KEY in .env file${NC}"
fi

echo ""
echo -e "${GREEN}=================================="
echo "✨ Ready to start!${NC}"
echo -e "${GREEN}=================================="
echo ""
echo -e "${YELLOW}Option 1: Start Backend Server${NC}"
echo "Run: cd backend && uvicorn main:app --reload"
echo ""
echo -e "${YELLOW}Option 2: Start Frontend${NC}"
echo "Run: cd frontend && streamlit run main.py"
echo ""
echo -e "${YELLOW}Option 3: Start Both (in separate terminals)${NC}"
echo ""
