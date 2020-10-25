from flask import Flask, render_template, request, jsonify


from backend.confload.confload import Config
from backend.netpalm.netpalm_adapter import NetpalmAdapter
from backend.parseatron.parseatron import ParseAtron

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
conf = Config()
netpalm = NetpalmAdapter()
parseatron = ParseAtron()


@app.route("/")
def home():
    # poorly generate some container stats
    container_data = netpalm.get_containers()
    container_names = []
    failed_jobs = []
    successful_jobs = []
    for container in container_data:
        container_names.append(container)
        successful_jobs.append(container_data[container]["successful_job_count"])
        failed_jobs.append(container_data[container]["failed_job_count"])
    total_successful_jobs = sum(successful_jobs)
    total_failed_jobs = sum(failed_jobs)
    total_jobs = total_successful_jobs + total_failed_jobs
    try:
        total_success_percent = "{:.2f}".format((total_successful_jobs / total_jobs) * 100)
        total_failed_percent = "{:.2f}".format((total_failed_jobs / total_jobs) * 100)
    except ZeroDivisionError:
        total_success_percent = 0
        total_failed_percent = 0

    # poorly generate some process stats
    worker_data = netpalm.get("workers/")
    worker_names = []
    worker_failed_jobs = []
    worker_successful_jobs = []
    total_processes = 0
    container_types = {"fifo":0,"pinned":0}
    container_set = set()
    for worker in worker_data:
        worker_names.append(worker["name"])
        worker_failed_jobs.append(worker["successful_job_count"])
        worker_successful_jobs.append(worker["failed_job_count"])
        if worker["hostname"] not in container_set:
            if "fifo" in worker["name"]:
                container_types["fifo"] += 1
                container_set.add(worker["hostname"])
            if ("fifo" not in worker["name"]) and ("processworker" not in worker["name"]):
                container_types["pinned"] += 1
                container_set.add(worker["hostname"])
        total_processes += 1
    total_running_containers = len(container_set)
    total_devices_inventory = len(conf.inventory_hosts)
    return render_template(
                        "home.html",
                        container_names=container_names,
                        failed_jobs=failed_jobs,
                        successful_jobs=successful_jobs,
                        total_successful_jobs=total_successful_jobs,
                        total_failed_jobs=total_failed_jobs,
                        total_jobs=total_jobs,
                        total_success_percent=total_success_percent,
                        total_failed_percent=total_failed_percent,
                        worker_names=worker_names,
                        worker_failed_jobs=worker_failed_jobs,
                        worker_successful_jobs=worker_successful_jobs,
                        container_types=container_types,
                        total_processes=total_processes,
                        total_running_containers=total_running_containers,
                        total_devices_inventory=total_devices_inventory
                        )


@app.route("/template_editor/<template_type>")
def template_editor(template_type=None):
    return render_template(
                        "template-editor-form.html",
                        heading=template_type
                        )


@app.route("/script_editor/<script_type>")
def script_editor(script_type=None):
    return render_template(
                        "python-editor-form.html",
                        script_type=script_type
                        )


@app.route("/parser/ttp")
def ttp_parser():
    ttpdata = netpalm.get("ttptemplate")
    return render_template(
                        "universal-template-table.html",
                        heading="TTP loaded templates",
                        data=ttpdata
                        )


@app.route("/parser/tfsm")
def tfsm_parser():
    tfsmdata = netpalm.get("template")
    return render_template("tfsm-parser-table.html", tfsmdata=tfsmdata)


@app.route("/template/service")
def service_template():
    data = netpalm.get("j2template/service/")
    return render_template(
                        "universal-template-table.html",
                        heading="service templates loaded",
                        data=data
                        )


@app.route("/template/webhook")
def webhook_template():
    data = netpalm.get("j2template/webhook/")
    return render_template(
                        "universal-template-table.html",
                        heading="webhook templates loaded",
                        data=data
                        )


