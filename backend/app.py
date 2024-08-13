
import os
import numpy as np
import cv2
import base64
import tempfile
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes import api

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='frontend', static_url_path='/')  # Set static folder to frontend
CORS(app)

# Load configuration from environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', '127.0.0.1')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE', 'invoicedetection')
app.config['MYSQL_PORT'] = os.getenv('MYSQL_PORT', '3308')

app.register_blueprint(api)

# Serve the main index.html file
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, images)
# @app.route('/<path:path>')
# def static_proxy(path):
#     return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
