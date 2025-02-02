import MongoHandler
import YOLOv8
import emailbackup

def main():
    """Launches a Weapon Detection Model to detect weapons then uploads the data of found weapons to MongoDB"""
    YOLOv8.launch_weapon_detection_model()
    db = MongoHandler.upload_to_db()
    emailbackup.send_email("cosohoj646@andinews.com", "EMERGENCY ALERT!!", "Eliezer", MongoHandler.download_from_db(db))

if __name__ == "__main__":
    main()