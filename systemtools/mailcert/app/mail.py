import smtplib, json
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import app.config as config

def smail(certhostname, crtmessage):
    msgTxt = MIMEMultipart()
    msgTxt['Subject'] = 'Certificate request for ' + certhostname + ' ' + str(date.today() - timedelta(days = 1))
    msgTxt['From'] = config.settings.fromaddr
    msgTxt['To'] = config.settings.toaddr
    msgTxt.preamble = 'This is multi-part message in MIME Format.'

    msgTxt.attach(MIMEText('Please see attached certificate for: ' + certhostname))
    msgTxt.attach(MIMEText(crtmessage.strip('"').replace('\\n', '\n'),'plain'))

    try:
        smtp = smtplib.SMTP()
        smtp.connect(host= config.settings.smtphost, port= config.settings.smtpport)
        smtp.sendmail(config.settings.fromaddr, config.settings.toaddr, msgTxt.as_string().encode('utf-8'))
        smtp.quit()
        return json.loads('{"success": "True", "status": 200}')
    except:
        return json.loads('{"success": "False", "status": 400}')