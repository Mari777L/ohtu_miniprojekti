from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "avain"

@app.route("/", methods =["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/viitteet", methods =["GET", "POST"])
def lisaa_viite():
    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        year = request.form.get("year", "").strip()
        reference_type = request.form.get("type", "").strip()

        if not author or not title or not year or not reference_type:
            flash("Kaikki kentät on täytettävä!")
            return redirect(url_for("index"))

        if not year.isdigit():
            flash("Vuosiluvun on oltava numero!")
            return redirect(url_for("index"))

        tallenna_viite(author, title, year, reference_type)
        flash("viite lisätty")
        return redirect(url_for("index"))
    return render_template("index.html")

def tallenna_viite(author, title, year, reference_type):
    return

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
    #app.run(host="0.0.0.0", port=80)