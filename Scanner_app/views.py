from django.shortcuts import render
from django.http import JsonResponse
import asyncio
from .Security_Pipeline import SecurityPipeline

def home(request):
    return render(request, "index.html")


async def start_scanning(request):
    if request.method == "GET":
        
        target = request.GET.get("target", "").strip()
        
        if not target:
            return JsonResponse({"error": "Invalid input"}, status=400)

        pipeline = SecurityPipeline(target)
        results = await pipeline.run_pipeline()
        
        return render(request, "index.html",{"results": results})
    
