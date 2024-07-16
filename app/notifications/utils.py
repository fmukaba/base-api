import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from core.config import settings
from notifications.schemas import EmailSchema

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, 'templates')

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('email_verification.html')

def send_email(email: MIMEMultipart):
    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_username, email["To"], email.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email could not be sent: {str(e)}")
    
def send_verification_email(email: EmailSchema, verification_url: str):
    html_content = template.render(
        subject=email.subject,
        recipient_name=email.target,
        verification_url=verification_url
    )

    msg = MIMEMultipart('alternative')
    msg['Subject'] = email.subject
    msg['From'] = settings.smtp_username
    msg['To'] = email.target

    msg.attach(MIMEText(html_content, 'html'))
    
    send_email(msg)
     