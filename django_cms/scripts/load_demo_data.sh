#!/bin/bash
# Load demo data into Django CMS

set -e

echo "======================================"
echo "   Loading Demo Data"
echo "======================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Load fixtures
echo "Loading demo data..."
python manage.py loaddata demo_data.json

echo ""
echo "✓ Demo data loaded successfully!"
echo ""
echo "Demo site includes:"
echo "  - Homepage with hero section"
echo "  - About page"
echo "  - Services page"
echo "  - Contact page"
echo "  - Navigation menu"
echo "  - Site configuration"
echo ""
echo "Visit http://localhost:8000/ to see the demo site"
echo ""
