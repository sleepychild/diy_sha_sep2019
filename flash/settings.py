from ujson import load, dump
from builtins import setattr

class settings_class():
    
    webrepl_cfg_PASS = "toor"
    cloud_address = ""

    def __init__(self, *args, **kwargs):
        if self.load_config():
            pass
        else:
            pass

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
        pass

cnf = settings_class()