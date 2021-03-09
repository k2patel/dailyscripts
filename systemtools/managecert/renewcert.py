#!/usr/bin/env python3
# Ketan Patel
# Small script to generate key and certificate for API based auth
# Update configuration file and you are good to go.
# gencert.py - generate certificatre and key
# renewcert.py - move old certificate with timestamp and create new one using gencert.
# submit.py - submit certificate to API for authorization
# managecert.py - use generate certificate script to create script and if certificate is expire in two month renewcert.py used.
# License MIT

from OpenSSL import crypto
import os, socket, datetime
import sys
import configparser, argparse

def main():
    parser = argparse.ArgumentParser(prog='managecert', description='Certificate Generator.')
    parser.add_argument("--cfile", dest='cfile', help="configuration location", default='/etc/managecert.conf')
    args = parser.parse_args()

    # Read Configuration
    config = configparser.ConfigParser()
    config.read(args.cfile)

    cert_location = config['DEFAULT']['cert_location']
    key_location = config['DEFAULT']['key_location']
    cert_host = socket.getfqdn()

    crtpath = os.path.join(cert_location, str('smtp_' + cert_host + '.crt'))
    keypath = os.path.join(key_location, str('smtp_' + cert_host + '.key'))
    oldcrtpath = os.path.join(cert_location, str('smtp_' + cert_host + '.crt' + datetime.datetime.now().strftime("%d-%m-%Y")))
    oldkeypath = os.path.join(key_location, str('smtp_' + cert_host + '.key' + datetime.datetime.now().strftime("%d-%m-%Y")))

    os.rename(crtpath, oldcrtpath)
    os.rename(keypath, oldkeypath)

    os.system(os.path.join(os.getenv("PWD"), 'gencert.py'))
    submitcert()

def submitcert():
    os.system(os.path.join(os.getenv("PWD"), 'submit.py'))

if __name__ == "__main__":
    main()