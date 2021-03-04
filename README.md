# netpalm-admin
simple admin app for managing a netpalm cluster

![netpalm commandatron](/netpalm-admin.gif)

### getting started
- make sure you have a [netpalm](https://github.com/tbotnz/netpalm) instance running
- git clone the project ``` git clone https://github.com/tbotnz/netpalm-admin.git && cd netpalm-admin ```
- update the ```config.json``` with your ```NETPALM_SERVER_IP``` ```NETPALM_SERVER_PORT``` ```NETPALM_API_KEY```
- configure ```inventory.json``` with your inventory (optional)
- install the requirements ```pip3 install -r requirements.txt```
- run the app ```python3 netpalm-admin.py```

### local inventory
for ```local inventory``` ensure ```config.json``` has the following lines
```
    "inventory_type": "local",
    "inventory_file": "inventory_local.json"
```
configure ```"inventory_local.json"``` with your local inventory params accordingly

### netbox inventory
for ```netbox inventory``` ensure ```config.json``` has the following lines
```
    "inventory_type": "netbox",
    "inventory_file": "inventory_netbox.json"
```
configure ```"inventory_netbox.json"``` with your netbox params accordingly

### notice
- project currently just a poc in progress, use at your own leisure
