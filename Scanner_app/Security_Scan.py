import asyncio
import subprocess
from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import Dict, List, Optional

# Define the state schema
class SecurityState(BaseModel):
    target: str
    results: Dict[str, str] = {}
    tasks: List[str] = ["nmap", "gobuster", "ffuf", "sqlmap"]

# Function to run external commands safely
def run_tool(command: List[str]) -> str:  
    try:
        result=subprocess.run(command, capture_output=True, text=True, timeout=300)
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Scan timed out"
    except FileNotFoundError:
        return "Tool not found, ensure it's installed and in PATH"
    except Exception as e:
        return f"Error: {str(e)}"