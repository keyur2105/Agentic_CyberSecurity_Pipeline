import subprocess
from .models import SecurityScan

def Scanning(tool, target):

    commands = {
        "nmap": ["nmap", "-sV", target],
        "gobuster": ["gobuster", "dir", "-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"],
        "ffuf": ["ffuf", "-u", f"{target}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"],
        "sqlmap": ["sqlmap", "-u", target, "--batch", "--level=5"]
    }

    if tool not in commands:
        return "Invalid tool"

    scan = SecurityScan.objects.create(target=target, tool_used=tool, status="running")

    try:
        result = subprocess.run(commands[tool], capture_output=True, text=True, timeout=300)
        scan.result = result.stdout
        scan.status = "completed"
    except subprocess.TimeoutExpired:
        scan.result = "Scan timed out"
        scan.status = "failed"
    except Exception as e:
        scan.result = f"Error: {str(e)}"
        scan.status = "failed"

    scan.save()
    return scan.result
