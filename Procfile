worker: python3 main.py
web: gunicorn -w 4 --bind 0.0.0.0:$PORT app:app --preload