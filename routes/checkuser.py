import hashlib
import uuid

import mysql.connector
from flask import Blueprint, jsonify, request


route = Blueprint('checkuser', __name__)

def register_route(app):

    @app.route('/check-user', methods=['POST'])
    def response():
        # Get the username and password from the post request
        username = request.form.get('username')
        passwordhash = request.form.get('password')
        if username is None or passwordhash is None:
            print("Missing parameters")
            return jsonify({
                "Response": "Error",
                "Info": "Missing parameters"
            }), 200
        else:
            # Create sql connection
            conn = mysql.connector.connect(
                host="10.10.10.30",
                username="edu",
                password="jy4anCIrgK9XzMqg",
                database="edupage"
            )
            # Create cursor
            cursor = conn.cursor()
            # Execute query
            # SQL Columns: ID | username | password | status | server
            cursor.execute(f"SELECT * FROM tavh_users WHERE username = '{username}'")
            # Get the result
            result = cursor.fetchone()
            # Close the connection
            conn.close()

            # Check if the user exists
            if result is None:
                return jsonify({
                    "Response": "Error",
                    "Info": "User does not exist"
                }), 200
            else:
                # Check if the password is correct
                if result[2] == passwordhash:
                    # Check if the user status (0 = disabled, 1 = enabled)
                    if result[3] == 1:
                        return jsonify({
                            "Response": "Success",
                            "Info": result[4]
                        }), 200
                    else:
                        return jsonify({
                            "Response": "Error",
                            "Info": "User is disabled"
                        }), 200
                else:
                    return jsonify({
                        "Response": "Error",
                        "Info": "Wrong password"
                    }), 200



    app.register_blueprint(route)
