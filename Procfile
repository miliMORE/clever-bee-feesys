web: python manage.py migrate --noinput && python manage.py create_demo_users && python manage.py collectstatic --noinput && gunicorn feesys.wsgi:application --bind 0.0.0.0:$PORT
