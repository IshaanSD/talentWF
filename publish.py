#!/usr/bin/env python3
"""
Script to build and publish talenWF to PyPI.
"""

import subprocess
import sys
import os
import shutil
import platform
from pathlib import Path

def check_and_install_dependencies(python_cmd):
    """Check if required dependencies are installed and install them if missing."""
    required_packages = ["build", "twine", "setuptools", "wheel"]
    missing_packages = []
    
    print("[INFO] Checking dependencies...")
    
    for package in required_packages:
        try:
            result = subprocess.run([python_cmd, "-c", f"import {package}"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                missing_packages.append(package)
            else:
                print(f"[SUCCESS] {package} is available")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing_packages.append(package)
    
    if missing_packages:
        print(f"[INFO] Missing packages: {', '.join(missing_packages)}")
        print("[INFO] Installing missing dependencies...")
        
        try:
            install_cmd = [python_cmd, "-m", "pip", "install"] + missing_packages
            result = subprocess.run(install_cmd, check=True, capture_output=True, text=True, timeout=300)
            print(f"[SUCCESS] Installed: {', '.join(missing_packages)}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install dependencies: {e.stderr}")
            print(f"[INFO] Try installing manually: {python_cmd} -m pip install {' '.join(missing_packages)}")
            return False
        except subprocess.TimeoutExpired:
            print("[ERROR] Installation timed out")
            return False
    
    return True

def get_python_cmd():
    """Get the correct Python command for the current platform."""
    # Try different Python commands in order of preference
    python_commands = ["python3", "python", "py"]
    
    for cmd in python_commands:
        if shutil.which(cmd):
            # Test if it's actually Python 3
            try:
                result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and "Python 3" in result.stdout:
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
    
    # If no Python 3 found, try the current interpreter
    if sys.executable:
        return sys.executable
    
    print("[ERROR] No Python 3 installation found")
    print("Please install Python 3 and ensure it's in your PATH")
    print("Available commands checked:", python_commands)
    sys.exit(1)

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"[INFO] {description}...")
    print(f"[DEBUG] Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=300)
        print(f"[SUCCESS] {description} completed successfully")
        if result.stdout and result.stdout.strip():
            print(f"[OUTPUT] {result.stdout.strip()}")
        return True
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {description} timed out after 5 minutes")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed with exit code {e.returncode}")
        if e.stderr:
            print(f"[ERROR] {e.stderr}")
        if e.stdout:
            print(f"[OUTPUT] {e.stdout}")
        return False
    except Exception as e:
        print(f"[ERROR] {description} failed with unexpected error: {e}")
        return False

def clean_build_dirs():
    """Clean build directories in a cross-platform way."""
    build_dirs = ["dist", "build"]
    egg_info_patterns = ["*.egg-info", "*.egg-info/"]
    
    for dir_name in build_dirs:
        if Path(dir_name).exists():
            print(f"[INFO] Removing {dir_name}/")
            shutil.rmtree(dir_name, ignore_errors=True)
    
    # Remove egg-info directories
    for pattern in egg_info_patterns:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                print(f"[INFO] Removing {path}/")
                shutil.rmtree(path, ignore_errors=True)

def main():
    """Main publishing workflow."""
    print("Publishing talenWF to PyPI")
    print("=" * 50)
    print(f"[INFO] Platform: {platform.system()} {platform.release()}")
    print(f"[INFO] Python version: {sys.version}")
    
    # Get the correct Python command
    python_cmd = get_python_cmd()
    print(f"[INFO] Using Python command: {python_cmd}")
    
    # Check and install dependencies if needed
    if not check_and_install_dependencies(python_cmd):
        return 1
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("[ERROR] pyproject.toml not found. Run this script from the package root.")
        return 1
    
    # Clean previous builds
    print("[INFO] Cleaning previous builds...")
    clean_build_dirs()
    
    # Build the package
    if not run_command(f"{python_cmd} -m build", "Building package"):
        return 1
    
    # Check the package
    if not run_command(f"{python_cmd} -m twine check dist/*", "Checking package"):
        return 1
    
    # Ask user for upload destination
    print("\n[SUCCESS] Package built successfully!")
    print("Choose upload destination:")
    print("1. Test PyPI (recommended for first upload)")
    print("2. Production PyPI")
    print("3. Just build (don't upload)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("\n[INFO] Uploading to Test PyPI...")
        if not run_command(f"{python_cmd} -m twine upload --repository testpypi dist/*", "Uploading to Test PyPI"):
            return 1
        print("\n[SUCCESS] Uploaded to Test PyPI!")
        print("Test installation with:")
        print(f"pip3 install --index-url https://test.pypi.org/simple/ talenWF")
        
    elif choice == "2":
        print("\n[INFO] Uploading to Production PyPI...")
        if not run_command(f"{python_cmd} -m twine upload dist/*", "Uploading to PyPI"):
            return 1
        print("\n[SUCCESS] Uploaded to PyPI!")
        print("Install with: pip3 install talenWF")
        
    elif choice == "3":
        print("\n[SUCCESS] Package built successfully!")
        print("Files created in dist/ directory")
        
    else:
        print("[ERROR] Invalid choice")
        return 1
    
    print("\n[SUCCESS] Done!")
    return 0

if __name__ == "__main__":
    exit(main())
