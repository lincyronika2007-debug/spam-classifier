from flask import Flask, render_template, request
import pickle
import sqlite3


app = Flask(__name__)

# Load trained model
app = Flask(__name__)

# Load trained model safely
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    msg = request.form["message"]

    data = vectorizer.transform([msg])
    result = model.predict(data)

    output = "Spam" if result[0] == 1 else "Not Spam"

    # Save to database
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (text, prediction) VALUES (?, ?)",
        (msg, output)
    )
    conn.commit()
    conn.close()

    return render_template("index.html", prediction=output)

# History page
@app.route("/history")
def history():
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()
    conn.close()

    return render_template("history.html", data=data)

# Main run (ngrok + Flask)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=50000)
