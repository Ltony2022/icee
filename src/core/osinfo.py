"""
Check the operating system and the python version
"""

def check_system():
    """Check the operating system and the python version"""
    import platform
    import sys

    if platform.system() != "Windows":
        print("This script is only for Windows OS. Exiting...")
        sys.exit(1)

    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        print("This script requires Python 3.6 or later")
        sys.exit(1)
        
    print("[INFO] System check passed")
    system = platform.system()
    print("[INFO] Current system is: " + system)
    return system
