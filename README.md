

# 🚀 Agentic Cybersecurity Pipeline using LangGraph & LangChain.


# Project Overview : 

--> This project is a rule-based agentic cybersecurity pipeline that autonomously scans a given target for security
vulnerabilities using various tools like Nmap, Gobuster, FFUF, and SQLmap. 

--> It is built using LangGraph,LangChain, Django, and Python, and integrates multiple security tools to provide
comprehensive security scanning.


# Features : 
--> Automated Scanning Pipeline : Runs a series of security scans sequentially.
--> Dynamic Task Execution : Adds SQLMap dynamically based on open ports found by Nmap. 
--> Asynchronous Execution : Uses Python's asyncio for non-blocking execution. 
--> Django-based API : Provides a simple web interface for scanning. 
--> Error Handling & Logging : Manages errors, logs outputs, and ensures robustness.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/keyur2105/Agentic_CyberSecurity_Pipeline.git


# Projects Structure/Root :

CyberSecurity_Pipeline/
│-- Scanner_app/
│   ├── Security_Pipeline.py  # Core pipeline logic using LangGraph
│   ├── Security_Scan.py      # Security tool execution logic
│   ├── views.py              # Django views handling requests
│   ├── templates/
│   │   ├── Scan_Result.html  # Frontend UI for viewing results
│   ├── static/
│   │   ├── styles.css        # CSS for UI styling
│   ├── urls.py               # Django URL configuration
│   ├── models.py             # Database models (if required)
│-- requirements.txt          # Required dependencies
│-- scan_results.json         # Stores past scan results
│-- README.md                 # Project documentation


# Installation & Setup : 
Ensure you have the following installed:

--> Python 3.11
--> Django
--> Nmap, Gobuster, FFUF, SQLmap (Ensure they are installed and accessible via the system path)
--> LangGraph & LangChain


# Security Tools Used : 

--> Nmap : Scans open ports & services 
--> Gobuster : Directory brute-forcing 
--> FFUF : Web fuzzing 
--> SQLmap : SQL injection testing

# How It Works this Project :

Security_Pipeline.py 
--> SecurityPipeline Class: Manages the scanning process using a task queue. 
--> execute_task(): Runs each tool asynchronously. 
--> run_pipeline(): Iterates through the task queue and executes scans dynamically.

Security_Scan.py 
--> scanning(): Executes security tools using asyncio.create_subprocess_exec(). 
--> Error Handling: Handles missing tools, timeouts, and subprocess failures.

views.py 
--> start_scanning(): Handles API requests and triggers async_scan(). 
--> async_scan(): Calls SecurityPipeline asynchronously and returns results.
