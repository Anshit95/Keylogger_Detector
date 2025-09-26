import sys
import os
import datetime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Fix template path for PyInstaller
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

socketio = SocketIO(app)
suspicious_logs = []

@app.route("/")
def home():
    return render_template("index.html", logs=suspicious_logs)

@app.route("/test_page1")
def test_page1():
    return render_template("test_page1.html")

@app.route("/test_page2")
def test_page2():
    return render_template("test_page2.html")

@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    suspicious_logs.clear()
    socketio.emit("logs_cleared", to=None)
    return {"status": "cleared"}

@socketio.on("suspicious_event")
def handle_suspicious_event(data):
    key = data.get("key")
    website = data.get("website")
    log_entry = f"{datetime.datetime.now().strftime('%H:%M:%S')} - {website} - Key: '{key}'"
    suspicious_logs.append(log_entry)
    emit("new_log", {"log": log_entry}, to=None)

if __name__ == "__main__":
    socketio.run(app, debug=True)

