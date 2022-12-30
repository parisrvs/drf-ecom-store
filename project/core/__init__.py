from django.conf import settings


APPS = [
    'core.accounts',
    'core.products'
]

for APP in APPS:
    if APP not in settings.INSTALLED_APPS:
        (settings.INSTALLED_APPS).append(APP)
