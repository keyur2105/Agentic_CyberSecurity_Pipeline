import asyncio
from collections import deque
from langgraph.graph import StateGraph
from pydantic import BaseModel
from .Security_Scan import scanning  

class SecurityState(BaseModel):
    target: str
    results: dict = {}

class SecurityPipeline:
    def __init__(self, target):
        self.target = target
        self.task_queue = deque(["nmap", "gobuster", "ffuf", "sqlmap"])
        self.results = {}

    async def execute_task(self, tool):
        print(f"⚙️ Executing {tool} on {self.target}...")
        result = await scanning(tool, self.target)  
        self.results[tool] = result
        print(f"✅ {tool} scan completed.")

        if tool == "nmap" and "open" in result:
            self.task_queue.append("sqlmap")  # Dynamically add SQLMap if ports are open

    async def run_pipeline(self):
        while self.task_queue:
            tool = self.task_queue.popleft()
            await self.execute_task(tool)

        print(f"✅ Full scan completed. Results: {self.results}")
        return self.results

async def async_scan(target):
    print(f"🚀 Starting security scan on {target}...")
    pipeline = SecurityPipeline(target)
    return await pipeline.run_pipeline()
