# This file the security scanning process and each tool runs sequentially modifies the task queue 
# based on results.
import asyncio
import json
import os
from collections import deque
from .Security_Scan import scanning  

class SecurityPipeline:
    def __init__(self, target):
        self.target = target
        self.task_queue = deque(["nmap", "gobuster", "ffuf", "sqlmap"])
        self.results = {}

    async def execute_task(self, tool):
        print(f"⚙️ Executing {tool} on {self.target}...")
        result = await scanning(tool, self.target)  
        formatted_result = self.format_result(tool, result)
        self.results[tool] = formatted_result
        print(f"✅ {tool} scan completed.")

        if tool == "nmap" and "open" in result.lower():
            self.task_queue.append("sqlmap")  # Dynamically add SQLMap if ports are open

    def format_result(self, tool, result):
        if tool == "nmap":
            return f"Open ports: {', '.join(self.extract_ports(result))}" if "open" in result.lower() else "No open ports found"
        elif tool == "gobuster":
            return f"Directories found: {', '.join(self.extract_directories(result))}" if result else "No directories found"
        elif tool == "sqlmap":
            return "SQL vulnerabilities detected" if "vulnerable" in result.lower() else "No SQL vulnerabilities detected"
        return result  # Default case

    def extract_ports(self, result):
        return [line.split('/')[0] for line in result.split('\n') if "open" in line]

    def extract_directories(self, result):
        return [line.strip() for line in result.split('\n') if "/" in line]

    async def run_pipeline(self):
        while self.task_queue:
            tool = self.task_queue.popleft()
            await self.execute_task(tool)

        print(f"✅ Full scan completed. Results: {self.results}")
        return self.results

async def async_scan(target):
    print(f"🚀 Starting security scan on {target}...")
    pipeline = SecurityPipeline(target)
    scan_results = await pipeline.run_pipeline()
    return scan_results


RESULTS_FILE = "scan_results.json"

def load_previous_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_results(results):
    with open(RESULTS_FILE, "w") as file:
        json.dump(results, file, indent=4)
