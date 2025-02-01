from ultralytics import YOLO
import cv2

# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")  # Use "yolov8s.pt" or larger models for better accuracy

# Open the webcam (0 = default camera)
cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # Set width
cap.set(4, 1080)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 on the frame
    results = model(frame, classes=[0])

    # Annotate the frame with detected objects

    annotated_frame = results[0].plot()
    cv2.imshow("Person Detection", annotated_frame)

    resized_frame = cv2.resize(annotated_frame, (1920, 1080))
    # Show the frame

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()