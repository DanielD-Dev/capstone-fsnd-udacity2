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

## Set Up Authentication

To test the endpoints that require authentication and authorization, you'll need to set up an Auth0 account and configure the necessary environment variables.

1. **Create an Auth0 Account:**
   If you don't have an Auth0 account, you can sign up for free at [https://auth0.com/signup](https://auth0.com/signup).

2. **Configure an Auth0 API:**
   - Log in to your Auth0 account dashboard.
   - Create a new API and note down the "Audience" and "Domain" details.
   - Configure roles and permissions for your API. For this project, you can set up roles like "Casting Assistant," "Casting Director," and "Executive Producer," each with specific permissions.

3. **Environment Variables:**
   Create a `.env` file in the root directory of your project and add the following environment variables:

AUTH0_DOMAIN=ddreyman1.us.auth0.com
API_AUDIENCE=https://capstone_project_api.com


4. **Roles and Permissions:**
Assign roles to your Auth0 account that correspond to the roles you've set up in your API. This will allow you to test different permissions while using the API.

## Running the Application

1. **Clone the Repository:**
```sh
git clone https://github.com/ddreiman/capstone-fsnd-udacity.git
cd YOUR_REPOSITORY

1. Install Dependencies:

pip install -r requirements.txt

2. Run the Development Server:

python app.py
The server will be running at http://localhost:8080.

API Documentation and RBAC Controls

For detailed API documentation, including information on available endpoints, their behavior, required authentication, and permissions, refer to the API Documentation file.

The API implements Role-Based Access Control (RBAC) using Auth0 roles and permissions. The @requires_auth(permission) decorator ensures that only authorized users with the necessary roles and permissions can access specific endpoints. For more information on roles and permissions, refer to the Auth0 Documentation.

Feel free to reach out with any questions or feedback!