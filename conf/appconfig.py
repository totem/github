import os

MIME_JSON = "application/json"
MIME_ROOT_V1 = "application/vnd.github.root-v1+json"

SCHEMA_ROOT_V1 = "root-v1"

ORCHESTRATOR_WEBHOOK = os.getenv("ORCHESTRATOR_WEBHOOK", None)
IMAGE_FACTORY_WEBHOOK = os.getenv("IMAGE_FACTORY_WEBHOOK", None)
TRAVIS_WEBHOOK = os.getenv("TRAVIS_WEBHOOK", None)

GITHUB = {
    "token": os.getenv("GITHUB_TOKEN", None),
    "endpoint_base": "https://api.github.com"
}
