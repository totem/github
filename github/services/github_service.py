import requests
import json
import base64
from conf.appconfig import CONFIG_PROVIDERS, ORCHESTRATOR_WEBHOOK, IMAGE_FACTORY_WEBHOOK
from github.config_templates import templates
from github.services.file_service import FileService

auth = (CONFIG_PROVIDERS["github"]["token"], "x-oauth-basic")
base_url = CONFIG_PROVIDERS["github"]["endpoint_base"]


def get_path_params(owner, repo, hook_id=None, path=None):
    return {
        "base": base_url,
        "owner": owner,
        "repo": repo,
        "id": hook_id,
        "path": path
    }


class GithubHookRequests():
    def list_hooks(self, owner, repo):
        path_params = get_path_params(owner, repo)
        url = "{base}/repos/{owner}/{repo}/hooks".format(**path_params)
        resp = requests.get(url, auth=auth)
        return resp.json()

    def create_hook(self, owner, repo):
        """
        Create webhook
        """
        path_params = get_path_params(owner, repo)
        url = "{base}/repos/{owner}/{repo}/hooks".format(**path_params)
        webhook_config = templates.webhook.copy()
        response = []

        existing_hooks = self.get_hooks(owner, repo)

        if "image_factory" in existing_hooks and "orchestrator" in existing_hooks:
            return existing_hooks

        # Create image factory webhook
        if "image_factory" not in existing_hooks:
            webhook_config["events"][0] = "push"
            webhook_config["config"]["url"] = IMAGE_FACTORY_WEBHOOK
            if_resp = requests.post(url, data=json.dumps(webhook_config), auth=auth)
            response.append(if_resp.json())

        # Create orchestrator webhook
        if "orchestrator" not in existing_hooks:
            webhook_config["events"][0] = "delete"
            webhook_config["config"]["url"] = ORCHESTRATOR_WEBHOOK
            orch_resp = requests.post(url, data=json.dumps(webhook_config), auth=auth)
            response.append(orch_resp.json())

        return response

    def delete_hook(self, owner, repo):
        """
        Delete hook
        """
        existing_hooks = self.get_hooks(owner, repo)
        ids = map(lambda service: existing_hooks[service]["id"], existing_hooks)

        if len(ids):
            for hook_id in ids:
                path_params = get_path_params(owner, repo, hook_id)
                url = "{base}/repos/{owner}/{repo}/hooks/{id}".format(**path_params)
                resp = requests.delete(url, auth=auth)

                if resp.status_code != 204:
                    return {"status": "failed"}

            return {"status": "success"}

        return {"status": "failed"}

    def get_hooks(self, owner, repo):
        """
        Check to see if our hook exists
        """
        hooks = {}
        for hook in self.list_hooks(owner, repo):
            if hook["config"]["url"] == ORCHESTRATOR_WEBHOOK:
                hooks["orchestrator"] = hook
            elif hook["config"]["url"] == IMAGE_FACTORY_WEBHOOK:
                hooks["image_factory"] = hook

        return hooks


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
        resp = self.add_file(owner, repo, "test.yml", FileService.to_string(totem))
        return resp
