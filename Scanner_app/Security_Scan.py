import asyncio
import subprocess
from .models import SecurityScan

async def scanning(tool, target):
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
        process = await asyncio.create_subprocess_exec(
            *commands[tool],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        result = stdout.decode().strip() if stdout else stderr.decode().strip()

        scan.result = result
        scan.status = "completed" if process.returncode == 0 else "failed"

    except asyncio.TimeoutError:
        scan.result = "Scan timed out"
        scan.status = "failed"
    except Exception as e:
        scan.result = f"Error: {str(e)}"
        scan.status = "failed"

    scan.save()
    return scan.result
