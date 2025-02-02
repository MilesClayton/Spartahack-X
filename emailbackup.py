import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


# Function to send an email
def send_email(to_email, subject, name, data):
    # Email sender details
    sender_email = "neospartansalert@gmail.com"
    sender_password = "oqdu tzvs nznf wtsl"

    # SMTP server setup (for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject


    # Generic string with variables
    body = f"""
    {name},

    🚨 : ARMED ASSAILANT 🚨

    An armed assailant has been reported in the area. 
    Seek immediate shelter, lock doors, and stay away from windows. 
    Remain quiet and follow emergency protocols. Await further instructions from law enforcement. 
    If you are in immediate danger, call 911. Do not approach the suspect. Stay alert and stay safe.
    
    Confidence in prediction: {data["conf"]}
    Location: {data["location_data"]}
    Date/Time: {data["date"]}
    Threat Type: {data["object"]}
    """

    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()

        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Example usage
# send_email("Robert3cannon@gmail.com", "ALERT! ARMED ASSAILANT", "Robert Cannon",) # email to send to, subject to email, first and last name
