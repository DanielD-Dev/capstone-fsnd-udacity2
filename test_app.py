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

    # Write more tests for other endpoints and RBAC behavior

if __name__ == '__main__':
    unittest.main()
