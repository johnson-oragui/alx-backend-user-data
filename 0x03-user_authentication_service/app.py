#!/usr/bin/env python3
"""
Module to run flask app
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def home():
    """
    Route to home
    """
    meassage = jsonify({"message": "Bienvenue"})
    return meassage


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
