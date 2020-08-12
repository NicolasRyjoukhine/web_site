import smtplib
import ssl
import imghdr
import random

from email.message import EmailMessage


files = []

def code_generator(max_val, min_val):
    code = random.randint(min_val, max_val)
    return code


def verification_email_sender(title, sender, receiver, message, filesimport,code, password):
    message_email = message + str(code)
    msg = EmailMessage()
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(message_email)
    msg.add_alternative('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body class="lead" style="text-align: center">
    <h5>
        thank you for registering on our website
    </h5>
    <br>
    <p>This is your confirmation code:{}</p>
</body>
</html>'''.format(code), subtype='html')

    if len(filesimport) != 0:
        for file in filesimport:
            with open(file) as f:
                file_type = imghdr.what(f.name)
                msg.add_attachment(file_type, maintype='image',
                                   subtype=imghdr.what(None, file_type))

    context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login('nicoryj.pythonbotpycharm@gmail.com', password)
    smtp.send_message(msg)





print('email sended!')