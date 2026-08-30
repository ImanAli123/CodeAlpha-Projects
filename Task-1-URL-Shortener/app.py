from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)


def init_db():
    connection = sqlite3.connect("urls.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    short_code = ''.join(
        random.choices(characters, k=length)
    )

    return short_code


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten_url():

    original_url = request.form["url"]

    short_code = generate_short_code()

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url)
    )

    connection.commit()
    connection.close()

    short_url = request.host_url + short_code

    return f"""
        <h1>URL Shortened Successfully!</h1>

        <p>Your short URL is:</p>

        <a href="{short_url}" target="_blank">
            {short_url}
        </a>

        <br><br>

        <a href="/">Shorten another URL</a>
    """


@app.route("/<short_code>")
def redirect_to_original(short_code):

    connection = sqlite3.connect("urls.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return redirect(result[0])

    return "Short URL not found", 404


if __name__ == "__main__":
    init_db()

    app.run(debug=True)