#!/usr/bin/env python3

import configparser, os, smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from optparse import OptionParser, SUPPRESS_HELP

# Setting config file and read values.
def main():
    config = configparser.ConfigParser()
    try:
        config.read('sar.conf')
    except:
        print("error reading configuration file")
        
    parser = OptionParser(add_help_option=False)
    parser.add_option("-l", "--location", dest="location", help="provide location of image, must proide", default=os.getcwd() + '/img')
    parser.add_option("-s", "--sender", dest="sender", help="Sender email address", default=config.get('DEFAULT', 'DEFAULT_SENDER'))
    parser.add_option("-t", "--to", dest="to", help="reciever's email address", default=config.get('DEFAULT', 'DEFAULT_RECIPIENT'))
    parser.add_option("-r", "--relay", dest="smtphost", help="smtp relay host", default=config.get('DEFAULT', 'SMTP_SERVER'))
    parser.add_option("-p", "--port", dest="smtpport", help="smtp relay server port", default=config.get('DEFAULT', 'SMTP_PORT'))
    parser.add_option("-h", "--help", action="help")
    
    (options, args) = parser.parse_args()
    status = smail(options)
    if status:
        print('Message Sent')
        if cleanImage(options.location):
            print('Images removed')
        else:
            print('Image Removal Failed')
    else:
        print('Message Failed')

# print(config.get('DEFAULT', 'SMTP_PORT'))
def smail(options):
    msgTxt = MIMEMultipart('related')
    msgTxt['Subject'] = 'System Status' + os.uname().nodename + ' ' + str(date.today() - timedelta(days = 1))
    msgTxt['From'] = options.sender
    msgTxt['To'] = options.to
    msgTxt.preamble = 'This is multi-part message in MIME Format.'

    msgAlternative = MIMEMultipart('alternative')
    msgTxt.attach(msgAlternative)

    msgPlain = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgPlain)

    msgHTML = MIMEText('<b>Daily System Usage: ' + str(date.today() - timedelta(days = 1)) + genhtml(options.location), 'html')
    msgAlternative.attach(msgHTML)

    msgTxt = addimage(options.location, msgTxt)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(host= options.smtphost, port= options.smtpport)
        smtp.sendmail(options.sender, options.to, msgTxt.as_string().encode('utf-8'))
        smtp.quit()
        return True
    except:
        return False

def genhtml(location):
    textmsg = ''
    for filename in os.listdir(location):
        if filename.endswith('.png'):
            textmsg = textmsg + '<br><img src=cid:"' + filename + '"><br>'
        else:
            continue
    return textmsg

def addimage(location, msgTxt):
    for filename in os.listdir(location):
        if filename.endswith('.png'):
            fp = open(os.path.join(location, filename), 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<%s>' %(filename))
            msgImage.add_header('Content-Disposition', "inline; filename= %s" % filename)
            msgTxt.attach(msgImage)
        else:
            continue
    return msgTxt

def cleanImage(location):
    for filename in os.listdir(location):
        try:
            os.remove(os.path.join(location, filename))
        except Exception as e:
            print(e)
            return False
            raise
    return True


if __name__ == "__main__":
    main()

