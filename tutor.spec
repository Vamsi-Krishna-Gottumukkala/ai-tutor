# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for AI Personal Tutor (pywebview edition)
Run:  $env:DJANGO_SETTINGS_MODULE="ai_tutor.settings"; .\build_env\Scripts\pyinstaller tutor.spec --clean
Output: dist/AI_Personal_Tutor.exe
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_tutor.settings')

# ── Hidden imports ──────────────────────────────────────────────────────────
hidden_imports = [
    # Django
    'django',
    'django.core.management',
    'django.core.management.commands.runserver',
    'django.core.management.commands.migrate',
    'django.contrib.staticfiles',
    'django.contrib.staticfiles.handlers',
    'django.template.backends.django',
    'django.template.loaders.filesystem',
    'django.template.loaders.app_directories',

    # DB backend
    'psycopg2',
    'psycopg2.extensions',
    'psycopg2._psycopg',
    'django.db.backends.postgresql',

    # Project apps
    'accounts', 'accounts.models', 'accounts.views', 'accounts.urls', 'accounts.forms',
    'subjects', 'subjects.models', 'subjects.views', 'subjects.urls',
    'assessments', 'assessments.models', 'assessments.views', 'assessments.urls',
    'learning', 'learning.models', 'learning.views', 'learning.urls',
    'chatbot', 'chatbot.models', 'chatbot.views', 'chatbot.urls',
    'dashboard', 'dashboard.views', 'dashboard.urls',
    'admin_panel', 'admin_panel.views', 'admin_panel.urls',
    'ml_engine', 'ml_engine.models', 'ml_engine.model',

    # Third-party
    'decouple',
    'allauth',
    'allauth.account',
    'allauth.account.middleware',
    'allauth.account.auth_backends',
    'allauth.socialaccount',
    'allauth.socialaccount.providers',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.google.views',
    'google.generativeai',
    'sklearn',
    'sklearn.ensemble',
    'sklearn.ensemble._forest',
    'sklearn.preprocessing',
    'sklearn.utils._cython_blas',
    'sklearn.neighbors._typedefs',
    'sklearn.tree._utils',
    'joblib',
    'pdfplumber',
    'PIL',
    'dj_database_url',

    # pywebview — Windows uses EdgeChromium (WebView2) via pythonnet/clr
    'webview',
    'webview.platforms',
    'webview.platforms.winforms',
    'webview.platforms.edgechromium',
    'clr_loader',
    'pythonnet',
    'proxy_tools',
    'bottle',
]

# ── Data files to bundle ────────────────────────────────────────────────────
datas = [
    ('templates',   'templates'),
    ('static',      'static'),
    ('.env',        '.'),
    ('ai_tutor',    'ai_tutor'),
    ('accounts',    'accounts'),
    ('subjects',    'subjects'),
    ('assessments', 'assessments'),
    ('learning',    'learning'),
    ('chatbot',     'chatbot'),
    ('dashboard',   'dashboard'),
    ('admin_panel', 'admin_panel'),
    ('ml_engine',   'ml_engine'),
    ('manage.py',   '.'),
]

# Bundle pywebview's own data files (JS bridge etc.)
from PyInstaller.utils.hooks import collect_data_files
datas += collect_data_files('webview')

a = Analysis(
    ['launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=['hooks'],
    hooksconfig={
        'django': {
            'settings': 'ai_tutor.settings',
        }
    },
    runtime_hooks=['rthook_django.py'],
    excludes=['matplotlib', 'notebook', 'IPython', 'spacy', 'tkinter'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI_Personal_Tutor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True,
)
