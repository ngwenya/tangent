# settings/local.py
from settings.base import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'hr.sqlite3'),
    }
}

# email backend for local email storage

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails/hr-leave-messages'  # file system directory for keeping dummy emails
