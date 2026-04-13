from django.http import JsonResponse


def method_not_allowed(request):
    return JsonResponse({"error": "method not found"}, status=405)
