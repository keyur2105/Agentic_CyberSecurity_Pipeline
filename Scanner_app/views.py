from django.shortcuts import render
from django.http import JsonResponse
from .Security_Pipeline import SecurityPipeline
import asyncio
from asgiref.sync import async_to_sync

data=[]
def home(request):
    return render(request, "index.html")

def scan_target(request):
    count=0
    target = request.GET.get("target","").strip()
    print("target --> ", target)
    
    if not target:
        return JsonResponse({"error": "No target specified"}, status=400)
    
    pipeline = SecurityPipeline(target)
    results = async_to_sync(pipeline.run_pipeline)()

    data.append({
        "id" : count+1,
        "target" : target,
        "open_ports" : results.open_ports,
        "directories" : results.directories,
        "sql_injection_vulns" : results.sql_injection_vulns
    })
    return JsonResponse({"message": "Scan completed", "id": data.id, "data": results.dict()})
