inventory_list = [
    {
        "device": "10.0.2.33",
        "netmiko_driver": "cisco_ios",
        "username": "admin",
        "password": "admin",
        "queue_strategy": "fifo",
    },
    {
        "device": "10.0.2.22",
        "netmiko_driver": "cisco_ios",
        "username": "admin",
        "password": "admin",
        "queue_strategy": "fifo",
    },
    {
        "device": "10.0.2.18",
        "netmiko_driver": "cisco_ios",
        "username": "admin",
        "password": "admin",
        "queue_strategy": "fifo",
    },
    {
        "device": "10.0.2.20",
        "netmiko_driver": "cisco_ios",
        "username": "admin",
        "password": "admin",
        "queue_strategy": "pinned",
    },
]


def get_hosts(inv_list):
    result = []
    for z in inv_list:
        result.append(z["device"])
    return result


def get_host_inventory(host, inv_list):
    for z in inv_list:
        if z["device"] == host:
            return z
    return False
