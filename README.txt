=====
Django-Rsync
=====

django-rsync is a simple deployment script using rsync for django projects.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_rsync" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'django_rsync',
      )

2. Crate the config files for syncing in the folder you want with this format::

      upload.ini:
            [remote]
            user    = user
            host    = host.org
            port    = 22
            dir     = /path/to/folder/

            [rsync_conf]
            filter_file = ./reference/to/rsync/filter.txt

       /reference/to/rsync/filter.txt
             - media/
             - *.pyc
             - projectname/
             - */migrations

3. Run `python manage.py update_remote uload.ini` to upload the changed files.

4. If it is any change in *.py files restart the project in server.