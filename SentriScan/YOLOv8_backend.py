from ultralytics import YOLO
import cv2
import base64
import time
import geocoder
import app

def launch_weapon_detection_model():
    """Runs YOLOv8 in real-time and yields detected threats"""

    model = YOLO("model.pt")
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.7)
        for result in results:
            for box in result.boxes:
                confidence = box.conf.item()
                object_name = model.names[int(box.cls.item())]

                if confidence > 0.7:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    location = geocoder.ip('me')
                    location_data = f"{location.city}, {location.state}, {location.country}"

                    # Convert frame to Base64
                    _, buffer = cv2.imencode(".jpg", frame)
                    encoded_image = base64.b64encode(buffer).decode("utf-8")

                    # Yield detection data
                    yield {
                        "weapon_detected": True,
                        "confidence": round(confidence * 100, 2),
                        "object": object_name,
                        "timestamp": timestamp,
                        "location_data": location_data,
                        "image_data": encoded_image
                    }

    cap.release()