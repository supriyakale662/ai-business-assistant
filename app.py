from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import requests

app = Flask(__name__)

# ---------------------------
# DATABASE SETUP
# ---------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------
# FORM SUBMISSION
# ---------------------------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO leads (name, email, phone, message) VALUES (?, ?, ?, ?)",
        (name, email, phone, message)
    )
    conn.commit()
    conn.close()

    print(f"New Lead: {name}, {email}, {phone}")

    return redirect("/")

# ---------------------------
# DASHBOARD
# ---------------------------
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM leads")
    data = c.fetchall()
    conn.close()

    return render_template("dashboard.html", data=data)

# ---------------------------
# CHATBOT (FINAL WORKING)
# ---------------------------
API_KEY = "AIzaSyB1mCAKk-o-C3ihjgq_g9HC_dUckaxV7cw"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()

    if "hello" in user_message:
        reply = "Hello! How can I help you today?"
    elif "ai" in user_message:
        reply = "AI (Artificial Intelligence) is technology that allows machines to think and learn like humans."
    elif "python" in user_message:
        reply = "Python is a popular programming language used for web development, AI, and data science."
    else:
        reply = "I am your AI assistant. Please ask something related to business or technology."

    return jsonify({"reply": reply})

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)