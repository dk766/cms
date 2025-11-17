#!/bin/bash
# Setup script for Django CMS
# This script automates the initial setup process

set -e  # Exit on error

echo "======================================"
echo "   Django CMS - Setup Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}Error: Python 3.10+ is required. You have $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version detected${NC}"
echo ""

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Setup environment file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env

    # Generate secret key
    secret_key=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

    # Update .env file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$secret_key/" .env
    else
        # Linux
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$secret_key/" .env
    fi

    echo -e "${GREEN}✓ .env file created with secure SECRET_KEY${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Create necessary directories
echo -e "${YELLOW}Creating media directories...${NC}"
mkdir -p media/uploads media/thumbnails media/branding
mkdir -p media/section_backgrounds media/content_blocks media/galleries
echo -e "${GREEN}✓ Media directories created${NC}"
echo ""

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Database migrations completed${NC}"
echo ""

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

# Create superuser
echo -e "${YELLOW}Creating superuser...${NC}"
echo "Please enter superuser details:"
python manage.py createsuperuser

echo ""
echo -e "${GREEN}======================================"
echo "   Setup Complete!"
echo "======================================${NC}"
echo ""
echo "To start the development server:"
echo -e "${YELLOW}  source venv/bin/activate${NC}"
echo -e "${YELLOW}  python manage.py runserver${NC}"
echo ""
echo "Then visit:"
echo -e "${GREEN}  Frontend: http://localhost:8000/${NC}"
echo -e "${GREEN}  Admin:    http://localhost:8000/admin/${NC}"
echo -e "${GREEN}  API:      http://localhost:8000/api/${NC}"
echo ""
