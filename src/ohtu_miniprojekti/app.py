from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "avain"

@app.route("/", methods =["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/viitteet", methods =["GET", "POST"])
def lisaa_viite():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        reference_type = request.form["type"]
        tallenna_viite(author, title, year, reference_type)
        flash("viite lisätty")
        return redirect(url_for("index"))
    return render_template("index.html")

def tallenna_viite(author, title, year, reference_type):
    return

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
    #app.run(host="0.0.0.0", port=80)