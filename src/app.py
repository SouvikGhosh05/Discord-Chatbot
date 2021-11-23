from flask import Flask
from threading import Thread
from main import bot, Token

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, DiscordBOT!"


def run():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(Token)
