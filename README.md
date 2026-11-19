# Movies API

A small Flask REST API and browser-based movie library for practicing CRUD operations.

## Requirements

- Python 3.10 or later
- Dependencies from `requirements.txt`

## Setup and run

Create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the development server from the project directory:

```powershell
flask --app app run --debug
```

Open <http://127.0.0.1:5000/> for the movie library. The API stores data in memory, so changes reset when the server restarts.

## API

All movie objects have an `id`, `title`, `director`, `year`, and `watched` field.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/movies` | List movies; optionally filter with `?director=Name` |
| `GET` | `/movies/<id>` | Get one movie |
| `POST` | `/movies` | Create a movie |
| `PUT` | `/movies/<id>` | Replace a movie |
| `DELETE` | `/movies/<id>` | Delete a movie |

Create and update requests require a JSON object with a non-empty string `title`, a non-empty string `director`, an integer `year`, and a boolean `watched`. Invalid input returns `400`; requests for unknown movie IDs return `404`.

Example request body:

```json
{
  "title": "Arrival",
  "director": "Denis Villeneuve",
  "year": 2016,
  "watched": false
}
```

## Tests

Run the API tests with:

```powershell
python -m unittest discover -v
```
