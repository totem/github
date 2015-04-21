from flask.views import MethodView
from github.views import util
from github.services.github_service import GithubFileRequests

files_request = GithubFileRequests()


class FilesApi(MethodView):
    def get(self, owner, repo):
        resp = files_request.add_totem(owner, repo)
        return util.build_response(resp)


def register(app):
    app.add_url_rule("/file/<owner>/<repo>/totem", view_func=FilesApi.as_view('files'), methods=["GET"])