"""Mode manager for OANDA connector environment switching.
Reads RICK_ENV from .env file to determine practice vs live mode.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
import os
from pathlib import Path

_CURRENT_MODE = 'OFF'
_MODE_HISTORY: List[Dict[str, Any]] = []


def get_mode_info() -> Dict[str, Any]:
    """Get current mode information"""
    env = _read_rick_env()
    return {
        'mode': env.upper() if env else 'PRACTICE',
        'api': True if env == 'live' else False,
        'description': f'OANDA connector in {env} mode'
    }


def switch_mode(mode: str, pin: Optional[int] = None, brokers: Optional[List[str]] = None) -> Dict[str, Any]:
    """Switch trading mode (updates .env file)"""
    global _CURRENT_MODE
    _CURRENT_MODE = mode
    entry = {'mode': mode, 'pin': pin, 'brokers': brokers}
    _MODE_HISTORY.append(entry)
    
    # Update .env file
    env_file = _get_env_file_path()
    if env_file and env_file.exists():
        try:
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            # Update RICK_ENV line
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('RICK_ENV='):
                    lines[i] = f'RICK_ENV={mode.lower()}\n'
                    updated = True
                    break
            
            # If not found, append it
            if not updated:
                lines.append(f'\nRICK_ENV={mode.lower()}\n')
            
            with open(env_file, 'w') as f:
                f.writelines(lines)
            
            return {'ok': True, 'mode': mode, 'updated_env': True}
        except Exception as e:
            return {'ok': False, 'mode': mode, 'error': str(e)}
    
    return {'ok': True, 'mode': mode, 'updated_env': False}


def get_connector_environment(connector: str) -> str:
    """Get environment for a specific connector (returns 'practice' or 'live')"""
    env = _read_rick_env()
    
    # Map to connector format
    if env == 'live':
        return 'live'
    else:
        return 'practice'  # Default to practice for safety


def read_upgrade_toggle() -> bool:
    """Check if upgrade toggle is set to LIVE/CANARY"""
    toggle_file = _get_toggle_file_path()
    if toggle_file and toggle_file.exists():
        try:
            content = toggle_file.read_text().strip().upper()
            return content in ['LIVE', 'CANARY']
        except:
            return False
    return False


def _read_rick_env() -> str:
    """Read RICK_ENV from .env file"""
    env_file = _get_env_file_path()
    if env_file and env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('RICK_ENV='):
                        value = line.split('=', 1)[1].strip().strip('"\'')
                        return value
        except:
            pass
    
    # Also check environment variable
    return os.getenv('RICK_ENV', 'practice')


def _get_env_file_path() -> Optional[Path]:
    """Get path to .env file"""
    # Try to find .env in current directory or parent directories
    current = Path.cwd()
    for _ in range(5):  # Search up to 5 levels
        env_file = current / '.env'
        if env_file.exists():
            return env_file
        current = current.parent
    
    # Try relative to this file
    try:
        this_file = Path(__file__).resolve()
        env_file = this_file.parent.parent / '.env'
        if env_file.exists():
            return env_file
    except:
        pass
    
    return None


def _get_toggle_file_path() -> Optional[Path]:
    """Get path to .upgrade_toggle file"""
    env_file = _get_env_file_path()
    if env_file:
        toggle_file = env_file.parent / '.upgrade_toggle'
        return toggle_file if toggle_file.exists() else None
    return None

