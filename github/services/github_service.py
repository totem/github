import requests
import json
import base64
from conf.appconfig import GITHUB, ORCHESTRATOR_WEBHOOK, IMAGE_FACTORY_WEBHOOK, TRAVIS_WEBHOOK
from github.config_templates import templates
from github.services.file_service import FileService
from github.views.error import HooksFailed

auth = (GITHUB["token"], "x-oauth-basic")
base_url = GITHUB["endpoint_base"]


def get_path_params(owner, repo, hook_id=None, path=None):
    return {
        "base": base_url,
        "owner": owner,
        "repo": repo,
        "id": hook_id,
        "path": path
    }


class GithubHookRequests():

    def create_totem_hooks(self, owner, repo):
        """
        Create totem specific hooks
        """
        resp = []
        hooks = self.list_hooks(owner, repo)
        existing_hooks = self.get_totem_hooks(hooks)

        if "image_factory" in existing_hooks and "orchestrator" in existing_hooks:
            return existing_hooks

        if "image_factory" not in existing_hooks:
            resp.append(self.create_hook(owner, repo, "push", IMAGE_FACTORY_WEBHOOK))

        if "orchestrator" not in existing_hooks:
            resp.append(self.create_hook(owner, repo, "delete", ORCHESTRATOR_WEBHOOK))

        return resp

    def delete_hook(self, owner, repo, match=None):
        """
        Delete hook
        """
        hooks = self.list_hooks(owner, repo)
        if match:
            existing_hooks = self.get_hook(hooks, match)
            ids = [existing_hooks["id"]]
        else:
            existing_hooks = self.get_totem_hooks(hooks)
            if not len(existing_hooks.keys()):
                raise HooksFailed("Error getting hook",
                                  status_code=404,
                                  details="Totem hooks do not exist on repo")

            ids = map(lambda service: existing_hooks[service]["id"], existing_hooks)

        for hook_id in ids:
            path_params = get_path_params(owner, repo, hook_id)
            url = "{base}/repos/{owner}/{repo}/hooks/{id}".format(**path_params)
            resp = requests.delete(url, auth=auth)

            if resp.status_code != 204:
                raise HooksFailed("Error deleting hooks",
                                  status_code=resp.status_code,
                                  details=resp.json())

        return {"status": "success"}

    @staticmethod
    def list_hooks(owner, repo):
        path_params = get_path_params(owner, repo)
        url = "{base}/repos/{owner}/{repo}/hooks".format(**path_params)
        resp = requests.get(url, auth=auth)

        if resp.status_code is not 200:
            raise HooksFailed("Error getting hooks",
                              status_code=resp.status_code,
                              details=resp.json())

        return resp.json()

    @staticmethod
    def create_hook(owner, repo, event, path):
        """
        Create github webhook
        """
        path_params = get_path_params(owner, repo)
        url = "{base}/repos/{owner}/{repo}/hooks".format(**path_params)
        webhook_config = templates.webhook.copy()

        webhook_config["events"][0] = event
        webhook_config["config"]["url"] = path
        resp = requests.post(url, data=json.dumps(webhook_config), auth=auth)
        if resp.status_code is not 201:
            raise HooksFailed("Error creating hook",
                              status_code=resp.status_code,
                              details=resp.json())
        return resp.json()

    @staticmethod
    def get_hook(hooks, match):
        """
        Check to see if our hook exists
        """
        for hook in hooks:
            if match in hook["config"]["url"]:
                return hook

        raise HooksFailed("Error getting hook",
                          status_code=404,
                          details="Hook does not exist on repo: %s" % match)

    @staticmethod
    def get_totem_hooks(hooks):
        """
        Get hooks specific to totem
        """
        totem_hooks = {}
        for hook in hooks:
            url = hook["config"]["url"]
            if url == IMAGE_FACTORY_WEBHOOK:
                totem_hooks["image_factory"] = hook
            elif url == ORCHESTRATOR_WEBHOOK:
                totem_hooks["orchestrator"] = hook

        return totem_hooks


class GithubFileRequests():
    def add_file(self, owner, repo, filename, content):
        path_params = get_path_params(owner, repo, path=filename)
        url = "{base}/repos/{owner}/{repo}/contents/{path}".format(**path_params)
        data = templates.create_file.copy()
        data["path"] = filename
        data["content"] = base64.b64encode(content)
        resp = requests.put(url, data=json.dumps(data), auth=auth)
        return resp.json()

    def add_totem(self, owner, repo):
        totem = FileService.get_totem()
        # resp = self.add_file(owner, repo, "totem.yml", FileService.to_string(totem))
        return totem

    def add_travis(self, owner, repo):
        travis = FileService.get_travis()
        travis["notifications"]["webhooks"] = [TRAVIS_WEBHOOK]
        # resp = self.add_file(owner, repo, ".travis.yml", FileService.to_string(travis))
        return travis

    def add_dockerfile(self, owner, repo):
        docker = FileService.get_dockerfile()
        pass