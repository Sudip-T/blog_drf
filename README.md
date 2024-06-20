# DRF Blog App

A simple Django blog application with authentication and CRUD functionality for blog posts. This project demonstrates the implementation of custom APIs for user registration, login, and logout, along with blog post creation, retrieval, update, and deletion. Additionally, unit tests are provided for both the authentication and blog apps.

## Features
- User Authentication: Custom APIs for user registration, login, and logout.
- Blog Posts: CRUD operations for blog posts with permission handling.
- Unit Testing: Comprehensive unit tests for both authentication and blog functionality.

## Installation

### Prerequisites
Python
Django
PostgreSQL

## Steps
Clone the repository:
- git clone https://github.com/Sudip-T/blog_drf

Create and activate a virtual environment:
- python -m venv venv
- `venv\Scripts\activate` # On Windows

## Install dependencies:
- pip install -r requirements.txt

## Set up the database:
Ensure your database settings in settings.py are correct. Then run:
- python manage.py migrate

## Create a superuser (optional, for admin access):
python manage.py createsuperuser

## Run the development server:
- python manage.py runserver

## Authentication
This project includes custom APIs for user registration, login, and logout.

User Registration
- Endpoint: /api/v1/auth/register/
- Method: POST
- Payload:{
  "email": "user@example.com",
  "password": "password",
  "confirm_password": "password"
}

User Login
- Endpoint: /api/v1/auth/login/token/
- Method: POST
- Payload:{
  "email": "user@example.com",
  "password": "password"
}

User Logout
- Endpoint: /api/v1/auth/logout/
- Method: POST
- Headers: Authorization: Token <token>


## Blog Posts

List and Create Blog Posts
- Endpoint: /api/v1/blogs/
- Method: GET, POST
Permissions:
- GET: Any user (authenticated or not) can retrieve the list of blog posts.
- POST: Only authenticated users can create a new blog post.

Retrieve, Update, and Delete a Blog Post
- Endpoint: /api/v1/blog/<int:pk>/
- Method: GET, PUT, DELETE
Permissions:
- GET: Any user (authenticated or not) can retrieve a blog post.
- PUT: Only the author of the blog post can update it.
- DELETE: Only the author of the blog post can delete it.

## Testing
Unit tests are provided for both authentication and blog functionalities.

To run the tests, use the following command:
- python manage.py test

### Authentication Tests
Tests for user registration, including valid registration, existing email, and password mismatch.
Tests for user login, including valid login, invalid password, and non-existent user.

### Blog Post Tests
Tests for listing and creating blog posts, including valid and invalid data handling.
Tests for retrieving, updating, and deleting blog posts, including permission checks for authorized and unauthorized users.


## API Documentation
You can find the Postman documentation at https://documenter.getpostman.com/view/28231090/2sA3XSC1my