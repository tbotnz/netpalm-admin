import json
import os

import requests

DEFAULT_CONFIG_FILENAME = "config.json"
DEFAULT_INVENTORY_FILENAME = "inventory_local.json"


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
        self.inventory_filename = inventory_filename
        
        self.netpalm_headers = {
            "Content-type": "application/json",
            "x-api-key": self.netpalm_api_key
            }


        self.inventory = self.get_inventory()
        self.inventory_hosts = self.get_inventory_hosts()

    def get_inventory(self):
        """ load the inventory """

        inv_type = self.load_value("inventory_type")
        inv_file = self.load_value("inventory_file")

        if inv_type == "local":
            if self.inventory_filename is None:
                inventory_filename = DEFAULT_INVENTORY_FILENAME
            try:
                with open(inventory_filename) as inv_json_file:
                    inventory_data = json.load(inv_json_file)

            except FileNotFoundError:
                inventory_data = []
            return inventory_data

        elif inv_type == "netbox":
            inventory_data = []
            with open(inv_file) as inv_json_file:
                nbox_config = json.load(inv_json_file)

            token = nbox_config["netbox_token"]
            base_url = nbox_config["netbox_url"]
            headers = {"Authorization": f"Token {token}" }
            ssl_verify = nbox_config["netbox_ssl_verify"]

            r = requests.get(f"{base_url}/api/dcim/devices", headers=headers, verify=ssl_verify, timeout=15).json()
            if r["count"] >= 1:
                for dev in r["results"]:
                    try:
                        plat_url = dev["platform"]["url"]
                        napalm_driver = r = requests.get(f"{plat_url}", headers=headers, verify=ssl_verify, timeout=15).json()["napalm_driver"]
                        obj = {
                            "device": dev["primary_ip4"]["address"].split("/")[0],
                            "library": "napalm",
                            "driver": napalm_driver,
                            "username": nbox_config["device_username"],
                            "password": nbox_config["device_password"],
                            "queue_strategy": "fifo"
                        }
                        inventory_data.append(obj)
                    except Exception as e:
                        print (f"error {e} getting inventory data for a host")
                        pass
            return inventory_data

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
