import os
from django.core.exceptions import ImproperlyConfigured

# Common settings always applied
from {{project_name}}.settings.common import *

# APP_ENV environment variable determines environment
app_env = os.environ.get('APP_ENV')
valid_app_envs = ['development', 'dev', 'staging', 'stage', 'stag', 'production', 'prod']

# Apply environment specific settings
if app_env:
    if app_env == 'development' or app_env == 'dev':
        from {{project_name}}.settings.development import *
    elif app_env == 'staging' or app_env == 'stag' or app_env == 'stage':
        from {{project_name}}.settings.staging import *
    elif app_env == 'production' or app_env == 'prod':
        from {{project_name}}.settings.production import *
    else:
        raise ImproperlyConfigured("The APP_ENV must be chosen from: {}".format(", ".join(valid_app_envs)))
else:
    raise ImproperlyConfigured("The APP_ENV setting must not be empty.")
