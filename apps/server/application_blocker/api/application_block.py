import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from src.core.exception.django_exception import method_not_allowed
from src.function.application_block import WindowsApplicationBlock

_blocker = WindowsApplicationBlock()


def _read_application_name(request):
    if not request.body:
        raise ValueError("request body is required")
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("invalid JSON payload")

    if not isinstance(payload, dict):
        raise ValueError("invalid JSON payload")

    application_name = payload.get("application") or payload.get("name")
    if not application_name:
        raise ValueError("application field is required")
    return application_name


def list_blocked_application(request):
    if request.method == "GET":
        return JsonResponse({"blocked_applications": _blocker.list_blocked_application()})
    return method_not_allowed(request)


@csrf_exempt
def add_block_application(request):
    if request.method != "POST":
        return method_not_allowed(request)

    try:
        application_name = _read_application_name(request)
        added, applications = _blocker.add_block_application(application_name)
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse(
        {"status": "added" if added else "already_blocked", "applications": applications}
    )


@csrf_exempt
def remove_block_application(request):
    if request.method != "POST":
        return method_not_allowed(request)

    try:
        application_name = _read_application_name(request)
        applications = _blocker.remove_block_application(application_name)
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)
    except KeyError:
        return JsonResponse({"error": "application not found"}, status=404)

    return JsonResponse({"status": "removed", "applications": applications})


@csrf_exempt
def enforce_block(request):
    if request.method == "POST":
        return JsonResponse(
            {"status": "enforced", "applications": _blocker.enforce_block()}
        )
    return method_not_allowed(request)


@csrf_exempt
def disable_block(request):
    if request.method == "POST":
        return JsonResponse(
            {"status": "disabled", "applications": _blocker.disable_block()}
        )
    return method_not_allowed(request)


def list_installed_applications(request):
    if request.method == "GET":
        return JsonResponse(
            {"installed_applications": _blocker.list_installed_applications()}
        )
    return method_not_allowed(request)
