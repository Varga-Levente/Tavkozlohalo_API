import os
import hashlib
import uuid

from flask import Blueprint, jsonify, request


route = Blueprint('upload', __name__)

def register_route(app):
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 * 1024  # 32 GB
    @route.route('/upload', methods=['POST'])
    def upload_file():
        # Check if the file is in the request
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "File is missing in the request"
            }), 400

        file = request.files['file']

        # Check if the file name is empty
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "File name is empty"
            }), 400

        # Generate a unique filename
        filename = f"{str(uuid.uuid4())}-{file.filename}"
        filepath = os.path.join('uploads', filename)

        # Save the file
        file.save(filepath)

        # Return the download URL
        url = f"http://{request.host}/download/{filename}"
        return jsonify({
            "status": "success",
            "url": url
        }), 200


    app.register_blueprint(route)
