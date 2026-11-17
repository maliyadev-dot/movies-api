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

@app.route("/test-body", methods=["POST"])
def test_body():
    data = request.get_json()
    return {
        "parsed": data,
        "title_field": data["title"] if data else None
    }

    # if we got here, no movie matched
    return jsonify({
            "error": "Not found",
            "message": f"No movie with id {movie_id} was found."
        }), 404

@app.route("/movies", methods=["POST"])
def create_movie():
    movie_data = request.get_json()

    response_body = {
        "message": "Movie created successfully",
        "received": movie_data
    }

    return jsonify(response_body), 201