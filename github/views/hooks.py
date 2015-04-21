from flask.views import MethodView
from github.views import util
from github.services.github_service import GithubHookRequests

hook_service = GithubHookRequests()


class HooksApi(MethodView):
    def get(self, owner=None, repo_name=None):
        """
        Get all hooks for a repository
        """
        hooks = hook_service.list_hooks(owner, repo_name)
        return util.build_response(hooks)

    def post(self, owner=None, repo_name=None):
        """
        Create hook for a repository
        """
        resp = hook_service.create_hook(owner, repo_name)
        return util.build_response(resp)

    def delete(self, owner=None, repo_name=None):
        """
        Delete hook for a repository
        """
        resp = hook_service.delete_hook(owner, repo_name)
        return util.build_response(resp)


def register(app):
    app.add_url_rule("/organizations/<owner>/repos/<repo_name>/hooks", view_func=HooksApi.as_view('github'),
                     methods=["GET", "POST", "DELETE"])