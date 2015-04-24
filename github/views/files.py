import flask
from flask.views import MethodView
from github.views import util
from github.services.github_service import GithubFileRequests

files_request = GithubFileRequests()


class FilesApi(MethodView):
    def get(self, owner, repo, file_type):
        resp = {}

        if file_type == "totem":
            resp = files_request.add_totem(owner, repo)
        elif file_type == "travis":
            resp = files_request.add_travis(owner, repo)
        else:
            flask.abort(404)

        return util.build_response(resp)


def register(app):
    app.add_url_rule("/file/<owner>/<repo>/<file_type>",
                     view_func=FilesApi.as_view('files'),
                     methods=["GET"])
