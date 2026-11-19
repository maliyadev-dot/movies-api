import copy
import unittest

from app import app
from movies_data import movies


class MoviesApiTestCase(unittest.TestCase):
    def setUp(self):
        self.original_movies = copy.deepcopy(movies)
        self.client = app.test_client()

    def tearDown(self):
        movies[:] = self.original_movies

    def valid_movie(self):
        return {
            "title": "Arrival",
            "director": "Denis Villeneuve",
            "year": 2016,
            "watched": False,
        }

    def test_get_unknown_movie_returns_not_found(self):
        response = self.client.get("/movies/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Not found")

    def test_create_rejects_malformed_and_non_object_json(self):
        malformed = self.client.post(
            "/movies", data="{", content_type="application/json"
        )
        non_object = self.client.post("/movies", json=["not", "an", "object"])
        malformed_update = self.client.put(
            "/movies/1", data="{", content_type="application/json"
        )

        self.assertEqual(malformed.status_code, 400)
        self.assertEqual(non_object.status_code, 400)
        self.assertEqual(malformed_update.status_code, 400)
        self.assertEqual(malformed.json["error"], "validation_error")

    def test_create_rejects_boolean_year(self):
        movie_data = self.valid_movie()
        movie_data["year"] = True

        response = self.client.post("/movies", json=movie_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Field 'year' must be an integer.")

    def test_create_update_and_delete_movie(self):
        created = self.client.post("/movies", json=self.valid_movie())

        self.assertEqual(created.status_code, 201)
        movie_id = created.json["id"]

        updated_data = self.valid_movie()
        updated_data["title"] = "Updated Arrival"
        updated = self.client.put(f"/movies/{movie_id}", json=updated_data)
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json["title"], "Updated Arrival")

        deleted = self.client.delete(f"/movies/{movie_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(self.client.get(f"/movies/{movie_id}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
