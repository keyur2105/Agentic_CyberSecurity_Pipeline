from django.shortcuts import render
from django.http import JsonResponse
import asyncio  
from asgiref.sync import sync_to_async
from .Security_Pipeline import async_scan

data = []

def home(request):
    return render(request, "index.html")

async def start_scanning_async(target):
    """Run security scan asynchronously."""
    return await async_scan(target)

def start_scanning(request):  
    if request.method == "POST":  
        target = request.POST.get("target", "").strip()  
        
        if not target:
            return JsonResponse({"error": "Invalid input"}, status=400)

        count = len(data) + 1
        try:
            # Run async function safely in a separate thread
            results = asyncio.run(start_scanning_async(target))

            data.append({
                "id": count,
                "target": target,
                "open_ports": results.get("nmap", "No open ports found"),
                # "directories": results.get("gobuster", "No directories found"),
                # "sql_injection_vulns": results.get("sqlmap", "No SQL injection vulnerabilities found"),
            })

            return JsonResponse({"message": "success", "id": count, "data": results})  

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  

    return JsonResponse({"error": "Invalid request method"}, status=405)  
