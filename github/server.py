from flask import Flask
from github.views import root, hooks, files, hypermedia

app = Flask(__name__)

hypermedia.register_schema_api(app).register_error_handlers(app)

for module in [root, hooks, files]:
    module.register(app)