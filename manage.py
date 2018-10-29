#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    #Force UTC-8. At the end I set the Ubuntu local per https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue
    #import importlib
    ## sys.setdefaultencoding() does not exist, here!
    #importlib.reload(sys)  # Reload does the trick!
    #sys.setdefaultencoding('UTF8')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djabbai.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
