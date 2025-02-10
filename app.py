from flask import Flask, render_template, request, send_from_directory
from generate_logo import generate_logo

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        style = request.form.get("style")
        description = request.form.get("description")
        image_path = generate_logo(style, description)
        if image_path:
            return render_template("index.html", image_path=image_path)
        else:
            return render_template("index.html", error="Не удалось сгенерировать логотип.")
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)