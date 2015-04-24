totem_yml = """
    example_tbd:
        example_tbd: 9000
"""

webhook = {
    "name": "web",
    "active": "true",
    "events": [
        "push"
    ],
    "config": {
        "url": "",
        "content_type": "json"
    }
}

travis_hook = """
notifications:
    webhooks:
        -
"""

create_file = {
    "path": "",
    "message": "Added configuration",
    "content": ""
}
