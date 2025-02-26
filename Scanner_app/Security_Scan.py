import asyncio
import subprocess

async def scanning(tool, target):
    """Run security scanning tool asynchronously."""
    commands = {
        "nmap": ["C:\\Program Files (x86)\\Nmap\\nmap.exe", "-sV", target],
        "gobuster": ["C:\\Users\\pc26\\go\\bin\\gobuster.exe", "dir", "-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"],
        "ffuf": ["C:\\Users\\pc26\\go\\bin\\ffuf.exe", "-u", f"{target}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"],
        "sqlmap": ["C:\\Users\\pc26\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\sqlmap.exe", "-u", target, "--batch", "--level=5"]
    }

    if tool not in commands:
        return f"Invalid tool: {tool}"

    try:
        process = await asyncio.create_subprocess_exec(
            *commands[tool],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        result = stdout.decode().strip() if stdout else stderr.decode().strip()

        return result

    except asyncio.TimeoutError:
        return "Scan timed out"
    except Exception as e:
        return f"Error: {str(e)}"
