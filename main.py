import os
import importlib

from flask import Flask, render_template
from werkzeug.serving import make_server

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 * 1024

# Get all modules in the routes subdirectory
route_modules = [f[:-3] for f in os.listdir('./routes') if f.endswith('.py') and f != '__init__.py']

# Register routes
for module_name in route_modules:
    module = importlib.import_module(f'routes.{module_name}')
    module.register_route(app)

if __name__ == '__main__':
    mode = os.getenv("DEBUG")
    app.run(host='0.0.0.0', debug=True)
