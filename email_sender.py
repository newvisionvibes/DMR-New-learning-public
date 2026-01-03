# email_sender.py
"""
Email Sender Module
Handles SMTP configuration and email delivery
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    """Send emails via SMTP"""
    
    def __init__(self, smtp_server, smtp_port, sender_email, app_password):
        """Initialize with SMTP credentials"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.app_password = app_password
    
    def send_email(self, recipient_email, subject, html_content):
        """Send HTML email"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            part = MIMEText(html_content, "html")
            msg.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.sendmail(
                    self.sender_email,
                    recipient_email,
                    msg.as_string()
                )
            
            return True, "Email sent successfully!"
        
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def test_connection(self):
        """Test SMTP connection"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
            return True, "Connection successful!"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
