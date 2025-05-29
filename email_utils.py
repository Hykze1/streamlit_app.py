import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(new_shows, sender_email, sender_password, recipient_email):
  subject = f"New IBDB Shows Detected: {len(new_shows)} New Show(s)"
    body = "New shows found:\n\n"
    for show in new_shows:
        body += f"- {show['Title']} (Opening: {show['Opening Date']})\n  Link: {show['Detail Link']}\n\n"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Notification email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
