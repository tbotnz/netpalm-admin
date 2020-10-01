# netpalm-commandatron
simple hello world app to run async commands for getting and setting config on multiple devices

![netpalm commandatron](/netpalm-commandatron.gif)

### getting started
- make sure you have a [netpalm](https://github.com/tbotnz/netpalm) instance running
- git clone the project ``` git clone https://github.com/tbotnz/netpalm-commandatron.git && cd netpalm-commandatron ```
- update the ```app.py``` with your ```NETPALM_SERVER_IP``` ```NETPALM_SERVER_PORT``` ```NETPALM_API_KEY```
- configure ```inventory.py``` with your inventory
- install the requirements ```pip3 install -r requirements.txt```
- run the app ```python3 app.py```

### todo
- stop long polling
- refactor and cleanup code
- something else interesting
