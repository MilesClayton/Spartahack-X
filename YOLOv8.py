from ultralytics import YOLO
import cv2
import os
from datetime import datetime
import base64
import json
import geocoder


def encode_to_json(conf, object, image_file_path, image_file_name, geocode):
    data = {
        "conf" : round(conf, 4),
        "object" : object,
        "date" : datetime.now().__str__(),
        "location_data" : f"{geocode.city}, {geocode.state}, {geocode.country}"
    }
    with open(image_file_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    image_file.close()
    data["image_name"] = image_file_name
    data["image_data"] = base64_string
    with open("Detected_Threat_Data/data.json", "w") as json_file:
        json.dump(data, json_file)
    json_file.close()

def launch_weapon_detection_model():
    # Load the pre-trained YOLOv8 model
    model = YOLO("model.pt")  # Use "yolov8s.pt" or larger models for better accuracy

    save_dir = "Detected_Threat_Data/"
    # Open the webcam (0 = default camera)
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set width
    cap.set(4, 720)
    threatDetected = False;
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 on the frame
        results = model(frame, classes=[0], conf=.5)
        for result in results:
            for box in result.boxes:
                confidence = box.conf.item()
                object = model.names[int(box.cls.item())]
                print(f"Confidence Score = {confidence:.4f}")
                print(f"Object = {object}")
                confidence = box.conf.item()  # Confidence score
                object_name = model.names[int(box.cls.item())]  # Object class name

                if confidence > 0.8:  # Apply confidence threshold
                    # Draw bounding box and label
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordinates of the box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{object_name} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    # Save or store the frame where an object was detected
                    now = datetime.now()
                    frame_file = f"detected_threat_{confidence:.2f}_{object_name}_{now.year}-{now.month}-{now.day}.jpg"
                    frame_filename = os.path.join(save_dir, frame_file )
                    cv2.imwrite(frame_filename, frame)
                    threatDetected = True
                    g = geocoder.ip('me')
                    encode_to_json(conf=confidence, object=object_name, image_file_path=frame_filename, image_file_name=frame_file, geocode=g)

        # Annotate the frame with detected objects

        annotated_frame = results[0].plot()
        cv2.imshow("SentriScan", annotated_frame)

        resized_frame = cv2.resize(annotated_frame, (1920, 1080))
        # Show the frame

        # Press 'q' to exit
        if (cv2.waitKey(1) & 0xFF == ord("q")) or threatDetected:
            break

    cap.release()
    cv2.destroyAllWindows()