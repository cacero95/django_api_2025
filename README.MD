# Run the project en local server
gunicorn backend.wsgi:application --bind 127.0.0.1:8000 --reload
