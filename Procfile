web: gunicorn -w 4 --pythonpath src --bind 0.0.0.0:$PORT app:app --preload
worker: python3 main.py