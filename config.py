import json


class Config:
    cfg_file_path = "config.json"

    def __init__(self):
        pass

    def load_cfg(self):
        with open(self.cfg_file_path) as fp:
            data = json.load(fp)

    def parse_auth(self):
        pass

    def parser_report(self):
        pass

    def parser_mail(self):
        pass
