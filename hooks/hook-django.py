# Custom hook-django.py — overrides the built-in one to avoid NoneType crash
# on non-existent migration modules.

import glob
import os

from PyInstaller import log as logging
from PyInstaller.utils import hooks
from PyInstaller.utils.hooks import django

logger = logging.getLogger(__name__)

# Collect everything from django, ignoring errors in sub-modules
datas, binaries, hiddenimports = hooks.collect_all('django', on_error="ignore")

root_dir = django.django_find_root_dir()
if root_dir:
    logger.info('Django root directory %s', root_dir)

    settings_py_imports = django.django_dottedstring_imports(root_dir)
    for submod in settings_py_imports:
        hiddenimports.append(submod)
        hiddenimports += hooks.collect_submodules(submod)

    package_name = os.path.basename(root_dir)
    default_settings_module = f'{package_name}.settings'
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', default_settings_module)
    hiddenimports += [
        settings_module,
        package_name + '.urls',
        package_name + '.wsgi',
        'http.cookies',
        'html.parser',
    ]

    logger.info('Collecting Django migration scripts.')
    migration_modules = [
        # Only include modules that actually exist on disk
        'django.contrib.admin.migrations',
        'django.contrib.auth.migrations',
        'django.contrib.contenttypes.migrations',
        'django.contrib.sessions.migrations',
        'django.contrib.sites.migrations',
    ]

    # Add installed app migrations
    try:
        installed_apps = hooks.get_module_attribute(settings_module, 'INSTALLED_APPS')
        if installed_apps:
            migration_modules.extend(set(app + '.migrations' for app in installed_apps))
    except Exception as e:
        logger.warning('Could not get INSTALLED_APPS: %s', e)

    for mod in migration_modules:
        parts = mod.split('.', 1)
        if len(parts) < 2:
            continue
        mod_name, bundle_name = parts
        # Safely get the module file — skip if it doesn't exist
        try:
            mod_file = hooks.get_module_file_attribute(mod_name)
            if mod_file is None:
                logger.warning('Skipping migration module (not found): %s', mod_name)
                continue
            mod_dir = os.path.dirname(mod_file)
            bundle_dir = bundle_name.replace('.', os.sep)
            pattern = os.path.join(mod_dir, bundle_dir, '*.py')
            files = glob.glob(pattern)
            for f in files:
                datas.append((f, os.path.join(mod_name, bundle_dir)))
        except Exception as e:
            logger.warning('Skipping migration module %s: %s', mod, e)

    datas += hooks.collect_data_files(package_name)

    root_dir_parent = os.path.dirname(root_dir)
    for p in ['*.db', 'db.*']:
        for f in glob.glob(os.path.join(root_dir_parent, p)):
            datas.append((f, '.'))
else:
    logger.warning('No django root directory could be found!')
