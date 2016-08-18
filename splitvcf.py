#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'Alessio Bianchi'
__email__ = "me@alessiobianchi.eu"
__license__ = 'Apache License Version 2.0'
__copyright__ = 'Copyright 2016 Alessio Bianchi'

program_description = """splitvcf v%(version)s
%(copyright)s (%(email)s)
Licensed under %(license)s

Splits a VCF file containing multiple contacts into
individual VCF files and removes features not compatible
with VCF 2.1.
""" % {
    'version': __version__,
    'copyright': __copyright__,
    'email': __email__,
    'license': __license__
}

import sys
import re

def phone(l):
    l = l.replace("type=", "")
    l = l.replace(";pref", "")
    l = l.replace(";IPHONE", "")
    if l.startswith("TEL:"):
        l = l.replace("TEL:", "")
        l = "TEL;MAIN:%s" % (l)
    l = re.sub(r'[^a-zA-Z0-9:;\+]', '', l)  # strip spaces
    return l

if len(sys.argv) != 2:
    sys.stderr.write("%s\nusage: %s <vfc file to split>\n" % (program_description, sys.argv[0]))
    sys.exit(1)

with open(sys.argv[1]) as f:
    content = f.readlines()
    i = 0;
    o = None
    
    for ll in content:
        l = ll.strip()
        if l == "BEGIN:VCARD":
            i = i + 1
            print "processing contact #%d" % (i)
            o = open("contact%d.vcf" % (i), "w")
            o.write(l)
            o.write("\n")
        elif l == "END:VCARD":
            o.write(l)
            o.write("\n")
            o.close()
        elif l.startswith("VERSION"):
            o.write("VERSION:2.1")
            o.write("\n")
        elif l.startswith("N:"):
            l = re.sub(r'[^a-zA-Z0-9 :;]', '', l) # strips emoji and such
            o.write(l)
            o.write("\n")
        elif l.startswith("TEL"):
            l = phone(l)
            o.write(l)
            o.write("\n")
