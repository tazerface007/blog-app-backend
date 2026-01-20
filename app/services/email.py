import os

from flask import render_template_string
from flask_mail import Message
from datetime import datetime

def send_email(name, subject, recipient, template, **kwargs):
    msg = Message(f'{subject}', recipients=[recipient])
    msg.body = render_template_string(template, name=name, **kwargs)
    return msg