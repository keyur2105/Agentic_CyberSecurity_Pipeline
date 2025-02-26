from django.shortcuts import render
from django.http import JsonResponse
import asyncio  
from asgiref.sync import async_to_sync
from .Security_Pipeline import async_scan

data = []

def home(request):
    return render(request, "index.html")

def start_scanning(request):
    if request.method == "POST":  
        target = request.POST.get("target", "").strip()  
        
        if not target:
            return JsonResponse({"error": "Invalid input"}, status=400)

        count = len(data) + 1
        try:
            # Run async scanning function in a separate thread using async_to_sync
            results = async_to_sync(async_scan)(target)

            data.append({
                "id": count,
                "target": target,
                "open_ports": results.get("nmap", "No open ports found"),
                "directories": results.get("gobuster", "No directories found"),
                "sql_injection_vulns": results.get("sqlmap", "No SQL injection vulnerabilities found"),
            })

            return JsonResponse({"message": "success", "id": count, "data": results})  

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  

    return JsonResponse({"error": "Invalid request method"}, status=405)
