from ujson import load, dump
from builtins import setattr, getattr

class settings_class():
    webrepl_cfg_PASS = "toor"
    cloud_address = ""
    ssid = ""
    key = ""

    conf = {
        "webrepl_cfg_PASS":"",
        "cloud_address":"",
        "ssid":"",
        "key":""
    }

    def __init__(self, *args, **kwargs):
        if not self.load_config():
            self.save_config()

    def load_config(self):
        try:
            with open("settings.json", "r") as settings_file:
                settings_json = load(settings_file)
                for setting, value in settings_json.items():
                    setattr(self, setting, value)
            return True
        except Exception as e:
            print(e)
            return False

    def save_config(self):
        for key, val in self.conf.items():
            self.conf[key] = getattr(self, key)
        with open("settings.json", "w") as settings_file:
            dump(self.conf, settings_file)

cnf = settings_class()