@app.route("/template/config")
def config_template():
    data = netpalm.get("j2template/config/")
    return render_template(
                        "universal-template-table.html",
                        heading="config templates loaded",
                        data=data
                        )


@app.route("/script")
def script():
    data = netpalm.get("script")
    return render_template(
                        "universal-template-table.html",
                        heading="scripts loaded",
                        data=data
                        )


@app.route("/webhook")
def webhook():
    data = netpalm.get("webhook")
    return render_template(
                        "universal-template-table.html",
                        heading="webhooks loaded",
                        data=data
                        )


@app.route("/containers")
def containers():
    data = netpalm.get_containers()
    return render_template(
                        "containers-table.html",
                        data=data
                        )


@app.route("/process")
def process():
    data = netpalm.get("workers/")
    return render_template(
                        "process-table.html",
                        data=data
                        )


@app.route("/queue")
def queue():
    data = netpalm.get("taskqueue/")
    return render_template(
                        "queue-depth-table.html",
                        data=data
                        )


@app.route("/taskatron")
def taskatron():
    return render_template(
                        "taskatron.html"
                        )


@app.route("/getcfg")
def getcfg():
    return render_template(
                        "commandatron_get_set_config.html",
                        cfgtype="get",
                        devices=conf.inventory_hosts
                        )


@app.route("/setcfg")
def setcfg():
    return render_template(
                        "commandatron_get_set_config.html",
                        cfgtype="set",
                        devices=conf.inventory_hosts
                        )


@app.route("/execnetpalm/", methods=["POST"])
def execnetpalm():
    posted_data = request.json
    res = netpalm.send_netpalm(
                    posted_data
                    )
    return res


@app.route("/task/<task_id>")
def checktask(task_id):
    res = netpalm.check_task(
                    task_id
                    )
    return res


@app.route('/fsm', methods=['POST'])
def fsm():
    try:
        data = request.form.to_dict(flat=False)
        clitxt = data["inputtext"][0]
        fsmtemplate = data["fsmtxt"][0]
        res = parseatron.parsefsm(
                                cli_txt=clitxt,
                                fsm_template=fsmtemplate
                                )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/j2', methods=['POST'])
def j2():
    try:
        data = request.form.to_dict(flat=False)
        clitxt = data["inputtext"][0]
        fsmtemplate = data["fsmtxt"][0]
        res = parseatron.parsej2(
                                cli_txt=clitxt,
                                fsm_template=fsmtemplate
                                )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/ttp', methods=['POST'])
def ttp():
    try:
        data = request.form.to_dict(flat=False)
        clitxt = data["inputtext"][0]
        fsmtemplate = data["fsmtxt"][0]
        res = parseatron.parsettp(
                                cli_txt=clitxt,
                                fsm_template=fsmtemplate
                                )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/ttp/add', methods=['POST'])
def add_ttp():
    try:
        data = request.json
        res = netpalm.post(
                        route="ttptemplate",
                        payload=data
                        )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/j2/add', methods=['POST'])
def add_j2_config():
    try:
        data = request.json
        res = netpalm.post(
                        route="j2template/config/",
                        payload=data
                        )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/script/add', methods=['POST'])
def add_script():
    try:
        data = request.json
        res = netpalm.post(
                        route="script/add/",
                        payload=data
                        )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/webhook/add', methods=['POST'])
def add_webhook():
    try:
        data = request.json
        res = netpalm.post(
                        route="webhook/add/",
                        payload=data
                        )
        return jsonify(res)
    except Exception as e:
        return str(e)


@app.route('/<remove_temp>/remove', methods=['POST'])
def remove_webhook(remove_temp=None):
    try:
        rt = {
            "script": "script/remove/",
            "webhook": "webhook/remove/",
            "webhookj2": "j2template/webhook/",
            "configj2": "j2template/config/",
            "servicej2": "j2template/service/",
            "ttp": "ttptemplate"
        }
        data = request.json
        res = netpalm.delete(
                        route=rt[remove_temp],
                        payload=data
                        )
        return jsonify(res)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, threaded=True, debug=True)
