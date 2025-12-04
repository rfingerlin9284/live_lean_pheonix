#!/usr/bin/env python3
"""
Helper script to auto-fix common linting and style issues across the repo.
It will try to use ruff, autoflake, isort, and black to fix syntax/format and remove unused imports.
If the tools are missing, the script will attempt to install them into the active Python environment.
"""
import os
import subprocess
import sys

TOOLS = ["ruff", "autoflake", "isort", "black"]

def ensure_tools():
    for tool in TOOLS:
        try:
            subprocess.run([tool, "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            print(f"Installing {tool}... (may require network)")
            subprocess.run([sys.executable, "-m", "pip", "install", tool], check=True)

def run_fixes():
    # Ruff auto-fix
    try:
        print("Running ruff --fix...")
        subprocess.run(["ruff", "check", "--fix", "."], check=True)
    except Exception as e:
        print("ruff failed:", e)

    # Remove unused imports/variables
    try:
        print("Running autoflake to remove unused imports...")
        subprocess.run(["autoflake", "--in-place", "--recursive", "--remove-unused-variables", "--remove-all-unused-imports", "."], check=True)
    except Exception as e:
        print("autoflake failed:", e)

    # Sort imports
    try:
        print("Running isort to sort imports...")
        subprocess.run(["isort", "."], check=True)
    except Exception as e:
        print("isort failed:", e)

    # Format with black
    try:
        print("Running black to format code...")
        subprocess.run(["black", ".", "--fast"], check=True)
    except Exception as e:
        print("black failed:", e)

def main():
    cwd = os.getcwd()
    print(f"Running lint fixers in {cwd}")
    try:
        ensure_tools()
    except Exception as e:
        print("Tool installation failed; continuing with available tools: ", e)
    run_fixes()
    print("Linting/formatting completed. You should run your unit tests and manual checks now.")

if __name__ == '__main__':
    main()
