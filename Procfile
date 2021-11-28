worker: python3 main.py
web: gunicorn -w 4 --pythonpath src --bind 0.0.0.0:$PORT web/app:app --preload