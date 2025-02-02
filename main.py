import MongoHandler
import YOLOv8

def main():
    """Launches a Weapon Detection Model to detect weapons then uploads the data of found weapons to MongoDB"""
    YOLOv8.launch_weapon_detection_model()
    MongoHandler.upload_to_db()

if __name__ == "__main__":
    main()