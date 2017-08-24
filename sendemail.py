#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
import codecs

sender = 'xiaochen@meizu.com'
receiver = 'xiaochen@meizu.com'
subject = 'trello task report'
username = 'xiaochen@meizu.com'
password = 'kelfy-666'


def get_email_content():
    try:
        file = codecs.open('ad_task.txt', 'r', encoding='utf-8')
        data = file.readlines()
        file.close()
    except Exception:
        print('read mail content error')
        sys.exit(0)

    return data


def content_html():
    body = get_email_content()

    list_name = "".join(body[0])
    card_stat = "".join(body[1])
    label_stat = "".join(body[2])
    member_stat = "".join(body[3][1:-2])
    requirement_stat = "".join(body[4])

    content = '<div><strong>' + list_name + '</strong></div><br/>' + \
              '<div style="color:red">' + card_stat + '</div><br/>' + \
              '<div>' + label_stat + '</div><br/>' + \
              '<div>' + member_stat + '</div><br/>' + \
              '<div>' + requirement_stat + '</div>'

    return content


def send_email():
    content = content_html()

    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.meizu.com')
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print('send email success')
    except smtplib.SMTPException:
        print('Error')
