from flask import Flask
from github.views import root, hooks, files, error, hypermedia

app = Flask(__name__)

hypermedia.register_schema_api(app).register_error_handlers(app)

for module in [root, hooks, files, error]:
    module.register(app)