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

    # 1) Presence validation (keys must exist)
    required_fields = ["title", "director", "year", "watched"]
    for field in required_fields:
        if field not in movie_data:
            return jsonify({
                "error": "validation_error",
                "message": f"Field '{field}' is required."
            }), 400

    # 2) Type validation
    if not isinstance(movie_data["title"], str):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'title' must be a string."
        }), 400

    if not isinstance(movie_data["director"], str):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'director' must be a string."
        }), 400

    if not isinstance(movie_data["year"], int):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'year' must be an integer."
        }), 400

    if not isinstance(movie_data["watched"], bool):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'watched' must be a boolean."
        }), 400

    # 3) Extra: non-empty checks for strings
    if movie_data["title"].strip() == "":
        return jsonify({
            "error": "validation_error",
            "message": "Field 'title' cannot be empty."
        }), 400

    if movie_data["director"].strip() == "":
        return jsonify({
            "error": "validation_error",
            "message": "Field 'director' cannot be empty."
        }), 400

    # 4) If everything is valid, create and store the movie
    new_movie = {
        **movie_data,
        "id": max(movie["id"] for movie in movies) + 1
    }
    movies.append(new_movie)

    return jsonify(new_movie), 201

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    # 1) Find the movie by ID
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
            break

    # 2) If movie not found, return 404
    if movie is None:
        return jsonify({
            "error": "Not found",
            "message": f"No movie with id {movie_id} was found."
        }), 404

    # 3) Read JSON body
    movie_data = request.get_json()

    # 4) Run the SAME validation logic as in create_movie
    required_fields = ["title", "director", "year", "watched"]
    for field in required_fields:
        if field not in movie_data:
            return jsonify({
                "error": "validation_error",
                "message": f"Field '{field}' is required."
            }), 400

    if not isinstance(movie_data["title"], str):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'title' must be a string."
        }), 400

    if not isinstance(movie_data["director"], str):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'director' must be a string."
        }), 400

    if not isinstance(movie_data["year"], int):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'year' must be an integer."
        }), 400
    
    if not isinstance(movie_data["watched"], bool):
        return jsonify({
            "error": "validation_error",
            "message": "Field 'watched' must be a boolean."
        }), 400

    if movie_data["title"].strip() == "":
        return jsonify({
            "error": "validation_error",
            "message": "Field 'title' cannot be empty."
        }), 400

    if movie_data["director"].strip() == "":
        return jsonify({
            "error": "validation_error",
            "message": "Field 'director' cannot be empty."
        }), 400

    # 5) If valid, update the existing movie (keep id)
    movie["title"] = movie_data["title"]
    movie["director"] = movie_data["director"]
    movie["year"] = movie_data["year"]
    movie["watched"] = movie_data["watched"]

    # 6) Return 200 w/ updated movie
    return jsonify(movie), 200

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    # 1) Find the movie by ID
    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            movies.pop(index)
            return "", 204

    # 2) If no movie matched, return the same 404 JSON shape
    return jsonify({
        "error": "Not found",
        "message": f"No movie with id {movie_id} was found."
    }), 404