release: python manage.py db upgrade
web: gunicorn -w 2 -b 0.0.0.0:$PORT "antipodal:create_app()"
