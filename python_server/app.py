from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/preview.html")
def preview():
    return render_template("preview.html")

@app.route("/preview/<cluster_name>")
def preview_cluster(cluster_name):
    return render_template("preview.html")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True, port=8088)
