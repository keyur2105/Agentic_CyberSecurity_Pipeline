from langgraph.graph import StateGraph
from . Security_Scan import Scanning
from pydantic import BaseModel

class SecurityState(BaseModel):
    target: str
    results: dict = {}

class SecurityPipeline(StateGraph):
    def __init__(self, target):
        # Provide a state schema while initializing
        super().__init__(state_schema=SecurityState)
        
        self.target = target
        self.tasks = ["nmap", "gobuster", "ffuf", "sqlmap"]
        self.results = {}

    def execute_task(self, tool):
        # Dummy implementation
        self.results[tool] = f"Executed {tool} on {self.target}"

    def run_pipeline(self):
        for tool in self.tasks:
            self.execute_task(tool)
        return self.results