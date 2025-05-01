import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

def send_email(html, subject, target):
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = target
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP(
            os.getenv('EMAIL_SERVER'),
            os.getenv('EMAIL_PORT')
        )
        server.login(
            os.getenv('EMAIL_USER'),
            os.getenv('EMAIL_PASSWORD')
        )
        server.sendmail(
            os.getenv('EMAIL_USER'),
            target,
            msg.as_string()
        )
        server.quit()
    except smtplib.SMTPResponseException as err:
        print(err)