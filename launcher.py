"""
AI Personal Tutor — Desktop App (pywebview)
============================================
The Django web app opens directly inside a native desktop window.
Double-clicking the .exe shows a loading splash, then loads the full app
— no browser, no localhost URL visible to the user.

IMPORTANT: Django runs in a background THREAD (not subprocess) so that
PyInstaller does not re-spawn the .exe recursively.
"""

import os
import sys
import threading
import time
import multiprocessing

# ── Must be called first thing when frozen by PyInstaller ───────────────────
# Without this, multiprocessing (used by Django internals) re-spawns the exe.
if getattr(sys, 'frozen', False):
    multiprocessing.freeze_support()

import webview

# ── Path resolution ─────────────────────────────────────────────────────────
def get_base_dir():
    """Return project root whether running from source or a PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
PORT = 8765
APP_URL = f"http://127.0.0.1:{PORT}"

# ── Ensure Django can find our apps when frozen ─────────────────────────────
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_tutor.settings')
os.environ.setdefault('DJANGO_BASE_DIR', BASE_DIR)


# ── Loading splash HTML ──────────────────────────────────────────────────────
LOADING_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0F0F1A;
      color: #F1F5F9;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      overflow: hidden;
    }
    .container { text-align: center; }
    .icon { font-size: 4rem; display: block; margin-bottom: 1.5rem; }
    h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .sub { color: #94A3B8; margin-bottom: 2.5rem; font-size: 1rem; }
    .spinner {
      width: 48px; height: 48px;
      border: 4px solid #2D2D4E;
      border-top-color: #7C3AED;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 0 auto;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .status { margin-top: 1.5rem; color: #64748B; font-size: 0.875rem; }
  </style>
</head>
<body>
  <div class="container">
    <span class="icon">🎓</span>
    <h1>AI Personal Tutor</h1>
    <p class="sub">Your intelligent learning companion</p>
    <div class="spinner"></div>
    <p class="status">Starting application…</p>
  </div>
</body>
</html>"""

ERROR_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0F0F1A; color: #F1F5F9;
      display: flex; align-items: center;
      justify-content: center; height: 100vh;
    }
    .container { text-align: center; }
    h2 { color: #EF4444; margin-bottom: 1rem; font-size: 1.5rem; }
    p { color: #94A3B8; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Failed to start</h2>
    <p>Could not start the application server.<br>Please check your configuration.</p>
  </div>
</body>
</html>"""


# ── Django server (runs in a thread, NOT a subprocess) ──────────────────────
django_started = threading.Event()
django_error = [None]

def run_django_server():
    """Start Django's runserver inside this same process via a thread.
    This avoids re-spawning the .exe when frozen by PyInstaller."""
    try:
        import django
        from django.core.management import call_command

        # Point Django's BASE_DIR to the bundle/source directory
        # so it can find templates, static, manage.py etc.
        django.setup()
        django_started.set()
        # --noreload is critical: prevents Django from spawning a second
        # watcher process (which would also try to re-launch the exe).
        call_command('runserver', f'127.0.0.1:{PORT}', '--noreload',
                     '--skip-checks')
    except Exception as exc:
        django_error[0] = exc
        django_started.set()   # unblock the waiter even on error


def wait_for_server(timeout=40):
    """Poll the server until it accepts connections."""
    import urllib.request, urllib.error
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(APP_URL, timeout=1)
            return True
        except Exception:
            time.sleep(0.4)
    return False


# ── pywebview callback ───────────────────────────────────────────────────────
def background_loader(window):
    """Called by pywebview after the GUI loop starts.
    Starts Django in a daemon thread and then loads the app URL."""
    server_thread = threading.Thread(target=run_django_server, daemon=True)
    server_thread.start()

    # Wait for django.setup() to complete (or fail)
    django_started.wait(timeout=30)

    if django_error[0]:
        window.load_html(ERROR_HTML)
        return

    # Now wait until the HTTP server is actually accepting requests
    if wait_for_server(timeout=30):
        window.load_url(APP_URL)
    else:
        window.load_html(ERROR_HTML)


# ── Entry point ──────────────────────────────────────────────────────────────
def run():
    window = webview.create_window(
        title="AI Personal Tutor",
        html=LOADING_HTML,
        width=1280,
        height=800,
        min_size=(900, 600),
        resizable=True,
        text_select=True,
    )

    webview.start(
        func=background_loader,
        args=[window],
        debug=False,
    )


if __name__ == "__main__":
    run()
