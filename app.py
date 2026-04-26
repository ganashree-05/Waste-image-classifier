from flask import Flask, render_template, request, jsonify, redirect, session
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

# Load model
model = tf.keras.models.load_model("model/waste_model.h5")

classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create DB
conn = sqlite3.connect("users.db")
conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.close()


def get_disposal(label):
    return {
        "metal": "♻️ Use metal recycling bin",
        "paper": "♻️ Paper recycling bin",
        "plastic": "♻️ Plastic recycling bin",
        "cardboard": "♻️ Flatten & recycle cardboard",
        "glass": "♻️ Glass recycling bin",
        "trash": "🗑️ General waste bin"
    }.get(label, "Check local guidelines")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            session["user"] = user
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        conn.execute("INSERT INTO users VALUES (?,?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No file uploaded"})

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    img = image.load_img(path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]
    idx = np.argmax(preds)

    label = classes[idx]
    confidence = float(preds[idx]) * 100

    if confidence < 70:
        label = "trash"

    return jsonify({
        "class": label,
        "confidence": round(confidence, 2),
        "disposal": get_disposal(label)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)