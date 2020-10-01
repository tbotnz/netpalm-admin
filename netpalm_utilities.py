import requests

from inventory import get_host_inventory, inventory_list


def send_netpalm(inbound_json, NETPALM_SERVER_IP, NETPALM_SERVER_PORT, NETPALM_API_KEY):
    inventory_obj = get_host_inventory(inbound_json["host"], inventory_list)
    post_data = {
        "library": "netmiko",
        "connection_args": {
            "device_type": inventory_obj["netmiko_driver"],
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
        f"http://{NETPALM_SERVER_IP}:{NETPALM_SERVER_PORT}/{method}config",
        headers={"Content-type": "application/json", "x-api-key": NETPALM_API_KEY},
        json=post_data,
        timeout=10,
    )
    return r.json()


def check_task(task_id, NETPALM_SERVER_IP, NETPALM_SERVER_PORT, NETPALM_API_KEY):
    r = requests.get(
        f"http://{NETPALM_SERVER_IP}:{NETPALM_SERVER_PORT}/task/{task_id}",
        headers={"Content-type": "application/json", "x-api-key": NETPALM_API_KEY},
        timeout=30,
    )
    return r.json()
