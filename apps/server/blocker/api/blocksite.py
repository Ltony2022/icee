from django.http import HttpResponse
import sys
import os


from src.helpers.WindowsBlockUtils import WindowsBlockUtils


# GET /api/blockingList/
def block_site(request):
    """
    A function that returns a list of sites that are blocked by the user.
    :return:
    """
    win_block = WindowsBlockUtils()

    # TODO: remove this dummy data add when the actual data is available
    testData(win_block)

    # Create new object
    return_data = win_block.return_all_blocked_sites()
    return_data = [site[0] for site in return_data]  # Return only the site name
    # print the list of blocked sites for testing
    print(return_data)
    return HttpResponse("<h1>Page was found</h1>")


def testData(win_block):
    win_block.add_block_site("www.example.com")
    win_block.add_block_site("www.example2.com")
    win_block.add_block_site("www.example3.com")
