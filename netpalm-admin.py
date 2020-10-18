from flask import Flask, render_template, request

from backend.confload.confload import Config
from backend.netpalm.netpalm_adapter import NetpalmAdapter

from urllib import parse

app = Flask(__name__)
conf = Config()
netpalm = NetpalmAdapter()

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
    total_success_percent = "{:.2f}".format((total_successful_jobs / total_jobs) * 100)
    total_failed_percent = "{:.2f}".format((total_failed_jobs / total_jobs) * 100)

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
            container_set.add(worker["hostname"])
            if "fifo" in worker["name"]:
                container_types["fifo"] += 1
            if "fifo" not in worker["name"] and "processworker" not in worker["name"]:
                container_types["pinned"] += 1
            total_processes += 1

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
                        total_processes=total_processes
                        )


@app.route("/parser/ttp")
def ttp_parser():
    ttpdata = netpalm.get("ttptemplate")
    return render_template(
                        "universal-template-table.html",
                        heading="TTP loaded parsers",
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


@app.route("/template_editor/<template_type>")
def template_editor(template_type=None):
    data = netpalm.template_editor(template_type)
    return render_template(
                        "template_editor.html",
                        heading=template_type,
                        data=data
                        )


@app.route("/rendering_editor/<template_type>")
def rendering_editor(template_type=None):
    data = netpalm.template_editor(template_type)
    return render_template(
                        "rendering_editor.html",
                        heading="Rendering editor",
                        data=data
                        )


@app.route("/custom_editor/<template_type>")
def custom_editor(template_type=None):
    data = netpalm.template_editor(template_type)
    return render_template(
                        "custom_editor.html",
                        heading="Custom extensibles editor",
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, threaded=True, debug=True)
