#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal

def shutdown(signum, frame):
    # Perform cleanup actions here
    print("Shutting down gracefully...")
    sys.exit(0)

def main():
    """Run administrative tasks."""
    #signal.signal(signal.SIGINT, shutdown)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
    sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
