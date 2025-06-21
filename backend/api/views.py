from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json

# Global in-memory store (resets on server restart)
CANDIDATES = [
    {
        "id": 1,
        "name": "Elena Lasconi",
        "image": "/images/lasconi.jpg",
        "party": "USR",
        "description": "O tzatza",
    },
    # add initial candidates if you want
]

@csrf_exempt
def candidates_list(request):
    if request.method == "GET":
        return JsonResponse(CANDIDATES, safe=False)
    
    if request.method == "POST":
        data = json.loads(request.body)
        new_id = max([c["id"] for c in CANDIDATES], default=0) + 1
        data["id"] = new_id
        CANDIDATES.append(data)
        return JsonResponse(data, status=201)
    
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def candidate_detail(request, id):
    candidate = next((c for c in CANDIDATES if c["id"] == id), None)
    if not candidate:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(candidate)

    if request.method == "PUT":
        data = json.loads(request.body)
        candidate.update(data)
        return JsonResponse(candidate)

    if request.method == "DELETE":
        CANDIDATES.remove(candidate)
        return JsonResponse({"deleted": True})

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
