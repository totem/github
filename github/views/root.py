import github
from flask.views import MethodView
from github.views import util, hypermedia
from conf.appconfig import SCHEMA_ROOT_V1, MIME_ROOT_V1, MIME_JSON


class RootApi(MethodView):
    """
    Root API
    """
    @hypermedia.produces({
        MIME_ROOT_V1: SCHEMA_ROOT_V1,
        MIME_JSON: SCHEMA_ROOT_V1
    }, default=MIME_ROOT_V1)
    def get(self, **kwargs):
        return util.build_response({"version": github.__version__})


def register(app, **kwargs):
    app.add_url_rule("/", view_func=RootApi.as_view('root'), methods=["GET"])