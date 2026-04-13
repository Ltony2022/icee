from django.http import JsonResponse

from src.core.exception.django_exception import method_not_allowed


def pomodoro(request):
    """
    This function gets the user configuration (to be implemented).
    :param request: Request object
    :return: JSON response - containing the user configuration
    """
    print("[server] received request to start pomodoro")
    print("[debug] request: ", request)
    print("[debug] request.body: ", request.body)
    if request.method == "GET":
        print("[debug] request.GET: ", request.GET)
        return JsonResponse({'pomodoro': 'pomodoro'})
    else:
        return method_not_allowed(request)
