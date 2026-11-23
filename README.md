# Movies API (Flask)

A small REST API I built in Flask to practice real-world backend skills: CRUD operations, input validation, meaningful status codes, and consistent error handling.

It manages a list of movies in memory and supports adding reviews to a movie through a hardened endpoint: 
POST /movies/<int:movie_id>/reviews.

# Why I built this

I wanted a project simple enough to finish, but real enough to show how I think about APIs:

- Clear, REST-style URLs
- Strong input validation (I don't trust the client)
- Meaningful HTTP status codes
- Consistent JSON error responses
- Tested end-to-end in Postman

# Endpoints

+-------------- Movies (CRUD) ---------------+
| Method | Endpoint	      | Description      |
|________|________________|__________________|
| GET	   | /movies	      | List all movies  |
|________|________________|__________________|
| GET	   | /movies/.      | Get one movie    |
|        | <int:movie_id> | by id            |
|________|________________|__________________|
| POST	 | /movies	      | Create a new     |
|        |                | movie            |
_________|________________|__________________|
| PUT	   | /movies/       | Update existing  |
|        | <int:movie_id>	| movie            |
|________|________________|__________________|
| DELETE | /movies/       | Delete a movie   |
|        | <int:movie_id>	|                  |
+--------------------------------------------+

# Reviews
+--------------------------------------------+
| Method |	Endpoint	    |    Description   |
|________|________________|__________________|
| POST	 | /movies/       | Add a review to  |
|        | <int:movie_id> | a movie          |
|        | /reviews       |                  |
+--------------------------------------------+

# Data model
--- A movie looks like this: ---
{
  "id": 1,
  "title": "Se7en",
  "director": "David Fincher",
  "year": 1995,
  "watched": true
}
--- Validation rules ---
- Required fields: title, director, year, watched
- title and director: non-empty strings
- year: integer (booleans are rejected on purpose)
- watched: boolean

# Reviews endpoint

POST /movies/<int:movie_id>/reviews adds a review to a specific movie and returns the newly created review.

--- Request body ---
{
  "reviewer": "Maliya",
  "rating": 5,
  "comment": "Amazing movie!"
}
--- What it does, in order ---
1. Checks that the movie exists. If there's no movie with that id, it returns 404 Not Found:

{
  "error": "not_found",
  "message": "No movie with id 999 was found."
}

2. Validates the request body.
- The body must be a JSON object
- Required fields: reviewer, rating, comment
- reviewer and comment: strings
- rating: integer (booleans are rejected on   purpose)
* if validation fails, it returns 400 Bad Request:

{
  "error": "validation_error",
  "message": "Field 'comment' is required."
}

3. Creates and returns the review. Each review gets an incrementing id within its movie, is appended to movie["reviews"], and the response is 201 Created with just the new review:

{
  "id": 1,
  "reviewer": "Maliya",
  "rating": 5,
  "comment": "Amazing movie!"
}
* Validation runs before anything is changed, so a bad request never leaves the data in a half-updated state.

# Status codes and error handling
I wanted responses to be predictable, so every endpoint sticks to the same conventions:
+--------------------------------------------+
| Code    | Meaning     | Used for           |
|_________|_____________|____________________|
| 200 OK  | Success     | Reads and updates  |
|_________|_____________|____________________|
| 201     | Resource    | New movies and new |
| Created | created     | reviews            |
|_________|_____________|____________________|
| 201 No  | Success, no | Deletes            |
| Content | body        |                    |
|_________|_____________|____________________|
| 400 Bad | Invalid     | Missing or wrong-  |
| Request | input       | type fields        |
|_________|_____________|____________________|
| 404 Not | Resource    | Unknown movie id   |
| Found   | doesnt exist|                    |
+--------------------------------------------+
* All errors share one JSON envelope

{
  "error": "validation_error",
  "message": "Field 'title' is required."
}

# Tech Stack
- Python
- Flask
- In-memory Python list as the data store (on purpose, so the focus stays on API design and not on the database)
- Postman for manual testing

# Running it locally

1. Clone the repo
git clone https://github.com/maliyadev-dot/movies-api.git
cd movies-api

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Start the server
flask run
or
python app.py

The API will be available at
http://localhost:5000


# How I tested it
I used Postman to check both the success and failure paths. For the reviews endpoint:
+--------------------------------------------+
| Request	                   |Expected result|
|____________________________|_______________|
| POST /movies/1/reviews with| 201 Created   |
| a valid body	             |               |
|____________________________|_______________|
| POST /movies/1/reviews     |400 Bad Request|
| missing comment	           |               |
|____________________________|_______________|
| POST /movies/1/reviews     |400 Bad Request|
| with "rating": "5"         |               |
| (a string)	               |               |
|____________________________|_______________|
| POST /movies/9999/reviews  |404 Not Found  |
|  (movie doesn't exist)	   |               |
+--------------------------------------------+
This confirmed that:
- Validation happens before any state changes
- Errors are clear and consistent
- Status codes match what actually happened

# Known limitations
- Data lives in memory, so it resets every time the server restarts.
- There's no authentication. Anyone who can reach the API can use it.

# What this project shows about me
- I care about clean API design, not just "making it work."
- I think about validation and error handling up front.
- I use Postman to verify real request and response flows.
- I can explain why a status code is the right one, not just guess.

It's a small project, but it's an honest snapshot of how I approach backend work.
