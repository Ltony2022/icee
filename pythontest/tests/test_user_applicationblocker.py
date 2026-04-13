# dependencies
from applicationlist import get_process_list


# setup test variables in test environment
PROGRAM_TO_BLOCK = ""

def test_application_blocker():
    """
    This is test to block application
    """

    # get the process list
    process_list = get_process_list()
    assert process_list is not None

    # assert a certain process is in the list