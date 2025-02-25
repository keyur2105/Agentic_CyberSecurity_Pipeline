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
    

# async def start_scanning(request):
#     if request.method != "GET":
#         return JsonResponse({"message": "Invalid request method"}, status=405)
    
#     target = request.GET.get("target", "").strip()
#     print("target",target)# Get input safely

#     if not target:
#         return JsonResponse({"error": "Invalid input"}, status=400)

#     # Run the pipeline asynchronously
#     pipeline = SecurityPipeline(target)
#     results = await pipeline.run_pipeline()

#     return JsonResponse({"message": "Scan completed", "results": results})
