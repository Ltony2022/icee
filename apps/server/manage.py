#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# import pyuac


def main():
    """Run administrative tasks."""
    # add env variable
    os.environ.setdefault('DJANGO_COLORS', 'dark')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    # Set the path to the Django project
    # sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    # add src to python path
    path_to_add = get_source_directory()
    # if (os.path.exists(path_to_add)):
    sys.path.append(path_to_add)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def get_source_directory():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# TODO: research run on background
if __name__ == '__main__':
    # if not pyuac.isUserAdmin():
    #     print("Re-launching as admin!")
    #     pyuac.runAsAdmin()
    # else:
    #     main()  # Already an admin here.
    main()
