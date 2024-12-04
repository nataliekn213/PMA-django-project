release: python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic -y
web: gunicorn mysite.wsgi