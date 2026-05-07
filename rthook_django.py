# Runtime hook: set Django settings env var before anything else imports Django
import os
import sys

# Set the settings module so Django can initialise
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_tutor.settings')

# When running from a PyInstaller bundle, sys._MEIPASS contains the extracted
# data.  We add it to the front of sys.path so Django can find the project apps.
if getattr(sys, 'frozen', False):
    bundle_dir = os.path.dirname(sys.executable)
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)
    # _MEIPASS holds unpacked temp files (templates, static, etc.)
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass and meipass not in sys.path:
        sys.path.insert(0, meipass)
