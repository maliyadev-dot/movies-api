from flask import Flask, jsonify, send_from_directory
from movies_data import movies

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/movies")
def list_movies():
    return jsonify(movies)