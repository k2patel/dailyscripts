# Makefile for mod_k2patel (gmake)
APXS=$(shell which apxs || which apxs2)

default: mod_k2patel.so
        @echo make done
        @echo type \"make install\" to install mod_k2patel

mod_k2patel.so: mod_k2patel.c
        $(APXS) -c -n $@ mod_k2patel.c mod_k2patel_cfg.c mod_k2patel_session.c mod_k2patel_ssl.c mod_k2patel_http.c mod_k2patel_json.c

mod_k2patel.c:

install: mod_k2patel.so
        $(APXS) -i -S LIBEXECDIR=$(DESTDIR)$$($(APXS) -q LIBEXECDIR)/ -n mod_k2patel.so mod_k2patel.la

clean:
        rm -rf *~ *.o *.so *.lo *.la *.slo *.loT .libs/
