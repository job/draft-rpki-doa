# draft-spaghetti-sidrops-rpki-doa

RPKI Discard Origin Authorization. A mechanism to confirm whether a resource
holder authorized a specific tuple of (peer AS, origin AS, prefix, prefixlength
and BGP community) to signal a request to discard traffic.

Work in progress repository for Internet-Draft draft-spaghetti-sidrops-rpki-doa

## Usage

### Draft documents

The source files for the Internet-Draft documents are:

- `draft-spaghetti-sidrops-rpki-doa.xml`
- `RpkiDiscardOriginAuthorization-2021.asn`

To regenerate the text and HTML versions after making changes, run:

``` sh
make drafts
```

### Object prototyping

An [rpkimancer](https://github.com/benmaddison/rpkimancer/) plug-in is also
available, providing the ability to read and write example DOA objects.

To install (in the root of your checkout):

``` sh
python3 -m pip install rpkimancer-doa
```

Object creation and inspection is provided by the `rpkincant` CLI tool.

See `rpkincant --help` for usage information.

After making changes to the ASN.1 module source, execute `make asn1` to update
the patched version in python distribution tree.

To setup a development environment with the required test dependencies:

``` sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r packaging/requirements-dev.txt
```
