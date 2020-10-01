from flask import Flask, render_template, redirect, url_for, request, json
import requests

from inventory import get_hosts, inventory_list
from netpalm_utilities import send_netpalm, check_task

app = Flask(__name__)

devices = get_hosts(inventory_list)

NETPALM_SERVER_IP = "10.0.2.15"
NETPALM_SERVER_PORT = 9000
NETPALM_API_KEY = "2a84465a-cf38-46b2-9d86-b84Q7d57f288"


@app.route("/")
def home():
    return render_template("navbase.html")


@app.route("/getcfg")
def getcfg():
    return render_template("get_set_config.html", cfgtype="get", devices=devices)


@app.route("/setcfg")
def setcfg():
    return render_template("get_set_config.html", cfgtype="set", devices=devices)


@app.route("/execnetpalm/", methods=["POST"])
def execnetpalm():
    posted_data = request.json
    res = send_netpalm(
        posted_data, NETPALM_SERVER_IP, NETPALM_SERVER_PORT, NETPALM_API_KEY
    )
    return res


@app.route("/task/<task_id>")
def checktask(task_id):
    res = check_task(task_id, NETPALM_SERVER_IP, NETPALM_SERVER_PORT, NETPALM_API_KEY)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, threaded=True)
