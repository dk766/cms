#!/bin/bash
# Quick script to clone https://info.arhivadefacturi.ro/

set -e

echo "======================================"
echo "  Clone Arhiva de Facturi Website"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Run ./scripts/setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if scraping requirements are installed
if ! python -c "import beautifulsoup4" 2>/dev/null; then
    echo "Installing scraping dependencies..."
    pip install -r requirements_scraping.txt
fi

# Ask user which method to use
echo "Choose cloning method:"
echo "1) Simple scraper (fast, may be blocked)"
echo "2) Selenium scraper (slower, more reliable)"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo "Running simple scraper..."
        python manage.py clone_arhiva_site
        ;;
    2)
        echo ""
        echo "Running Selenium scraper..."

        # Check if Selenium is installed
        if ! python -c "import selenium" 2>/dev/null; then
            echo "Installing Selenium..."
            pip install -r requirements_scraping.txt
        fi

        python manage.py clone_arhiva_selenium --headless
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "  Cloning Complete!"
echo "======================================"
echo ""
echo "Start the server with:"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  http://localhost:8000/"
echo ""
