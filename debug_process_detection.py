
import subprocess
import sys

def check_pgrep():
    print("--- Testing pgrep ---")
    try:
        cmd = ["pgrep", "-af", "oanda_trading_engine.py"]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        print(f"Return Code: {result.returncode}")
        print(f"Stdout: '{result.stdout.strip()}'")
        print(f"Stderr: '{result.stderr.strip()}'")
    except Exception as e:
        print(f"Error: {e}")

def check_ps():
    print("\n--- Testing ps aux ---")
    try:
        cmd = ["ps", "aux"]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        print(f"Return Code: {result.returncode}")
        found = False
        for line in result.stdout.splitlines():
            if "oanda_trading_engine.py" in line and "grep" not in line:
                print(f"MATCH: {line}")
                found = True
        if not found:
            print("No match found in ps aux")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_pgrep()
    check_ps()
