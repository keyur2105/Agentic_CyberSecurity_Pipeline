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
        """Execute a scanning tool asynchronously."""
        print(f"⚙️ Executing {tool} on {self.target}...")
        result = await scanning(tool, self.target)  
        self.results[tool] = result

        if tool == "nmap" and "open" in result:
            self.task_queue.append("sqlmap")  # Dynamically add SQLMap if ports are open

    async def run_pipeline(self):
        """Run security scanning pipeline asynchronously."""
        while self.task_queue:
            tool = self.task_queue.popleft()
            await self.execute_task(tool)

        return self.results

async def async_scan(target):
    """Helper function to handle async scanning."""
    pipeline = SecurityPipeline(target)
    return await pipeline.run_pipeline()
