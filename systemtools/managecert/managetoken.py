#!/usr/bin/env python3
# Ketan Patel
# Small script to manage token
# Set script run using cron weekly
# Update configuration file and you are good to go.
# License MIT

import configparser, argparse, os, requests, json, smtplib
from datetime import datetime, date
from email.message import EmailMessage


def main():
    parser = argparse.ArgumentParser(prog='managecert', description='Certificate Generator.')
    parser.add_argument("--cfile", dest='cfile', help="configuration location", default='/etc/managecert.conf')
    parser.add_argument("--renew", dest='renew', help="should script renew token, if expiring", default='0')
    args = parser.parse_args()

    # Read Configuration
    config = configparser.ConfigParser()
    config.read(args.cfile)

    token, date, status = gettokeninfo(config)
    # print(token, date, status)
    if status == 'Active':
        expiring = checkdate(date)
    else:
        print('Token is expired, something went wrong in logic')
        exit(1)

    if token != config['DEFAULT']['apiToken'] and config['AUTH']['updateconfig'] == '1':
        updateconfig(token, config, args)
        print('Updated configuration to match new token')
    else:
        print('Config and current token match')

    if expiring < 2:
        if args.renew == '1':
            ntoken, ndate, nstatus, tokenrenewed = renewtoken(config)
            print('New Expiry Date is: ' + ndate)
            print('Status of new token is: ' + nstatus)
            if config['EMAIL']['enablenotify'] == '1' and tokenrenewed :
                emailer(token, ntoken, config, str(expiring))
            if config['AUTH']['printtoken'] == '1':
                print('New Token is: ' + ntoken )
            if config['AUTH']['updateconfig'] == '1':
                updateconfig(ntoken, config, args)
            else:
                print('Token updated but configuration update disabled')
        else:
            print('Token expiring, but renewal disabled, will not renew')
    else:
        print('Token validity is ' + str(expiring) + ' week')

def updateconfig(ntoken, config, args):
    config.set('DEFAULT', 'apiToken', ntoken)

    with open(args.cfile, 'w') as configfile:
        config.write(configfile)


def gettokeninfo(config):
    endpoint = config['AUTH']['endpoint']

    headers = {
        'userID': config['DEFAULT']['apiUser'],
        'apiToken': config['DEFAULT']['apiToken'],
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get(endpoint, headers=headers)
    result = json.loads(response.text)
    data = result[0]
    return data['apiToken'], data['expirationDate'], data['status']

def checkdate(date):
    date_format = "%Y-%m-%d"
    not_after = datetime.strptime(date, date_format)
    now = datetime.now()
    result = (not_after - now).days/7
    return result

def renewtoken(config):
    endpoint = config['AUTH']['endpoint'] + '/rotate'

    headers = {
        'userID': config['DEFAULT']['apiUser'],
        'apiToken': config['DEFAULT']['apiToken'],
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(endpoint, headers=headers)
    result = json.loads(response.text)
    data = result[0]
    if response.ok:
        tokenrenewed = True
    else:
        tokenrenewed = False
    return data['apiToken'], data['expirationDate'], data['status'], tokenrenewed

def emailer(token, ntoken, config, rweek):
    msgTxt = EmailMessage()
    msgTxt['Subject'] = '[' + config['EMAIL']['subject_prefix'] + '] Token Updated : '  + str(date.today())
    msgTxt['From'] = config['EMAIL']['sender']
    msgTxt['To'] = config['EMAIL']['recepient']
    local_str = 'Key will be expiring in ' + rweek + ' weeks.'
    if config['EMAIL']['send_newkey'] == '1' and config['EMAIL']['send_oldkey'] == '1':
        compiler = ('Hello,', config['EMAIL']['custom_message'], 'Old token: ' + str(token), 'New token: ' + str(ntoken), local_str)
    elif config['EMAIL']['send_newkey'] == '0' and config['EMAIL']['send_oldkey'] == '1':
        compiler = ('Hello,', config['EMAIL']['custom_message'], 'Old token: ' + str(token), local_str)
    elif config['EMAIL']['send_newkey'] == '1' and config['EMAIL']['send_oldkey'] == '0':
        compiler = ('Hello,', config['EMAIL']['custom_message'], 'New token: ' + str(ntoken), local_str)
    else:
        compiler = ('Hello,', config['EMAIL']['custom_message'], local_str)
    data = "\n".join(compiler)
    msgTxt.set_payload(data)

    try:
        smtp = smtplib.SMTP('localhost')
        smtp.send_message(msgTxt)
        smtp.quit()
    except:
        print('Failed sending email')

if __name__ == "__main__":
    main()
