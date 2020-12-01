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


def send_mail(to, body, mail):
    message = Message('Congratulations！Someone has taken your task!', recipients=[to], body=body)
    mail.send(message)

@app.route("/")
def test_mail():
    mail = send_email(app)
    send_mail('yudong1864@gmail.com', '有人申请了你的任务，请速去查看', mail)
    print("success")

if __name__ == "__main__":
    app.run(host='0.0.0.0')


