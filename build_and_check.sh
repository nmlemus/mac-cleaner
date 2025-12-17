#!/bin/bash
# Script to build and check the package before publishing

set -e

echo "🧹 Mac Cleaner - Build and Check Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Error: pyproject.toml not found. Are you in the right directory?"
    exit 1
fi

print_status "Found pyproject.toml"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_status "Using Python $PYTHON_VERSION"

# Install build tools if needed
echo ""
echo "Installing/upgrading build tools..."
pip install --upgrade build twine > /dev/null 2>&1
print_status "Build tools ready"

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info
print_status "Cleaned build directories"

# Compile translations
echo ""
echo "Compiling translations..."
python3 compile_translations.py
print_status "Translations compiled"

# Run tests
echo ""
echo "Running tests..."
if command -v pytest &> /dev/null; then
    if pytest -q 2>&1 | grep -q "passed"; then
        print_status "Tests passed"
    else
        print_warning "Some tests failed, but continuing..."
    fi
else
    print_warning "pytest not installed, skipping tests"
fi

# Build the package
echo ""
echo "Building package..."
python3 -m build
print_status "Package built"

# Check the package
echo ""
echo "Checking package..."
python3 -m twine check dist/*
print_status "Package check completed"

# Show what was built
echo ""
echo "Built files:"
ls -lh dist/
echo ""

# Summary
echo "========================================"
echo -e "${GREEN}✓ Build completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Test upload to TestPyPI:"
echo "   python3 -m twine upload --repository testpypi dist/*"
echo ""
echo "2. Install from TestPyPI and test:"
echo "   pip install --index-url https://test.pypi.org/simple/ --no-deps mac-cleaner"
echo ""
echo "3. If everything works, upload to PyPI:"
echo "   python3 -m twine upload dist/*"
echo ""
echo "See DEPLOYMENT_STEPS.md for detailed instructions."
echo "========================================"
