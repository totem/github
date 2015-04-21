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
    "config" : {
        "url": "",
        "content_type": "json"
    }
}

create_file = {
    "path": "",
    "message": "Added configuration",
    "content": ""
}