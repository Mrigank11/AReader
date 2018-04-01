import json
import os


class Config:
    CONFIG_FILE = "areader.json"

    def __init__(self):
        # create empty CONFIG_FILE
        if(not os.path.exists(self.CONFIG_FILE)):
            with open(self.CONFIG_FILE, "a") as f:
                f.write("{\"feeds\":[]}")
        self.read()

    def read(self):
        self.config = json.load(open(self.CONFIG_FILE))

    def get(self, key):
        return self.config[key] if key in self.config else False

    def write(self):
        json.dump(self.config, open(self.CONFIG_FILE, "w"), indent=4)
