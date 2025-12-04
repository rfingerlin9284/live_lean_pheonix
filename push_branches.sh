#!/bin/bash
# Push RICK PHOENIX components to feature branches

set -e
echo "Pushing RICK PHOENIX system components to branches..."

# Return to master
git checkout master

# Create and push foundations branch
echo "Creating feature/foundations..."
git checkout -b feature/foundations || git checkout feature/foundations
git add foundation/*.py logic/*.py 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in foundations"
else
    git commit -m "Add foundation and logic modules"
    git push -u origin feature/foundations
fi

# Create and push strategies branch  
echo "Creating feature/strategies..."
git checkout master
git checkout -b feature/strategies || git checkout feature/strategies
git add strategies/*.py strategies_new/*.py wolf_packs/ 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in strategies"
else
    git commit -m "Add trading strategies"
    git push -u origin feature/strategies
fi

# Create and push dashboards branch
echo "Creating feature/dashboards..."
git checkout master
git checkout -b feature/dashboards || git checkout feature/dashboards
git add dashboard/*.py dashboard/*.html backend.py rbotzilla_*.py 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in dashboards"
else
    git commit -m "Add dashboard and monitoring interfaces"
    git push -u origin feature/dashboards
fi

# Create and push utilities branch
echo "Creating feature/utilities..."
git checkout master
git checkout -b feature/utilities || git checkout feature/utilities
git add util/*.py utils/*.py 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in utilities"
else
    git commit -m "Add utility modules"
    git push -u origin feature/utilities
fi

# Create and push hive-mind branch
echo "Creating feature/hive-mind..."
git checkout master
git checkout -b feature/hive-mind || git checkout feature/hive-mind
git add hive/*.py rick_hive/ 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in hive-mind"
else
    git commit -m "Add hive mind consensus system"
    git push -u origin feature/hive-mind
fi

# Create and push documentation branch
echo "Creating docs/comprehensive..."
git checkout master
git checkout -b docs/comprehensive || git checkout docs/comprehensive
git add *.md docs/ 2>/dev/null || true
if git diff --staged --quiet; then
    echo "No changes in documentation"
else
    git commit -m "Add comprehensive documentation"
    git push -u origin docs/comprehensive
fi

git checkout master
echo "Branch push complete!"
