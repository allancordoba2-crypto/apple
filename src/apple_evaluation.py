# apple_evaluation.py - macOS Diagnostic Orchestrator
import os
import sys
import json
import logging
import platform
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('AppleEvaluation')

def run_zsh_diagnostics(script_path: Optional[str] = None) -> Dict[str, Any]:
    if script_path is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base, 'scripts', 'SourceApple.zsh')
    
    if platform.system() != 'Darwin':
        logger.info('Non-macOS (%s). Using fallback diagnostics.', platform.system())
        return {
            'computer_name': platform.node(),
            'hardware_model': 'Simulated Device',
            'os_version': platform.release(),
            'os_build': '24A335',
            'architecture': platform.machine(),
            'kernel': platform.version(),
            'boot_storage': '/dev/disk3s1 465Gi 120Gi 320Gi 28%'
        }
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f'Diagnostic script not found: {script_path}')
    
    result = subprocess.run(
        ['/bin/zsh', script_path],
        capture_output=True,
        text=True,
        check=True,
        timeout=15
    )
    return json.loads(result.stdout)

def show_applescript_dialog(title: str, message: str) -> bool:
    if platform.system() != 'Darwin':
        logger.info('[AppleScript Simulation] %s: %s', title, message)
        return True
    
    clean_title = title.replace('"', '')
    clean_msg = message.replace('"', '')
    script = f'display dialog "{clean_msg}" with title "{clean_title}" buttons {{"OK"}} default button "OK"'
    try:
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
        return True
    except Exception as e:
        logger.warning('AppleScript dialog failed: %s', e)
        return False

def generate_report(data: Dict[str, Any]) -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return (
        f'# macOS System Diagnostic Report
'
        f'**Date:** {now}
'
        f'**Mode:** Read-Only Verification

'
        f'---

'
        f'- **Computer Name:** {data.get("computer_name", "N/A")}
'
        f'- **Hardware Model:** {data.get("hardware_model", "N/A")}
'
        f'- **macOS Version:** {data.get("os_version", "N/A")} (Build {data.get("os_build", "N/A")})
'
        f'- **Architecture:** {data.get("architecture", "N/A")}
'
        f'- **Kernel:** {data.get("kernel", "N/A")}
'
        f'- **Boot Storage:** {data.get("boot_storage", "N/A")}

'
        f'---
'
        f'*Report generated safely without system modifications.*
'
    )

def main():
    logger.info('Starting Apple Evaluation Diagnostic...')
    data = run_zsh_diagnostics()
    report = generate_report(data)
    print(report)
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
    os.makedirs(out_dir, exist_ok=True)
    report_file = os.path.join(out_dir, f'diagnostic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info('Report saved to: %s', report_file)
    
    summary = f'macOS {data.get("os_version", "")} ({data.get("architecture", "")})
Storage: {data.get("boot_storage", "")}'
    show_applescript_dialog('Diagnostic Complete', summary)

if __name__ == '__main__':
    main()
