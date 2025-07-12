# OPENSMT + DKIM + IMAP + PF + ACME-CLIENT +  HTTPD + RAINLOOP + PHP-FPM

This is simple openSMTP Based mail server for personal use.
 - Make sure to replace `<DOMAIN>` with your actual domain name.
 - Install following packages
	 - acme-client / certbot
	 - dkimproxy
	 - dovecot
	 - dovecot-pigeonhole
	 - opensmtpd-table-passwd
	 - php
	 - femail # Optional

## OPENSMTP
### Credentials `/etc/mail/credential`
This files content the user, authentication and location for the mail.
Example format.
here is simple script to manage users / password
```
#!/bin/ksh

if [ ${#} -ne 2 ]
then
	echo "Usage: $0 <username> <password>"
	exit 1
fi
DOMAIN=example.com
echo "${1}@$DOMAIN:$(smtpctl encrypt ${2}):vmail:2000:2000:/var/vmail/$DOMAIN/${1}::userdb_mail=maildir:/var/vmail/$DOMAIN/${1}" | doas tee -a /etc/mail/credentials
```

### /etc/mail/smtpd.conf
```
#	$OpenBSD: smtpd.conf,v 1.14 2019/11/26 20:14:38 gilles Exp $

# This is the smtpd server system-wide configuration file.
# See smtpd.conf(5) for more information.

# SSL
pki mail.<DOMAIN> key "/etc/ssl/private/mail.<DOMAIN>.key"
pki mail.<DOMAIN> cert "/etc/ssl/mail.<DOMAIN>.fullchain.pem"

# Local user database
table aliases file:/etc/mail/aliases
table virtuals file:/etc/mail/virtuals
table credentials passwd:/etc/mail/credentials

# Define actions on storing
action "inbound" maildir "/var/vmail/<DOMAIN>/%{dest.user:lowercase}" virtual <virtuals>
action "local" mbox alias <aliases>

# out going
action "relay" relay helo mail.<DOMAIN>
action "relay_dkim" relay host smtp://127.0.0.1:10027

# Stored compressed.
queue compression

# Encrypt queue files with EVP_aes_256_gcm(3).
# (generate a key with 'openssl rand -hex 16')
queue encryption <RANDOM_STRING>

# Set maximum message size.
smtp max-message-size 35M

#accept for local alias <aliases> deliver to maildir
#accept for any for domain <vdomains> virtual <vusers> deliver to maildir
#accept for local for any relay

# To accept external mail, replace with: listen on all
#
listen on all hostname mail.<DOMAIN> tls-require pki mail.<DOMAIN>
listen on all port submission hostname mail.<DOMAIN> tls-require pki mail.<DOMAIN> auth <credentials>
listen on lo0 port 10028 tag DKIM

#  action "local" maildir "%{user.directory}/.mail" alias <aliases>

# <domain>
match from any for domain "<DOMAIN>" action "inbound"
# local
match from local for local action "local"

# dkim
match tag DKIM for any action "relay"
##match auth from any for any action "relay"
match auth from any for any action "relay_dkim"
```

### /etc/mail/spamd.conf
```
# $OpenBSD: spamd.conf,v 1.9 2018/07/22 17:09:43 jmc Exp $
#
# spamd(8) configuration file, read by spamd-setup(8).
# See also spamd.conf(5).
#
# Configures lists for spamd(8).
#
# Strings follow getcap(3) convention escapes, except you
# can have a bare colon (:) inside a quoted string and it
# will deal with it. See spamd-setup(8) for more details.
#
# "all" must be here, and defines the order in which lists are applied.
# Lists specified with the :white: capability apply to the previous
# list with a :black: capability.
#
# As of June 2016, a place to search for blacklists is
#     http://en.wikipedia.org/wiki/Comparison_of_DNS_blacklists
# - most of these are DNS-based only and cannot be used with spamd(8),
# but some of the lists also provide access to text files via rsync.

all:\
	:nixspam:

# Nixspam recent sources list.
# Mirrored from http://www.heise.de/ix/nixspam
nixspam:\
	:black:\
	:msg="Your address %A is in the nixspam list\n\
	See http://www.heise.de/ix/nixspam/dnsbl_en/ for details":\
	:method=https:\
	:file=www.openbsd.org/spamd/nixspam.gz

# An example of a list containing addresses which should not talk to spamd.
#
#override:\
#	:white:\
#	:method=file:\
#	:file=/var/db/override.txt:
```

