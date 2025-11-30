from flask import Flask, render_template, request
from db_config import get_connection
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    floor = request.form["floor"]
    flat_no = request.form["flat_no"]
    amount = request.form["amount"]

    image = request.files["image"]
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(save_path)

    db = get_connection()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO maintenance (name, floor, flat_no, amount, image_path) VALUES (%s, %s, %s, %s, %s)",
        (name, floor, flat_no, amount, save_path)
    )
    db.commit()
    cur.close()
    db.close()

    # Returning values back to form so fields stay filled
    return render_template(
        "form.html",
        name=name,
        floor=floor,
        flat_no=flat_no,
        amount=amount,
        message="Submitted Successfully!"
    )


@app.route("/dashboard")
def dashboard():
    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM maintenance")
    data = cur.fetchall()
    cur.close()
    db.close()

    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
