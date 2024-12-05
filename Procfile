release: python manage.py makemigrations && python manage.py migrate && yes | python manage.py collectstatic
web: gunicorn mysite.wsgi