### Virtual Mail `/etc/mail/virtual`
```
email@domain.com: vmail
```

### Allow IP of known Sender for fast Delivery
use `nospamd` file which list all the whiltelist IP for PF


## DKIM
### `/etc/dkimproxy_in.conf`
```
# specify what address/port DKIMproxy should listen on
listen    127.0.0.1:10025

# specify what address/port DKIMproxy forwards mail to
relay     127.0.0.1:10026
```
### `/etc/dkimproxy_out.conf`
```
# specify what address/port DKIMproxy should listen on
listen    127.0.0.1:10025

# specify what address/port DKIMproxy forwards mail to
relay     127.0.0.1:10026
bsd# cat dkimproxy_out.conf                                                                                                                                                         
# specify what address/port DKIMproxy should listen on
listen    127.0.0.1:10027

# specify what address/port DKIMproxy forwards mail to
relay     127.0.0.1:10028

# specify what domains DKIMproxy can sign for (comma-separated, no spaces)
domain    <DOMAIN>,mail.<DOMAIN>

# specify what signatures to add
signature dkim(c=relaxed)
signature domainkeys(c=nofws)

# specify location of the private key
keyfile   /etc/mail/private.key

# specify the selector (i.e. the name of the key record put in DNS)
selector  <DOMAIN>

# control how many processes DKIMproxy uses
#  - more information on these options (and others) can be found by
#    running `perldoc Net::Server::PreFork'.
#min_servers 5
#min_spare_servers 2
```

### DNS Record
`_dmarc	TXT	v=DMARC1;p=reject;sp=reject;pct=100;adkim=s;aspf=r;rua=mailto:user@<DOMAIN>;fo=1`

`<DOMAIN>	TXT	v=spf1 ip4:<MAIL_SERVER_IPv4> ip6:<MAIL_SERVER_IPv6> include:<DOMAIN> include:mail.<DOMAIN> include:<OTHER RECORD> ~all`

`<DOMAIN>._domainkey	TXT	v=DKIM1;t=s;p=<YOUR KEY>`

`mail.<DOMAIN>	MX	<MAIL_SERVER_IPv4>`

## IMAP
### `/etc/dovecot/dovecot.conf`
Make sure you have this block, if not add
```
# A config file can also tried to be included without giving an error if
# it's not found:
!include_try local.conf
```
### `/etc/dovecot/local.conf`
```
# ----- TRANSPORT LAYER SECURITY (TLS) -----

# TLS is always required, otherwise will cause an authentication failure.
ssl = required

# Define mail server's TLS key and certificate.
ssl_cert = </etc/ssl/mail.<DOMAIN>.fullchain.pem
ssl_key = </etc/ssl/private/mail.<DOMAIN>.key

ssl_dh = </etc/ssl/dovecot/dh.pem
ssl_prefer_server_ciphers = yes

# ----- AUTHENTICATION -----

# Define auth mechanism.
# Since the mail server uses TLS,
# don't need to bother worrying about anything else than the PLAIN mechanism.
auth_mechanisms = plain

# Define username database from credentials file.
userdb {
  args = username_format=%u /etc/mail/credentials
  driver = passwd-file
  name =
}

# Define password database from credentials file.
passdb {
  args = scheme=CRYPT username_format=%u /etc/mail/credentials
  driver = passwd-file
  name =
}

# ----- MAIL -----

# Define uid and gid of the user Virtual Mail Account.
first_valid_uid = 2000
first_valid_gid = 2000

# Define location of mailboxes.
mail_location = maildir:/var/vmail/%d/%n

# Define mailboxes.
namespace inbox {
  inbox = yes
  location =
  mailbox Archive {
  auto = subscribe
  special_use = \Archive
  }
  mailbox Drafts {
  auto = subscribe
  special_use = \Drafts
  }
  mailbox Junk {
  auto = subscribe
  special_use = \Junk
  }
  mailbox Sent {
  auto = subscribe
  special_use = \Sent
  }
  mailbox Trash {
  auto = subscribe
  special_use = \Trash
  }
  prefix =
}

protocols = imap sieve

protocol imap {
  mail_plugins = " imap_sieve"
}

mail_plugin_dir = /usr/local/lib/dovecot

managesieve_notify_capability = mailto

managesieve_sieve_capability = fileinto reject envelope encoded-character vacation subaddress comparator-i;ascii-numeric relational regex imap4flags copy include variables body enotify environment mailbox date index ihave duplicate mime foreverypart extracttext imapsieve vnd.dovecot.imapsieve

