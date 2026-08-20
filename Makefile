NAME=draft-spaghetti-grow-rpki-doa
MOD=RpkiDiscardOriginAuthorization-2021

.PHONY: all
all: drafts asn1

.PHONY: drafts
drafts: $(NAME).txt

$(NAME).txt: $(NAME).xml
	xml2rfc $(NAME).xml --html --text --expand --allow-local-file-access

.PHONY: asn1
asn1: rpkimancer_doa/asn1/$(MOD).asn

rpkimancer_doa/asn1/$(MOD).asn: $(MOD).asn $(MOD).patch
	patch $(MOD).asn $(MOD).patch -o $@

clean:
	rm -f *.html *.txt rpkimancer_doa/asn1/$(MOD).asn

www:
	cp -v $(NAME).{exp.xml,txt,html} ~/Downloads/
