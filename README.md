# Spartahack-X
Weapon Detection Model

This project trains a YOLOv8 object detection model to detect guns in images. It utilizes a pre-trained YOLOv8 model and fine-tunes it with a dataset obtained from Kaggle.

This dataset contains labeled images of guns, which were used to train the YOLOv8 model for object detection. Each image has an associated .txt file containing the annotation details, specifying the location of the gun within the image in YOLO format. This annotation format includes the class index, x and y coordinates, width, and height of the bounding box, making it directly compatible with YOLOv8 without requiring additional conversion.
