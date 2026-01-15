from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.error(f'Failed to send email: {e}')


def send_email(subject, sender=None, recipients=None, text_body=None, html_body=None,
               attachments=None, sync=False):
    if sender is None:
        sender = current_app.config.get('MAIL_DEFAULT_SENDER') or \
                 current_app.config.get('MAIL_USERNAME') or \
                 'noreply@localhost'
    
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients or [],
        body=text_body,
        html=html_body
    )
    
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    
    if sync:
        mail.send(msg)
    else:
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()