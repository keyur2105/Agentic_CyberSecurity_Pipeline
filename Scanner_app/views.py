from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .Security_Pipeline import SecurityPipeline
from .models import SecurityScan
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CyberSecurity_Pipeline.settings")
django.setup()

def Home(request):
    return render(request, "index.html")
    
def StartScanning(request):
    if request.method == "GET":
        target = request.GET.get['target']
        target = str(target)
        print("target --> ",target)

        if not target:
            return JsonResponse({"error": "Invalid input"}, status=400)
        else:
            pipeline = SecurityPipeline(target)
            results = pipeline.run_pipeline()

            return JsonResponse({"message": "Scan completed", "results": results})
    return JsonResponse({"message":"Target is not exists"})

