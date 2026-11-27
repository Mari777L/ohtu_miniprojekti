from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "avain"

@app.route("/", methods =["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/viitteet", methods =["GET", "POST"])
def lisaa_viite():
    if request.method == "POST":
        citation_key = request.form.get("citation_key", "").strip()
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

        tallenna_viite(citation_key, author, title, year, reference_type)
        flash("viite lisätty")
        return redirect(url_for("index"))
    return render_template("index.html")

def tallenna_viite(citation_key, author, title, year, reference_type):
    with sqlite3.connect("viitteet.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS viitteet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                citation_key TEXT NOT NULL,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                reference_type TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO viitteet (citation_key, author, title, year, reference_type) "
            "VALUES (?, ?, ?, ?, ?)",
            (citation_key, author, title, int(year), reference_type),
        )
    conn.close()

def hae_viitteet():
    with sqlite3.connect("viitteet.db") as conn:
        conn.row_factory = sqlite3.Row

        viitteet = conn.execute(
            "SELECT * FROM viitteet ORDER BY id DESC"
        ).fetchall()

    return viitteet

@app.route("/viitelista")
def viitelista():
    viitteet = hae_viitteet()
    return render_template("viitelista.html", viitteet=viitteet)

@app.route("/muokkaa/<int:id>", methods=["GET", "POST"])
def muokkaa_viite(id):
    with sqlite3.connect("viitteet.db") as conn:
        conn.row_factory = sqlite3.Row

        viite = conn.execute(
            "SELECT * FROM viitteet WHERE id = ?",
            (id,)
        ).fetchone()

        if viite is None:
            flash("Viitettä ei löytynyt!")
            return redirect(url_for("viitelista"))

        if request.method == "POST":

            citation_key = request.form.get("citation_key", "").strip()
            author = request.form.get("author", "").strip()
            title = request.form.get("title", "").strip()
            year = request.form.get("year", "").strip()
            reference_type = request.form.get("type", "").strip()

            
            conn.execute("""
                UPDATE viitteet
                SET citation_key = ?,
                    author = ?,
                    title = ?,
                    year = ?,
                    reference_type = ?
                WHERE id = ?
            """, (
                citation_key,
                author,
                title,
                int(year),
                reference_type,
                id
            ))

            flash("Viite päivitetty!")
            return redirect(url_for("viitelista"))

    return render_template("muokkaa_viite.html", viite=viite)

@app.route("/poista/<int:id>", methods=["POST"])
def poista_viite(id):

    with sqlite3.connect("viitteet.db") as conn:

        conn.execute(
            "DELETE FROM viitteet WHERE id = ?",
            (id,)
        )

    flash("Viite poistettu!")

    return redirect(url_for("viitelista"))


    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
    #app.run(host="0.0.0.0", port=80)