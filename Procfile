release: python manage.py migrate --noinput
web: gunicorn project.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery -A project worker -l info
