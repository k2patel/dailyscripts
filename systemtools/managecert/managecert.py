#!/usr/bin/env python3
# Ketan Patel
# Small script to generate key and certificate for API based auth
# Set script run using cron monthly (managecert.py).
# Update configuration file and you are good to go.
# gencert.py - generate certificatre and key.
# submit.py - submit certificate to API for authorization.
# managecert.py - use generate certificate script to create script and if certificate is expire in two month renewcert.py used.
# License MIT

from datetime import datetime
from OpenSSL import crypto as c
import configparser, argparse, os, socket

def main():
    parser = argparse.ArgumentParser(prog='managecert', description='Certificate Generator.')
    parser.add_argument("--cfile", dest='cfile', help="configuration location", default='/etc/managecert.conf')
    args = parser.parse_args()

    # Read Configuration
    config = configparser.ConfigParser()
    config.read(args.cfile)

    cert_location = config['DEFAULT']['cert_location']
    cert_host = socket.getfqdn()
    crtpath = os.path.join(cert_location, str('smtp_' + cert_host+'.crt'))

    if os.path.isfile(crtpath): 
        with open(crtpath, 'rb') as f:
            cert_buf = f.read()
            
        cert = c.load_certificate(c.FILETYPE_PEM, cert_buf)
        date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
        not_after = datetime.strptime(cert.get_notAfter().decode(encoding), date_format)
        now = datetime.now()
        r = not_after.month - now.month + 12*(not_after.year - now.year)
        if r < 2:
            print('renewing certificate')
            os.system(os.path.join(os.getenv("PWD"), 'renewcert.py'))
        else:
            print('Certificate still valid')
    else:
        print('generating certificate')
        os.system(os.path.join(os.getenv("PWD"), 'gencert.py'))


if __name__ == "__main__":
    main()