from flask import Flask, render_template, redirect, url_for, request, json

app = Flask(__name__)


@app.route("/starter")
def starter():
    return render_template("starter.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/index2")
def index_two():
    return render_template("index2.html")


@app.route("/index3")
def index_three():
    return render_template("index3.html")


@app.route("/widgets")
def widgets():
    return render_template("pages/widgets.html")


@app.route("/calendar")
def calendar():
    return render_template("pages/calendar.html")


@app.route("/gallery")
def gallery():
    return render_template("pages/gallery.html")


@app.route("/charts/<template>")
def charts(template):
    template = template.replace(".html", "")
    return render_template(f"pages/charts/{template}.html")


@app.route("/examples/<template>")
def examples(template):
    template = template.replace(".html", "")
    return render_template(f"pages/examples/{template}.html")


@app.route("/forms/<template>")
def forms(template):
    template = template.replace(".html", "")
    return render_template(f"pages/forms/{template}.html")


@app.route("/layout/<template>")
def layout(template):
    template = template.replace(".html", "")
    return render_template(f"pages/layout/{template}.html")


@app.route("/mailbox/<template>")
def mailbox(template):
    template = template.replace(".html", "")
    return render_template(f"pages/mailbox/{template}.html")


@app.route("/tables/<template>")
def tables(template):
    template = template.replace(".html", "")
    return render_template(f"pages/tables/{template}.html")


@app.route("/ui/<template>")
def ui(template):
    template = template.replace(".html", "")
    return render_template(f"pages/UI/{template}.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, threaded=True)