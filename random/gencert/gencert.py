#!/usr/bin/env python3
# Ketan Patel
# Small script to generate self signed certificat for hostlist.
# List all the hosts and related value saperated by pipe.
# Update configuration file and you are good to go.
# It generates folder for each system you are generating certificate for.
# License MIT

#!/usr/bin/python
from OpenSSL import crypto
import os
import sys
import configparser, argparse


def main():
    parser = argparse.ArgumentParser(prog='gencert', description='Certificate Generator.')
    parser.add_argument("--sfile", dest='sfile', help="list of system list", default='systems')
    args = parser.parse_args()

    # Read Configuration
    HOME = os.getenv("PWD")
    config = configparser.ConfigParser()
    config.read(os.path.join(HOME, 'gencert.conf'))

    # Set global variables.
    cert_country = config['DEFAULT']['country']
    cert_state = config['DEFAULT']['state']
    cert_location = config['DEFAULT']['location']
    cert_Oraganization = config['DEFAULT']['Organization']
    cert_ou = config['DEFAULT']['OU']
    search = eval(config.get("DEFAULT", "search"), {}, {})

    #Pull these out of scope
    with open(args.sfile, "r") as file:
        for line in file:
                parts = line.split('|')
                if any(item in line for item in search):
                    if str(config['DATA']['domainpresent']) == 'False':
                        cert_host = str(parts[0]+str(config['DATA']['domain']))
                    else:
                        cert_host = str(parts[0])
                    cert_home = os.path.join(HOME, cert_host)
                    os.system('mkdir {}'.format(cert_home))
                    keypath = os.path.join(cert_home, str(cert_host+'.key'))
                    csrpath = os.path.join(cert_home, str(cert_host+'.csr'))
                    crtpath = os.path.join(cert_home, str(cert_host+'.crt'))

                    # Request for host
                    key = crypto.PKey()
                    print("Generating Key For" + cert_host + "Please standby ")
                    key.generate_key(crypto.TYPE_RSA, 4096)

                    #Save key
                    dumpkey(keypath, key)

                    req = crypto.X509Req()
                    req.get_subject().CN = cert_host
                    req.get_subject().C = cert_country
                    req.get_subject().ST = cert_state
                    req.get_subject().L = cert_location
                    req.get_subject().O = cert_Oraganization
                    req.get_subject().OU = cert_ou
                    req.set_pubkey(key)
                    req.sign(key, "sha512")

                    # Dump csr
                    dumpcsr(req, csrpath)

                    # Certificate for host
                    cert = crypto.X509()
                    cert.get_subject().CN = cert_host
                    cert.get_subject().C = cert_country
                    cert.get_subject().ST = cert_state
                    cert.get_subject().L = cert_location
                    cert.get_subject().O = cert_Oraganization
                    cert.get_subject().OU = cert_ou
                    cert.set_serial_number(1000)
                    cert.gmtime_adj_notBefore(0)
                    cert.gmtime_adj_notAfter(31536000)
                    cert.set_issuer(cert.get_subject())
                    cert.set_pubkey(key)
                    cert.sign(key, "sha512")

                    # Dump cert
                    dumpcert(cert, crtpath)


def dumpkey(keypath, key):
    if os.path.exists(keypath):
        print("Certificate file exists, aborting.")
        print(keypath)
        sys.exit(1)
    else:
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()

def dumpcsr(req, csrpath):
    if os.path.exists(csrpath):
        print("Sign Request File Exists, aborting.")
        print(csrpath)
    else:
        f = open(csrpath, "wb")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()
        print("Success")

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
