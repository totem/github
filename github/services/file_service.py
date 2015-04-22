import yaml
from github.config_templates import templates


class FileService():
    @staticmethod
    def get_totem():
        return yaml.load(templates.totem_yml)

    @staticmethod
    def get_dockerfile():
        pass

    @staticmethod
    def get_travis():
        return yaml.load(templates.travis_hook)

    @staticmethod
    def to_string(obj):
        return yaml.dump(obj, default_flow_style=False)