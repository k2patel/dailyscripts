#!/usr/bin/env python3
# Ketan Patel
# Small script to generate key and certificate for API based auth
# Set script run using cron monthly (managecert.py).
# Update configuration file and you are good to go.
# gencert.py - generate certificatre and key.
# submit.py - submit certificate to API for authorization.
# managecert.py - use generate certificate script to create script and if certificate is expire in two month renewcert.py used.
# License MIT

from OpenSSL import crypto
import os, socket
import sys
import configparser, argparse


def main():
    parser = argparse.ArgumentParser(prog='managecert', description='Certificate Generator.')
    parser.add_argument("--cfile", dest='cfile', help="configuration location", default='/etc/managecert.conf')
    args = parser.parse_args()

    # Read Configuration
    config = configparser.ConfigParser()
    config.read(args.cfile)

    # Set global variables.
    crt_country = config['DEFAULT']['country']
    crt_state = config['DEFAULT']['state']
    crt_location = config['DEFAULT']['location']
    crt_Oraganization = config['DEFAULT']['Organization']
    crt_ou = config['DEFAULT']['OU']
    cert_location = config['DEFAULT']['cert_location']
    key_location = config['DEFAULT']['key_location']
    cert_host = socket.getfqdn()

    keypath = os.path.join(key_location, str('smtp_' + cert_host+'.key'))
    crtpath = os.path.join(cert_location, str('smtp_' + cert_host+'.crt'))

    # Generate Key
    key = crypto.PKey()
    print("Generating Key For" + cert_host + "Please standby ")
    key.generate_key(crypto.TYPE_RSA, 4096)

    #Save key
    dumpkey(keypath, key)

    # Certificate for host
    cert = crypto.X509()
    cert.get_subject().CN = cert_host
    cert.get_subject().C = crt_country
    cert.get_subject().ST = crt_state
    cert.get_subject().L = crt_location
    cert.get_subject().O = crt_Oraganization
    cert.get_subject().OU = crt_ou
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha512")

    # Dump cert
    dumpcert(cert, crtpath)
    
    # Submit certificate
    submitcert()

def submitcert():
    os.system(os.path.join(os.getenv("PWD"), 'submit.py'))

def dumpkey(keypath, key):
    if os.path.exists(keypath):
        print("Certificate file exists, aborting.")
        print(keypath)
        sys.exit(1)
    else:
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()

def dumpcert(cert, crtpath):
    if os.path.exists(crtpath):
        print("Certificate File Exists, aborting.")
        print(crtpath)
    else:
        f = open(crtpath, "wb")
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        f.close()
        print("CRT Stored Here :" + crtpath)

if __name__ == "__main__":
    main()