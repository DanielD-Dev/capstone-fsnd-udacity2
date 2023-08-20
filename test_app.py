import unittest
from app import app

class YourTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Set up any necessary test data or context here

    def test_get_movies(self):
        response = self.app.get('/movies')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('movies' in data)

    def test_create_movie(self):
        # Write a test for the POST request here

    def test_update_movie(self):
        # Write a test for the PATCH request here

    def test_delete_movie(self):
        # Write a test for the DELETE request here

    # Add similar test cases for actors endpoints (GET, POST, PATCH, DELETE)

    # Test RBAC behavior for different roles
    def test_get_movies_unauthorized(self):
        response = self.app.get('/movies', headers={'Authorization': 'Bearer YOUR_INVALID_TOKEN'})
        self.assertEqual(response.status_code, 401)

    def test_create_movie_forbidden(self):
        response = self.app.post('/movies', headers={'Authorization': 'Bearer YOUR_ACTOR_TOKEN'})
        self.assertEqual(response.status_code, 403)

    # Add similar RBAC test cases for other endpoints and roles

if __name__ == '__main__':
    unittest.main()
