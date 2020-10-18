import requests

from backend.confload.confload import Config


class NetpalmAdapter:
    def __init__(self):
        self.config = Config()

    def send_netpalm(self, inbound_json):
        inventory_obj = self.config.get_host_inventory(inbound_json["host"])
        post_data = {
            "library": inventory_obj["library"],
            "connection_args": {
                "device_type": inventory_obj["driver"],
                "host": inventory_obj["device"],
                "username": inventory_obj["username"],
                "password": inventory_obj["password"],
            },
            "queue_strategy": inventory_obj["queue_strategy"],
        }

        if inbound_json["method"] == "get":
            post_data["command"] = inbound_json["command"]
        elif inbound_json["method"] == "set":
            post_data["config"] = [inbound_json["command"]]

        method = inbound_json["method"]
        r = requests.post(
            f"http://{self.config.netpalm_server}:{self.config.netpalm_server_port}/{method}config",
            headers=self.config.netpalm_headers,
            json=post_data,
            timeout=10,
        )
        return r.json()

    def check_task(self, task_id):
        r = requests.get(
            f"http://{self.config.netpalm_server}:{self.config.netpalm_server_port}/task/{task_id}",
            headers=self.config.netpalm_headers,
            timeout=30,
        )
        return r.json()

    def get(self, route):
        r = requests.get(
            f"http://{self.config.netpalm_server}:{self.config.netpalm_server_port}/{route}",
            headers=self.config.netpalm_headers,
            timeout=30,
        )
        return r.json()

    def template_editor(self, route):
        r = requests.get(
            f"http://{self.config.netpalm_server}:{self.config.netpalm_server_port}/{route}",
            headers=self.config.netpalm_headers,
            timeout=30,
        )
        return r.json()

    def template_getter(self, route):
        r = requests.get(
            f"http://{self.config.netpalm_server}:{self.config.netpalm_server_port}/{route}",
            headers=self.config.netpalm_headers,
            timeout=30,
        )
        return r.json()  

    def get_containers(self):
        workers = self.get("workers/")
        result = {}
        for worker in workers:
            if worker["hostname"] not in result.keys():
                result[worker["hostname"]] = {
                    "successful_job_count": 0,
                    "failed_job_count": 0,
                    "container_type": "pinned",
                    }
                if "fifo" in worker["name"]:
                    result[worker["hostname"]]["container_type"] = "fifo"
            result[worker["hostname"]]["successful_job_count"] += worker["successful_job_count"]
            result[worker["hostname"]]["failed_job_count"] += worker["failed_job_count"]
        return result
