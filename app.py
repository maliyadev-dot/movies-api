from flask import Flask, jsonify, send_from_directory, request
from movies_data import movies
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# --- helpers ---

def validation_error(message):
    return jsonify({
        "error": "validation_error",
        "message": message
    }), 400

def validate_movie_data(movie_data):
    if not isinstance(movie_data, dict):
        return None, "Request body must be a JSON object."

    required_fields = ["title", "director", "year", "watched"]
    for field in required_fields:
        if field not in movie_data:
            return None, f"Field '{field}' is required."

    if not isinstance(movie_data["title"], str):
        return None, "Field 'title' must be a string."

    if not isinstance(movie_data["director"], str):
        return None, "Field 'director' must be a string."

    if not isinstance(movie_data["year"], int) or isinstance(movie_data["year"], bool):
        return None, "Field 'year' must be an integer."

    if not isinstance(movie_data["watched"], bool):
        return None, "Field 'watched' must be a boolean."

    if movie_data["title"].strip() == "":
        return None, "Field 'title' cannot be empty."

    if movie_data["director"].strip() == "":
        return None, "Field 'director' cannot be empty."

    return movie_data, None

def not_found_error(message):
    return jsonify({
        "error": "not_found",
        "message": message
    }), 404

# --- routes ---

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/movies")
def list_movies():
    """
    List all movies, optionally filtered by director.
    ---
    parameters:
      - name: director
        in: query
        type: string
        required: false
        description: Filter movies by director name
    responses:
      200:
        description: A JSON array of movies.
    """
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
    return jsonify({
        "error": "Not found",
        "message": f"No movie with id {movie_id} was found."
    }), 404


@app.route("/test-body", methods=["POST"])
def test_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return validation_error("Request body must be a JSON object.")
    return {
        "parsed": data,
        "title_field": data.get("title")
    }

@app.route("/movies", methods=["POST"])
def create_movie():
    movie_data, error = validate_movie_data(request.get_json(silent=True))
    if error:
        return validation_error(error)

    new_movie = {
        **movie_data,
        "id": max((movie["id"] for movie in movies), default=0) + 1
    }
    movies.append(new_movie)

    return jsonify(new_movie), 201

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
            break

    if movie is None:
        return jsonify({
            "error": "Not found",
            "message": f"No movie with id {movie_id} was found."
        }), 404

    movie_data, error = validate_movie_data(request.get_json(silent=True))
    if error:
        return validation_error(error)

    movie["title"] = movie_data["title"]
    movie["director"] = movie_data["director"]
    movie["year"] = movie_data["year"]
    movie["watched"] = movie_data["watched"]

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

@app.route("/movies/<int:movie_id>/reviews", methods=["POST"])
def add_review(movie_id):
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
            break

    if movie is None:
        return jsonify({
            "error": "not_found",
            "message": f"No movie with id {movie_id} was found."
        }), 404

    review_data = request.get_json(silent=True)
    if not isinstance(review_data, dict):
        return validation_error("Request body must be a JSON object.")

    required_fields = ["reviewer", "rating", "comment"]
    for field in required_fields:
        if field not in review_data:
            return validation_error(f"Field '{field}' is required.")

    if not isinstance(review_data["reviewer"], str):
        return validation_error("Field 'reviewer' must be a string.")

    if not isinstance(review_data["rating"], int) or isinstance(review_data["rating"], bool):
        return validation_error("Field 'rating' must be an integer.")

    if not isinstance(review_data["comment"], str):
        return validation_error("Field 'comment' must be a string.")

    new_review = {
        **review_data,
        "id": max((review.get("id", 0) for review in movie.get("reviews", [])), default=0) + 1
    }

    if "reviews" not in movie:
        movie["reviews"] = []
    movie["reviews"].append(new_review)

    return jsonify(new_review), 201