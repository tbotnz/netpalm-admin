import json
import os 


DEFAULT_CONFIG_FILENAME = "config.json"
DEFAULT_INVENTORY_FILENAME = "inventory.json"


class Config:
    def __init__(self, config_filename=None, inventory_filename=None):

        if config_filename is None:
            config_filename = DEFAULT_CONFIG_FILENAME
        with open(config_filename) as json_file:
            config_data = json.load(json_file)

        self.config_data = config_data
        self.netpalm_server = self.load_value("netpalm_server")
        self.netpalm_server_port = self.load_value("netpalm_server_port")
        self.netpalm_api_key = self.load_value("netpalm_api_key")

        self.netpalm_headers = {
            "Content-type": "application/json",
            "x-api-key": self.netpalm_api_key
            }

        if inventory_filename is None:
            inventory_filename = DEFAULT_INVENTORY_FILENAME
        try:
            with open(inventory_filename) as inv_json_file:
                inventory_data = json.load(inv_json_file)

        except FileNotFoundError:
            inventory_data = []

        self.inventory = inventory_data
        self.inventory_hosts = self.get_inventory_hosts()

    def load_value(self, config_key: str):
        """Allows environment variables to override config values"""
        config_value = self.config_data.get(config_key)

        env_key = f'NPA_{config_key.upper()}'
        env_value = os.environ.get(env_key)

        rslt = env_value if env_value is not None else config_value
        print(f'setting {config_key} to {rslt}')
        return rslt

    def get_inventory_hosts(self):
        result = []
        for device in self.inventory:
            result.append(device["device"])
        return result

    def get_host_inventory(self, host):
        for device in self.inventory:
            if device["device"] == host:
                return device
        return False
