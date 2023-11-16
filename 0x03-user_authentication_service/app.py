#!/usr/bin/env python3
"""
Module to run flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def home():
    """
    Route to home
    """
    # Create a JSON response message
    meassage = jsonify({"message": "Bienvenue"})
    # Return a JSON response message
    return meassage


@app.route("/users", methods=["POST"])
def users():
    """
    Registers Users.

    Handles the registration of users via a POST request.
    Expects 'email' and 'password' fields in the request form.

    Returns a JSON response with appropriate messages and HTTP status codes.

    HTTP Status Codes:
    - 200 OK: User successfully registered.
    - 400 Bad Request: Invalid request method or email already registered.
    - 500 Internal Server Error: Unexpected error during registration.
    """
    # Check if the request method is POST
    if request.method == "POST":
        # Get the 'email' field from the request form
        email = request.form.get("email")
        # Get the 'password' field from the request
        password = request.form.get("password")
        try:
            # Attempt to register the user using the Auth instance
            AUTH.register_user(email, password)
            # Create a JSON response message
            message = jsonify({"email": email,
                               "message": "user created"})
            # Return the JSON response
            return message
        # Catch a ValueError if the email is already registered
        except ValueError:
            # Return a JSON response with a 400 status code
            return jsonify({"message": "email already registered"}), 400
        # Catch other exceptions
        except Exception as E:
            # Return a JSON response with a 500 status code
            return jsonify({"message": f"Error {str(E)} occured"}), 500
    else:
        # If the request method is not POST, return a 400 Bad Request
        abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
