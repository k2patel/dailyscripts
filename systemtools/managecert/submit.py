#!/usr/bin/env python3
# Ketan Patel
# Small script to generate key and certificate for API based auth
# Set script run using cron monthly (managecert.py).
# Update configuration file and you are good to go.
# gencert.py - generate certificatre and key
# submit.py - submit certificate to API for authorization
# managecert.py - use generate certificate script to create script and if certificate is expire in two month renewcert.py used.
# License MIT

import codecs
import os, socket, requests
import configparser, argparse

def main():
    parser = argparse.ArgumentParser(prog='managecert', description='Certificate Generator.')
    parser.add_argument("--cfile", dest='cfile', help="configuration location", default='/etc/managecert.conf')
    args = parser.parse_args()

    # Read Configuration
    config = configparser.ConfigParser()
    config.read(args.cfile)

    cert_host = socket.getfqdn()
    cert_location = config['DEFAULT']['cert_location']
    endpoint = config['DEFAULT']['endpoint']

    crtpath = os.path.join(cert_location, str('smtp_' + cert_host+'.crt'))

    tmpfile = open(crtpath, 'r')
    text = tmpfile.read()
    tmpfile.close()
    data = codecs.encode(bytes(text, 'utf8'), 'base64').decode("utf-8").replace('\n', ' ').rstrip()

    payload = {'cert': data}
    headers = {
        'userID': config['DEFAULT']['apiUser'],
        'apiToken': config['DEFAULT']['apiToken'],
        'accept': 'application/json'
    }
    response = requests.post(endpoint, data=payload, headers=headers)
    
    print('Response Code: ' + str(response.status_code))
    print(response.json())

if __name__ == "__main__":
    main()