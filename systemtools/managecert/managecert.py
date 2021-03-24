#!/usr/bin/env python3
# Ketan Patel
# Small script to generate key and certificate for API based auth
# Set script run using cron monthly (managecert.py).
# Update configuration file and you are good to go.
# License MIT

from datetime import datetime
from OpenSSL import crypto as c
import configparser, argparse, os, socket, requests, sys, codecs

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
            renewcert(config)
        else:
            print('Certificate still valid')
    else:
        print('generating certificate')
        gencert(config)

def gencert(config):
    # Set variables.
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
    key = c.PKey()
    print("Generating Key For" + cert_host + "Please standby ")
    key.generate_key(c.TYPE_RSA, 4096)

    #Save key
    dumpkey(keypath, key)

    # Certificate for host
    cert = c.X509()
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
    submit(config)


def dumpkey(keypath, key):
    if os.path.exists(keypath):
        print("Certificate file exists, aborting.")
        print(keypath)
        sys.exit(1)
    else:
        f = open(keypath, "wb")
        f.write(c.dump_privatekey(c.FILETYPE_PEM, key))
        f.close()

def dumpcert(cert, crtpath):
    if os.path.exists(crtpath):
        print("Certificate File Exists, aborting.")
        print(crtpath)
    else:
        f = open(crtpath, "wb")
        f.write(c.dump_certificate(c.FILETYPE_PEM, cert))
        f.close()
        print("CRT Stored Here :" + crtpath)

def renewcert(config):
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
    submit(config)

def submit(config):

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