plugin {
  imapsieve_mailbox1_before = file:/usr/local/lib/dovecot/sieve/report-spam.sieve
  imapsieve_mailbox1_causes = COPY
  imapsieve_mailbox1_name = Junk
  imapsieve_mailbox2_before = file:/usr/local/lib/dovecot/sieve/report-ham.sieve
  imapsieve_mailbox2_causes = COPY
  imapsieve_mailbox2_from = Junk
  imapsieve_mailbox2_name = *
  sieve = file:~/sieve;active=~/.dovecot.sieve
  sieve_global_extensions = +vnd.dovecot.pipe +vnd.dovecot.environment
  sieve_pipe_bin_dir = /usr/local/lib/dovecot/sieve
  sieve_plugins = sieve_imapsieve sieve_extprograms
}

service imap-login {
  inet_listener imap {
  port = 0
  }
}

service managesieve-login {
  inet_listener sieve {
  port = 4190
  }
  inet_listener sieve_deprecated {
  port = 2000
  }
}
```
## PF
### `/etc/pf.conf`
Add following code to your PF
```
table <spamd-white> persist
table <nospamd> persist file "/etc/mail/nospamd"

set skip on lo

block return	# block stateless traffic
pass		# establish keep-state

pass in on egress proto tcp to any port smtp \
    divert-to 127.0.0.1 port spamd
pass in on egress proto tcp from <nospamd> to any port smtp
pass in log on egress proto tcp from <spamd-white> to any port smtp
pass out log on egress proto tcp to any port smtp
```
## CertBot / Acme Client
### `/etc/acme-client.conf`
Add your domain to get it registered.
```
domain mail.<DOMAIN> {
	domain key "/etc/ssl/private/mail.<DOMAIN>.key"
	domain full chain certificate "/etc/ssl/mail.<DOMAIN>.fullchain.pem"
	sign with letsencrypt
}
```
### `Cron Job`
```
~	0	*	*	*  acme-client mail.<DOMAIN> && rcctl reload httpd && rcctl reload dovecot && rcctl restart smtpd
```

## HTTPD
### `/etc/httpd.conf`
```
server "mail.<DOMAIN>" {
    listen on egress port 80
    # The next five lines are what you need for acme-client:
    location "/.well-known/acme-challenge/*" {
        root "/acme"
        request strip 2
        directory no auto index
    }
    location * {
        block return 301 "https://$HTTP_HOST$REQUEST_URI"
    }
}

server "mail.<DOMAIN>" {
    listen on egress tls port 443
    hsts
    gzip-static
    tls {
       certificate "/etc/ssl/mail.<DOMAIN>.fullchain.pem"
       key "/etc/ssl/private/mail.<DOMAIN>.key"
    }
    root "/htdocs/rainloop"
    directory index "index.php"
    tcp { nodelay, backlog 10}
    hsts {
          max-age 31556952
          preload
    }
    connection max request body 26214400
    location "/data*" {
          block return 403
    }
    location "*/.git*" {
          block return 403
    }
    # The next five lines are for acme-client:
    location "/.well-known/acme-challenge/*" {
        root "/acme"
        request strip 2
        directory no auto index
    }
    location "*.php*" {
        fastcgi socket "/run/php-fpm.sock"
        # root "/htdocs/rainloop"
        root "/htdocs/rainloop"
    }
    log access "rainloop_access.log"
    log error "rainloop_error.log"
}
```
## RAINLOOP
### `/var/www/htdocs/rainloop`
In this folder, create if doesn't exists extract the rainloop
#### index.php
```
<?php

if (!defined('APP_VERSION'))
{
	define('APP_VERSION', '1.17.0');
	define('APP_INDEX_ROOT_FILE', __FILE__);
	define('APP_INDEX_ROOT_PATH', str_replace('\\', '/', rtrim(dirname(__FILE__), '\\/').'/'));
}

if (file_exists(APP_INDEX_ROOT_PATH.'rainloop/v/'.APP_VERSION.'/include.php'))
{
	include APP_INDEX_ROOT_PATH.'rainloop/v/'.APP_VERSION.'/include.php';
}
else
{
	echo '[105] Missing version directory';
	exit(105);
}
```
Create folder structure matching this pattern, if does not exists.
`/var/www/htdocs/rainloop/rainloop/v/1.17.0`


Make sure to start most installed services using `rcctl`

