import unittest
from app import create_app
from auth import AuthError, requires_auth


class YourTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        # Set up any necessary test data or context here

    def test_get_movies(self):
        response = self.app.get('/movies')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movies' in data)

    def test_create_movie(self):
        new_movie_data = {
            'title': 'Test Movie',
            'release_date': '2023-08-19'
        }
        response = self.app.post('/movies', json=new_movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movie' in data)

        # Clean up: Delete the created movie
        movie_id = data['movie']['id']
        self.app.delete(f'/movies/{movie_id}')

    def test_update_movie(self):
        # Create a movie first to update
        new_movie_data = {
            'title': 'Test Movie',
            'release_date': '2023-08-19'
        }
        create_response = self.app.post('/movies', json=new_movie_data)
        movie_id = create_response.get_json()['movie']['id']

        updated_movie_data = {
            'title': 'Updated Movie'
        }
        response = self.app.patch(f'/movies/{movie_id}', json=updated_movie_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movie' in data)

        # Clean up: Delete the created movie
        self.app.delete(f'/movies/{movie_id}')

    def test_delete_movie(self):
        # Create a movie first to delete
        new_movie_data = {
            'title': 'Test Movie',
            'release_date': '2023-08-19'
        }
        create_response = self.app.post('/movies', json=new_movie_data)
        movie_id = create_response.get_json()['movie']['id']

        response = self.app.delete(f'/movies/{movie_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in data)

    # I can also add similar test cases for actors endpoints (GET, POST, PATCH, DELETE) if needed

    # Test RBAC behavior for different roles
    def test_get_movies_unauthorized(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer rol_cIg3ZghFe3ALr666'}) # Invalid token
        self.assertEqual(response.status_code, 401)

    def test_create_movie_forbidden(self):
        response = self.app.post('/movies', headers={'Authorization': 'Bearer rol_cIg3ZghFe3ALr2L5'}) # Casting Assistant
        self.assertEqual(response.status_code, 403)

    # I can also add similar RBAC test cases for other endpoints and roles if needed

if __name__ == '__main__':
    unittest.main()
