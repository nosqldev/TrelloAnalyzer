#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys
import codecs


def get_email_content():
    try:
        fp = codecs.open('data/task_stat.txt', 'r', encoding='utf-8')
        data = fp.readlines()
        fp.close()
    except IOError:
        print('read mail content error')
        sys.exit(0)

    return data


def content_html():
    body = get_email_content()

    list_name = "".join(body[0])
    card_stat = "".join(body[1])
    label_stat = "".join(body[2])
    member_stat = "".join(body[3])
    requirement_stat = "".join(body[4])

    content = '<div><strong>' + list_name + '</strong></div><br/>' + \
              '<div style="color:red">' + card_stat + '</div><br/>' + \
              '<div>' + label_stat + '</div><br/>' + \
              '<div>' + member_stat + '</div><br/>' + \
              '<div>' + requirement_stat + '</div>'

    return content


def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage


def send_email(board_name, sender, receiver, username, password):
    content = content_html()
    subject = board_name + " 迭代任务统计"

    msg = MIMEMultipart('related')
    msgtext = MIMEText(content + '<br><img src=\"cid:weekly\" border=\"1\">' +
                       '<br><img src=\"cid:burn_down\" border=\"1\">', 'html', 'utf-8')
    msg.attach(msgtext)
    msg.attach(addimg("img/work_hours_chart.png", "weekly"))
    msg.attach(addimg("img/burn_down_chart.png", "burn_down"))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.meizu.com')
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        print('\n------------> Send email...')
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()
        print('send email success')
    except smtplib.SMTPException as e:
        print('Error: ' + str(e))
