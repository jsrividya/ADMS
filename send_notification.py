from smtplib import SMTP, SMTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_notification(patient, receiver):
    msg = MIMEMultipart()
    sender = 'adms.server@gmail.com'
    receivers = [receiver]
    msg['Subject'] = 'ADMS Registration'
    msg['To'] = receiver
    msg['From'] = sender
    content = """\
    <html>
      <head></head>
      <body>
        <p>Hi %s<br><br>
           Congratulations!! Your ADMS account has been created.<br><a href="http://0.0.0.0:4000/">Click here</a> to access you account.<br><br><br><br>
           Thank you,<br>
           ADMS Team
        </p>
      </body>
    </html>
    """ % patient
    body = MIMEText(content, 'html')
    # content = 'This is a test body'
    # body = MIMEText(content, 'text')
    msg.attach(body)
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender, 'A1z24B2y23')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print('Email Sent to: ' + receiver)
        smtpObj.quit()
    except SMTPException:
        print('Email failed')

