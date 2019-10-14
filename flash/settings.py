from ujson import load
from builtins import setattr

class settings_class():
    local_wifi_ssid = ""
    local_wifi_password = ""
    webrepl_cfg_PASS = "toor"
    def __init__(self, *args, **kwargs):
        try:
            with open("settings.json", "r") as settings_file:
                settings_json = load(settings_file)
                for setting, value in settings_json.items():
                    setattr(self, setting, value)
        except Exception as e:
            print(e)
            self.provision()
    def provision(self):
        print("provisioning")

cnf = settings_class()