from pyuac import main_requires_admin

from src.helpers.WindowsBlockUtils import WindowsBlockUtils

# Create new object
global win_block
win_block = WindowsBlockUtils()


# @pytest.fixture(scope="module")
# def win_block():
#     """
#     This will return the WindowsBlockUtils object
#     """
#     return WindowsBlockUtils()


@main_requires_admin
def test_block_suite():
    """
    This will test disable block site
    expected output: 
    +www.example3.com is disabled 
    +there is no example2.com in the list
    """

    # Test the block function - add a site to the block list
    win_block.add_block_site("www.example.com")
    win_block.add_block_site("www.example2.com")
    win_block.add_block_site("www.example3.com")

    # Test the blockUtil function
    win_block.disable_block_site("www.example3.com")
    win_block.remove_block_site("www.example2.com")
    win_block.enable_block_site("www.example.com")


def test_check_hosts_file():
    # Read the file and check if the content is correct
    with open('C:/Windows/System32/drivers/etc/hosts', "r") as f:
        content = f.read()
        assert "www.example.com" in content
        assert "www.example2.com" not in content
        assert "# 127.0.0.1 www.example3.com" in content

# @main_requires_admin
# def test_remove_block_site(win_block: WindowsBlockUtils):
#     # Get the list of blocked sites
#     win_block.list_block_sites()
#     assert "www.example.com" not in win_block.blocked_sites
