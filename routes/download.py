import os
import hashlib
import uuid

from flask import Blueprint, jsonify, request, send_file

route = Blueprint('download', __name__)

def register_route(app):
    @route.route('/download/<filename>', methods=['POST', 'GET'])
    def downloadFile(filename):
        # Get the filename from the URL
        filename = request.view_args['filename']
        # Get the file path
        path = os.path.join('uploads', filename)
        # Check if the file exists
        if not os.path.exists(path):
            return jsonify({
                "status": "error",
                "message": "File does not exist"
            }), 404
        # Return the file
        return send_file(path, as_attachment=True)

    @route.route('/download/', methods=['POST', 'GET'])
    def simpleresponse():
        return jsonify({
            "status": "error",
            "message": "No permission"
        }), 403

    @route.route('/download', methods=['POST', 'GET'])
    def simpleresponse_():
        return jsonify({
            "status": "error",
            "message": "No permission"
        }), 403


    app.register_blueprint(route)
