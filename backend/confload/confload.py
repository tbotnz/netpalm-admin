import json

DEFAULT_CONFIG_FILENAME = "config.json"
DEFAULT_INVENTORY_FILENAME = "inventory.json"
TEMPLATES_AUTO_RELOAD = True

class Config:
    def __init__(self, config_filename=None, inventory_filename=None):

        if config_filename is None:
            config_filename = DEFAULT_CONFIG_FILENAME
        with open(config_filename) as json_file:
            config_data = json.load(json_file)

        self.netpalm_server = config_data["netpalm_server"]
        self.netpalm_server_port = config_data["netpalm_server_port"]
        self.netpalm_api_key = config_data["netpalm_api_key"]
        self.netpalm_headers = {
            "Content-type": "application/json",
            "x-api-key": self.netpalm_api_key
            }

        if inventory_filename is None:
            inventory_filename = DEFAULT_INVENTORY_FILENAME
        with open(inventory_filename) as inv_json_file:
            inventory_data = json.load(inv_json_file)

        self.inventory = inventory_data
        self.inventory_hosts = self.get_inventory_hosts()

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
