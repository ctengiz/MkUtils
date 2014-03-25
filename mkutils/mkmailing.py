#-*- coding: utf-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from html2text import html2text
from email.utils import formataddr
from email.utils import formatdate
from email.utils import COMMASPACE


def send_mail( msg_from,
               msg_to,
               msg_subject,
               msg_body,
               msg_from_name='',
               msg_attach=[],
               smtp_server='localhost',
               smtp_port=25,
               smtp_user='',
               smtp_pass='',
               smtp_do_auth=True,
               smtp_start_tls=True
               ):


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('mixed')
    #Eskisi : msg = MIMEMultipart('alternative')
    msg.set_charset("utf-8")

    msg['Subject'] = Header(msg_subject, 'utf-8')
    msg['Date'] = formatdate(localtime=1)

    if msg_from_name:
        msg['From'] = formataddr((Header(msg_from_name, 'utf-8').encode('utf-8'),  msg_from))
    else:
        msg['From'] = formataddr((msg_from,  msg_from))

    if isinstance(msg_to, list):
        msg['To'] = COMMASPACE.join(msg_to)
    else:
        msg['To'] = msg_to
    msg.preamble = 'This is a multi-part message in MIME format.'

    msg_related = MIMEMultipart('related')
    msg.attach(msg_related)

    msg_alternative = MIMEMultipart('alternative')
    msg_related.attach(msg_alternative)

    textpart = MIMEText(html2text(msg_body), 'plain', _charset='utf-8')
    htmlpart = MIMEText(msg_body, 'html', _charset='utf-8')

    #msg_text = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    msg_alternative.attach(textpart)

    #msg_html = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    msg_alternative.attach(htmlpart)

    '''
    Eski kodd !
    # Record the MIME types of both parts - text/plain and text/html.
    #todo: convert html to text
    textpart = MIMEText(html2text(msg_body), 'plain', _charset='utf-8')
    htmlpart = MIMEText(msg_body, 'html', _charset='utf-8')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(textpart)
    msg.attach(htmlpart)
    '''

    '''
    #################################
    ## DOSYA EKLEME
    #################################
    for i, img in enumerate(img_list):
        with open(img, 'rb') as fp:
            msg_image = MIMEImage(fp.read())
            msg_image.add_header('Content-ID', '<image{}>'.format(i))
            msg_related.attach(msg_image)

    for attachment in attachments:
        fname = os.path.basename(attachment)

        with open(attachment, 'rb') as f:
            msg_attach = MIMEBase('application', 'octet-stream')
            msg_attach.set_payload(f.read())
            encoders.encode_base64(msg_attach)
            msg_attach.add_header('Content-Disposition', 'attachment',
                                  filename=(Header(fname, 'utf-8').encode()))
            msg_root.attach(msg_attach)
    '''

    # Send the message via local SMTP server.
    s = smtplib.SMTP(smtp_server, smtp_port)
    if smtp_start_tls:
        s.starttls()
    if smtp_do_auth:
        s.login(smtp_user, smtp_pass)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    x = s.sendmail(msg_from, msg_to, msg.as_string())
    s.quit()

