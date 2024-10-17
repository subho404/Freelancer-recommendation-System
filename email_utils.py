import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, project_title, message_body):
    from_email = "your_email@example.com"
    password = "your_password"

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Project Opportunity: {project_title}"

    body = f"You have been recommended for the following project: {project_title}\n\n{message_body}"
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()
