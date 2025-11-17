# Makefile for Django CMS
# Simplifies common development tasks

.PHONY: help setup install migrate createsuperuser demo run clean test collectstatic shell docker-build docker-up docker-down clone-site install-scraper

# Default target
help:
	@echo "Django CMS - Available Commands"
	@echo "================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Complete initial setup (recommended for first time)"
	@echo "  make install        - Install Python dependencies"
	@echo "  make migrate        - Run database migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make demo           - Load demo site data"
	@echo ""
	@echo "Website Cloning:"
	@echo "  make install-scraper - Install web scraping dependencies"
	@echo "  make clone-site     - Clone https://info.arhivadefacturi.ro/"
	@echo "  make clone-simple   - Clone using simple scraper (fast)"
	@echo "  make clone-selenium - Clone using Selenium (more reliable)"
	@echo ""
	@echo "Development:"
	@echo "  make run            - Start development server"
	@echo "  make shell          - Open Django shell"
	@echo "  make collectstatic  - Collect static files"
	@echo "  make test           - Run tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove generated files"
	@echo ""

# Setup entire project
setup:
	@echo "Running complete setup..."
	./scripts/setup.sh

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run migrations
migrate:
	@echo "Running migrations..."
	python manage.py migrate

# Create superuser
createsuperuser:
	@echo "Creating superuser..."
	python manage.py createsuperuser

# Load demo data
demo:
	@echo "Loading demo site..."
	python manage.py create_demo_site

# Install scraping dependencies
install-scraper:
	@echo "Installing web scraping dependencies..."
	pip install -r requirements_scraping.txt
	@echo "✓ Scraping tools installed"

# Clone website (interactive)
clone-site:
	@echo "Cloning https://info.arhivadefacturi.ro/..."
	./scripts/clone_arhiva.sh

# Clone using simple scraper
clone-simple:
	@echo "Cloning website with simple scraper..."
	python manage.py clone_arhiva_site

# Clone using Selenium
clone-selenium:
	@echo "Cloning website with Selenium..."
	python manage.py clone_arhiva_selenium --headless

# Run development server
run:
	@echo "Starting development server..."
	python manage.py runserver

# Open Django shell
shell:
	@echo "Opening Django shell..."
	python manage.py shell

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	python manage.py collectstatic --noinput

# Run tests
test:
	@echo "Running tests..."
	python manage.py test

# Docker build
docker-build:
	@echo "Building Docker images..."
	docker-compose build

# Docker up
docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Waiting for database..."
	@sleep 5
	@echo "Running migrations..."
	docker-compose exec web python manage.py migrate
	@echo ""
	@echo "CMS is running at http://localhost/"

# Docker down
docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf staticfiles/
	@echo "Clean complete!"

# Create migrations
makemigrations:
	@echo "Creating migrations..."
	python manage.py makemigrations

# Show migrations status
showmigrations:
	@echo "Migration status:"
	python manage.py showmigrations

# Backup database (SQLite)
backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	cp db.sqlite3 backups/db_backup_$(shell date +%Y%m%d_%H%M%S).sqlite3
	@echo "Backup created in backups/"

# Check for issues
check:
	@echo "Checking for issues..."
	python manage.py check

# Format code (requires black)
format:
	@echo "Formatting code..."
	black cms_app/ cms_project/

# Lint code (requires flake8)
lint:
	@echo "Linting code..."
	flake8 cms_app/ cms_project/
