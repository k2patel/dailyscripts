Let's Encrypt
============

How this script work:

Create configuration file in /etc/letsencrypt/conf folder for each of your domain.

configuration sample is provided in cert.conf.

in your nginx vhost configuration define following.

<pre><code>
    location /.well-known/acme-challenge {
        root /var/www/letsencrypt;
    }
</code></pre>

Above setting must be defined in HTTP section, at it will not work in HTTPS.