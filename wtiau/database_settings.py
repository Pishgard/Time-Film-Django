# Sqlite
from pathlib import Path
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Postgres
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'royalmelk',
#         'USER': 'postgres',
#         'PASSWORD': '12345',
#         'HOST': 'localhost',
#     }
# }