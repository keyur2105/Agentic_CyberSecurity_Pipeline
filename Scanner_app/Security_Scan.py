import asyncio
import subprocess
import os

async def scanning(tool, target):
    
    WORDLIST_PATH = os.getenv("WORDLIST_PATH", r"C:\wordlists\SecLists\Discovery\Web-Content\common.txt")

    commands = {
        "nmap": ["C:\\Program Files (x86)\\Nmap\\nmap.exe", "-sV", target],
        "gobuster": ["C:\\Users\\pc26\\go\\bin\\gobuster.exe", "dir", "-u", target, "-w", WORDLIST_PATH],
        "ffuf": ["C:\\Users\\pc26\\go\\bin\\ffuf.exe", "-u", f"{target}/FUZZ", "-w", WORDLIST_PATH],
        "sqlmap": ["C:\\Users\\pc26\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\sqlmap.exe", "-u", target, "--batch", "--level=1","--risk=1"]
    }
    
    if tool not in commands:
        return f"❌ Invalid tool: {tool}"

    print(f"⚙️ Running {tool} on {target}...")

    try:
        process = await asyncio.create_subprocess_exec(
            *commands[tool],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        result = stdout.decode().strip() if stdout else stderr.decode().strip()
        
        print(f"✅ {tool} Result:\n{result}")  # Debugging print
        
        return result if result else f"⚠️ No output from {tool}"

    except FileNotFoundError:
        return f"❌ {tool} not installed or not found in PATH"
    except asyncio.TimeoutError:
        return f"⏳ {tool} scan timed out"
    except Exception as e:
        return f"❌ Error running {tool}: {str(e)}"