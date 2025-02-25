import subprocess
from langgraph.graph import StateGraph
from .Security_Scan import SecurityState, run_tool

# Individual scanning functions
def run_nmap(state: SecurityState) -> SecurityState:
    command = ["C:\\Program Files (x86)\\Nmap\\nmap.exe", "-sV", state.target]
    state.results["nmap"] = run_tool(command)
    return state

def run_sqlmap(state: SecurityState) -> SecurityState:
    command = ["C:\\Users\\pc26\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\sqlmap.exe", "-u", state.target, "--batch", "--level=5"]
    state.results["sqlmap"] = run_tool(command)
    return state

def run_gobuster(state: SecurityState) -> SecurityState:
    command = ["C:\\Users\\pc26\\go\\bin\\gobuster.exe", "dir", "-u", state.target, "-w", "C:\\Tools\\wordlists\\common.txt"]
    state.results["gobuster"] = run_tool(command)
    return state

def run_ffuf(state: SecurityState) -> SecurityState:
    command = ["C:\\Users\\pc26\\go\\bin\\ffuf.exe", "-u", f"{state.target}/FUZZ", "-w", "C:\\Tools\\wordlists\\common.txt"]
    state.results["ffuf"] = run_tool(command)
    return state

# Define the security pipeline
class SecurityPipeline(StateGraph):
    def __init__(self, target: str):
        super().__init__(state_schema=SecurityState)
        self.target = target
        self.add_node("nmap", run_nmap)
        self.add_node("gobuster", run_gobuster)
        self.add_node("ffuf", run_ffuf)
        self.add_node("sqlmap", run_sqlmap)
        
        self.set_entry_point("nmap")
        self.add_edge("nmap", "gobuster")
        self.add_edge("gobuster", "ffuf")
        self.add_edge("ffuf", "sqlmap")
        self.set_finish_point("sqlmap")

    def run_pipeline(self):
        executor = self.compile()
        result = executor.invoke(SecurityState(target=self.target))
        return result.results