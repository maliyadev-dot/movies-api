from flask import Flask, jsonify, send_from_directory, request
from movies_data import movies

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/movies")
def list_movies():
    director = request.args.get("director")

    if director:
        filtered_movies = []
        for movie in movies:
            if movie["director"] == director:
                filtered_movies.append(movie)
        return jsonify(filtered_movies)
    return jsonify(movies)

@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    for movie in movies:
        if movie["id"] == movie_id:
            return jsonify(movie), 200

    # if we got here, no movie matched
    return jsonify({
            "error": "Not found",
            "message": f"No movie with id {movie_id} was found."
        }), 404