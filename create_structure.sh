#!/usr/bin/env bash

set -e

echo "Creating devops-basics project structure..."

# -----------------------------
# Directories
# -----------------------------

mkdir -p backend/app
mkdir -p backend/tests
mkdir -p backend/data

mkdir -p frontend

mkdir -p .github/workflows

# -----------------------------
# Backend files
# -----------------------------

touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/database.py

touch backend/tests/__init__.py
touch backend/tests/test_tasks.py

touch backend/requirements.txt

# -----------------------------
# Frontend files
# -----------------------------

touch frontend/index.html
touch frontend/style.css
touch frontend/app.js

# -----------------------------
# GitHub Actions
# -----------------------------

touch .github/workflows/ci.yml

# -----------------------------
# Root files
# -----------------------------

touch .gitignore
touch README.md

# -----------------------------
# Show structure
# -----------------------------

echo ""
echo "Project structure created:"
echo ""

if command -v tree >/dev/null 2>&1; then
    tree -a -I ".git"
else
    find . -not -path "./.git*" | sort
fi