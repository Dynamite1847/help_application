from flask import jsonify, Flask
from flask_mail import Mail, Message

app = Flask(__name__)



def send_email(app):
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'help_application@163.com'
    MAIL_PASSWORD = 'STHZAMLLAFSCKGNA'
    app.config.update(
        SECRET_KEY="SECRET KEY",
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=MAIL_USERNAME
    )
    mail = Mail(app)
    return mail


def send_mail(to, body, mail,title):
    message = Message(title, recipients=[to], body=body)
    mail.send(message)




