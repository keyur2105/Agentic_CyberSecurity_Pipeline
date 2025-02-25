import asyncio
from collections import deque
from langgraph.graph import StateGraph
from pydantic import BaseModel
from .Security_Scan import scanning  # Ensure proper import

class SecurityState(BaseModel):
    target: str
    results: dict = {}

class SecurityPipeline(StateGraph):
    def __init__(self, target):
        super().__init__(state_schema=SecurityState)

        self.target = target
        self.task_queue = deque(["nmap", "gobuster", "ffuf", "sqlmap"])
        self.results = {}

    async def execute_task(self, tool):
        print(f"⚙️ Executing {tool} on {self.target}...")
        result = await scanning(tool, self.target)  # Run asynchronously
        self.results[tool] = result

        if tool == "nmap" and "open" in result:
            self.task_queue.append("sqlmap")  # Dynamically add SQLMap if ports are open

    async def run_pipeline(self):
        while self.task_queue:
            tool = self.task_queue.popleft()
            await self.execute_task(tool)

        return self.results
