import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body, to_email):
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")  # Gmail App Password

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email error:", e)



send_email("testing", "sent from python class", "adeyemiemmanuel547@gmail.com")