#!/usr/bin/env python

import os
import sys

from optparse import OptionParser

from django.conf import settings
from django.core.management import call_command


def main():
    parser = OptionParser()
    parser.add_option("--DATABASE_ENGINE", dest="DATABASE_ENGINE", default="sqlite3")
    parser.add_option("--DATABASE_NAME", dest="DATABASE_NAME", default="")
    parser.add_option("--DATABASE_USER", dest="DATABASE_USER", default="")
    parser.add_option("--DATABASE_PASSWORD", dest="DATABASE_PASSWORD", default="")
    parser.add_option("--SITE_ID", dest="SITE_ID", type="int", default=1)

    options, args = parser.parse_args()

    app_path = 'mangopay'
    parent_dir, app_name = os.path.split(app_path)
    sys.path.insert(0, parent_dir)

    settings.configure(**{
        "DATABASES": {
            'default': {
                "ENGINE": 'django.db.backends.%s' % options.DATABASE_ENGINE,
                "NAME": options.DATABASE_NAME,
                "USER": options.DATABASE_USER,
                "PASSWORD": options.DATABASE_PASSWORD,
            }
        },
        "SITE_ID": options.SITE_ID,
        "ROOT_URLCONF": app_name + ".urls",
        "TEMPLATE_LOADERS": (
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
            "django.template.loaders.eggs.Loader",
        ),
        "TEMPLATE_DIRS": (
            os.path.join(os.path.dirname(__file__),
                         "paypaladaptive/templates"),
        ),
        "INSTALLED_APPS": (
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            app_name,
        ),
        "MANGOPAY_PAGE_DEFAULT_STORAGE": True,
        "LOGGING": {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                              '%(thread)d %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                }
            },
            'loggers': {
                app_name: {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'propagate': True,
                }
            }
        }
    })
    call_command("test", app_name)

if __name__ == "__main__":
    main()
