import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from os import getenv


def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))


def send_verification_email(
    email: str,
    code: str,
    custom_gmail_email: Optional[str] = None,
    custom_gmail_password: Optional[str] = None
) -> bool:
    """
    Send verification email with code using Gmail SMTP
    Can use custom Gmail credentials or fall back to environment variables
    """
    try:
        # Use custom credentials if provided, otherwise use environment variables
        gmail_email = custom_gmail_email or getenv('GMAIL_EMAIL')
        gmail_password = custom_gmail_password or getenv('GMAIL_PASSWORD')
        
        if not gmail_email or not gmail_password:
            print("[WARNING] Gmail credentials not configured. Verification code:", code)
            return False
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Email Verification Code - StudentSystem'
        message['From'] = gmail_email
        message['To'] = email
        
        # HTML email body
        html = f"""\
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #667eea;">Verify Your Email</h2>
              <p>Welcome to StudentSystem! Your verification code is:</p>
              <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                <h1 style="color: #667eea; letter-spacing: 5px; margin: 0;">{code}</h1>
              </div>
              <p>This code will expire in 10 minutes.</p>
              <p>If you didn't request this, please ignore this email.</p>
              <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
              <p style="color: #666; font-size: 12px;">© 2026 StudentSystem. All rights reserved.</p>
            </div>
          </body>
        </html>
        """
        
        part = MIMEText(html, 'html')
        message.attach(part)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_email, gmail_password)
            server.sendmail(gmail_email, email, message.as_string())
        
        print(f"[EMAIL] Verification code {code} sent to {email}")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Gmail authentication failed. Check your email and app password.")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send email: {str(e)}")
        return False
