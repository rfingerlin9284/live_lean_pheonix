
import subprocess

def check_process(process_name):
    """Check if a process is running using pgrep"""
    try:
        print(f"Checking for: {process_name}")
        result = subprocess.run(
            ["pgrep", "-af", process_name],
            capture_output=True,
            text=True
        )
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            pid = result.stdout.split()[0]
            return True, pid
        return False, None
    except Exception as e:
        print(f"Exception: {e}")
        return False, None

is_running, pid = check_process("oanda_trading_engine.py")
print(f"Result: {is_running}, PID: {pid}")
