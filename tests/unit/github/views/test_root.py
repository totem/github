import json
import github
from nose.tools import eq_
from github.server import app
from conf.appconfig import MIME_ROOT_V1

class TestRootView:
    def setup(self):
        self.client = app.test_client()

    def test_root(self):
        resp = self.client.get("/")

        eq_(resp.status_code, 200)
        eq_(resp.headers["content-type"], MIME_ROOT_V1)
        data = json.loads(resp.data)
        eq_(data["version"], github.__version__)
