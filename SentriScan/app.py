from flask import Flask, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
import certifi
from YOLOv8_backend import launch_weapon_detection_model

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB Connection
uri = "mongodb+srv://@freedb.xh3be.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client.SpartaHack
collection = db.Detections

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    socketio.start_background_task(start_detection)

def start_detection():
    """Runs YOLO and emits detected threats to WebSocket & MongoDB"""
    for detected_threat in launch_weapon_detection_model():
        collection.insert_one(detected_threat)
        socketio.emit("detection", detected_threat)

@app.route("/get-threats", methods=["GET"])
def get_threats():
    """Fetch past detected threats from MongoDB"""
    threats = list(collection.find().sort("timestamp", -1))
    for threat in threats:
        threat["_id"] = str(threat["_id"])
    return jsonify(threats)

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8081, debug=True, allow_unsafe_werkzeug=True)
