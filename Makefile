#
# Makefile for I-D's and RFCs
# $Id: Makefile,v 1.1.1.1 2002-11-11 05:11:48 randy Exp $
#

# Your nroff document is called foo.txt. Change below as appropiate.
NAME=draft-spaghetti-sidrops-rpki-doa
MOD=RpkiDiscardOriginAuthorization-2021

.PHONY: all
all: drafts asn1

.PHONY: drafts
drafts: $(NAME).txt

$(NAME).txt: $(NAME).xml
	xml2rfc $(NAME).xml --html --text --expand

.PHONY: asn1
asn1: rpkimancer_doa/asn1/$(MOD).asn

rpkimancer_doa/asn1/$(MOD).asn: $(MOD).asn $(MOD).patch
	patch $(MOD).asn $(MOD).patch -o $@

clean:
	rm -f *.html *.txt rpkimancer_doa/asn1/$(MOD).asn
