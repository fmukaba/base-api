import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader, Template
from core.config import settings
from notifications.schemas import EmailSchema

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
templates_dir = os.path.join(parent_dir, 'templates')

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(templates_dir))

def send_email(email: MIMEMultipart):
    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_username, email["To"], email.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email could not be sent: {str(e)}")
    

def send_email_with_link(email: EmailSchema, template: Template, url: str):
    html_content = template.render(
        subject=email.subject,
        recipient_name=email.target,
        url=url
    )

    msg = MIMEMultipart('alternative')
    msg['Subject'] = email.subject
    msg['From'] = settings.smtp_username
    msg['To'] = email.target

    msg.attach(MIMEText(html_content, 'html'))
    
    send_email(msg)

def send_verification_email(email: EmailSchema, verification_url: str):
    template = env.get_template('email_verification.html')
    send_email_with_link(email, template, verification_url)
     
def send_reset_password_email(email: EmailSchema, reset_url: str):
    template = env.get_template('reset_password_email.html')
    send_email_with_link(email, template, reset_url)