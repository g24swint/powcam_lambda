import datetime as dt
import json
import boto3
import urllib.request
from email.message import EmailMessage
from email.utils import make_msgid

ses = boto3.client('ses')

sender = 'Galen Live <swintgs@live.com>'
recipient = 'TheBear <gssbear@gmail.com>'
recipient_list = ['melissa.swint@gmail.com', 'galen.swint@gmail.com',
    'henrylinhart@hotmail.com',
    'graham.s.swint@gmail.com',
    'hannah.c.swint@gmail.com',
    'laurel.a.swint@gmail.com',
    ]

subject = "PowCam for "


def get_picture():
    url = 'http://skicb.server310.com/ftp/powcam/pow.jpg'
    
    resp = urllib.request.urlopen(url)
    picture = resp.read()
    
    return picture

def build_email():
    now = dt.datetime.now(tz=dt.timezone(dt.timedelta(hours=-7)))
    time_is = f'{now.year}/{now.month:02}/{now.day:02} at {now.hour}:{now.minute} MDT'
    day_is = f'{now.year}/{now.month:02}/{now.day:02}'
    
    msg = EmailMessage()

    msg['From'] = sender
    msg['To'] = ', '.join(recipient_list)
    msg['Subject'] = subject + f" {day_is}"
    msg.preamble = 'Trying out a send.'
    msg.set_content = "Hello. Today's PowCam grab. Maybe."
    
    powcam_cid = make_msgid()
    stripped_powcam_cid = powcam_cid[1:-1]
    
    html_msg = f'''
        <html>
        <head />
        <body>
        <p>PowCam from {time_is}. Maybe.</p>
        <p><a href="http://www.skicb.com/the-mountain/web-cams">Link to the 
        Crested Butte Webcam Page.</a></p>
        <img src="cid:{stripped_powcam_cid}"
        </bod>
        </html>'''
    
    pow_cam_img = get_picture()
    
    msg.add_alternative(html_msg, subtype='html')
    msg.get_payload()[0].add_related(pow_cam_img, 'image', 'jpeg', 
        cid=powcam_cid)
    
    return msg

def lambda_handler(event, context):

    built_message = build_email()
    
    response = ses.send_raw_email(Source=sender,
        Destinations=recipient_list,
        RawMessage={'Data': built_message.as_bytes()})
    
    return response

