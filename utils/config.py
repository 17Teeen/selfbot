import json
import os

from . import console

VERSION = "0.0.3-alpha"
DEFAULT_CONFIG = {
    "token": "",
    "prefix": "",
    "message_settings": {
        "auto_delete_delay": 15
    },
    "theme": {
        "colour": "fa8072",
        "title": "flight sb",
        "emoji": "\ud83d\udee9\ufe0f"
    }
}

class Config:
    def __init__(self) -> None:
        self.config = {}

        if os.path.exists("config.json"):
            self.config = json.load(open("config.json"))
    
    def check(self):
        if not os.path.exists("config.json"):
            json.dump(DEFAULT_CONFIG, open("config.json", "w"))
            console.print_info("Created config file")

        if not self.config:
            self.config = json.load(open("config.json"))

        if self.get("token") == "":
            console.print_error("No token found, please set it below.")
            new_token = input("> ")

            self.set("token", new_token)

        if self.get("prefix") == "":
            console.print_error("No prefix found, please set it below.")
            new_prefix = input("> ")

            self.set("prefix", new_prefix)

    def save(self) -> None:
        json.dump(self.config, open("config.json", "w"), indent=4)

    def get(self, key) -> str:
        return self.config[key]

    def set(self, key, value) -> None:
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        self.config[key] = value
        self.save()