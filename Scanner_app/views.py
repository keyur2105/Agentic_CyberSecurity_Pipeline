from django.shortcuts import render
from django.http import JsonResponse
import asyncio  
from asgiref.sync import async_to_sync
from .Security_Pipeline import async_scan, load_existing_results, save_results

def home(request):
    return render(request, "Scan_Result.html")

def start_scanning(request):
    if request.method == "GET":  
        target = request.GET.get("target", "").strip()  
        if not target:
            return JsonResponse({"error": "Invalid input"}, status=400)

        try:
            # Run async scanning function in a separate thread using async_to_sync
            results = async_to_sync(async_scan)(target)
            
            all_results = load_existing_results()
            count = len(all_results) + 1
            scan_entry = {"id": count, "target": target, "data": results}
            all_results.append(scan_entry)
            
            save_results(all_results)
            
            return JsonResponse({"message": f"The {target} has been scanned successfully and you can see the result in the {scan_results.json} file."})  

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  

    return JsonResponse({"error": "Invalid request method"}, status=405)
