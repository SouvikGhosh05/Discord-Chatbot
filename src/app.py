from flask import Flask
from threading import Thread
from main import bot, Token

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, DiscordBOT!"


def run():
    app.run()


if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(Token)
