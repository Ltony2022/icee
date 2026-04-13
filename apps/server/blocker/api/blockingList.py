import sys

sys.path.append('../../')
from django.http import HttpResponse


def blocking_site_list(Request):
    """
    A function that returns a list of sites that are blocked by the user.
    :return:
    """
    print("Blocking site list")
    print(1)
    print(Request)
    return HttpResponse("<h1>Page was found</h1>")
