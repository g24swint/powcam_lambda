import json
import boto3
import urllib.request
from email.message import EmailMessage
from email.utils import make_msgid

ses = boto3.client('ses')

sender = 'Galen <galen.swint@gmail.com>'
recipient = 'The Bear <gssbear@gmail.com>'
recipient_list = [recipient]

subject = "Today's PowCam. Amazon SES test (sdk in lambda)"

counter = 0

def get_picture():
    url = 'http://skicb.server310.com/ftp/powcam/pow.jpg'
    
    resp = urllib.request.urlopen(url)
    picture = resp.read()
    
    return picture

def build_email():
    msg = EmailMessage()

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.preamble = 'Trying out a send.'
    msg.set_content = "Hello. Today's PowCam grab. Maybe."
    
    powcam_cid = make_msgid()
    stripped_powcam_cid = powcam_cid[1:-1]
    html_msg = f'''
        <html>
        <head />
        <body>
        <p>PowCam from today. Maybe.</p>
        <img src="cid:{stripped_powcam_cid}"
        </bod>
        </html>'''
    
    pow_cam_img = get_picture()
    
    msg.add_alternative(html_msg, subtype='html')
    msg.get_payload()[0].add_related(pow_cam_img, 'image', 'jpeg', 
        cid=powcam_cid)
    
    return msg

def lambda_handler(event, context):
    # TODO implement
    global counter
    
    counter = counter+1
    
    body_text = f'Simple email send #{counter} through SES.'
    
    # pow_cam_picture = get_picture()
    
    email_dict = {'Source': sender,
        'Destination': {'ToAddresses': recipient_list},
        'Message': {
            'Subject': {'Data':subject}, 
            'Body': {'Text': {'Data': body_text}},
        },
    }
        
    # response = ses.send_email(**email_dict)
    
    built_message = build_email()
    
    response = ses.send_raw_email(Source=sender,
        Destinations=recipient_list,
        RawMessage={'Data': built_message.as_bytes()})
    
    return response
