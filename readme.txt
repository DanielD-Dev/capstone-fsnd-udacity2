# Casting Agency API

## Motivation for the Project

The Casting Agency API is a project developed as part of the Udacity Full Stack Nanodegree program. The goal of the project is to create a RESTful API for a casting agency, allowing users to manage actors and movies in a database. The API supports various CRUD operations and implements role-based access control (RBAC) to ensure proper authorization for different actions.

## Hosted API URL

The Casting Agency API is hosted at: [https://capstone-fsnd-udacity-44f9232cb6dd.herokuapp.com](https://capstone-fsnd-udacity-44f9232cb6dd.herokuapp.com)

## Project Dependencies

To run and test the Casting Agency API locally, you'll need the following dependencies:

- Python 3.7 or later
- Flask web framework
- Flask-CORS
- Flask-SQLAlchemy
- Jose (JSON Web Token library)
- Auth0 account for authentication and authorization

## Local Development and Hosting Instructions

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/ddreiman/capstone-fsnd-udacity.git
   cd YOUR_REPOSITORY

Install Dependencies:
pip install -r requirements.txt

2. Set Up Auth0:
Create an account on Auth0.
Configure an API in Auth0 and note down the API Audience and Domain details.
Set up roles and permissions for your application.

3. Configure Environment Variables:
Create a .env file and add the following environment variables:

Copy code
AUTH0_DOMAIN=YOUR_AUTH0_DOMAIN
API_AUDIENCE=YOUR_API_AUDIENCE

4. Run the Development Server:
python app.py

The server will be running at http://localhost:8080.

API Documentation

Detailed API documentation can be found in the API Documentation file. This documentation provides information on all available endpoints, their behavior, and the required authentication and permissions.

RBAC Controls

The API implements Role-Based Access Control (RBAC) using Auth0 roles and permissions. The @requires_auth(permission) decorator ensures that only authorized users with the necessary roles and permissions can access specific endpoints.

For more information on roles and permissions, refer to the Auth0 Documentation.

Feel free to reach out with any questions or feedback!

