from django.http import JsonResponse

def api_response(success=True, message="", data=None, status=200):
    return JsonResponse({
        "success": success,
        "message": message,
        "data": data or {}
    }, status=status)
