#!/usr/local/bin/python

import re, urllib
import os.path
import sys


def get_store(fn):
    tr = {}
    fh = open(fn, 'r')
    for line in fh:
        line = line.replace('^M', ' ')
        v = line.strip().split(": ", 1)                
        tr[v[0]] = v[1]    
    fh.close()
    return tr

def gen_wp(vals):
    site = 'http://ling.auf.net'
    pdfurl = vals['PDFURL']
    pdfurl.strip('"')
    pdfurl = site + pdfurl
    tm = re.search('''(\<table.*$)''', vals['HTML'], flags=re.IGNORECASE)
    if (tm == None):
        print "Can't find table in " + vals['HTML']
        sys.exit(-1)
    table = tm.group(1)
    s = ["<b><a href=\"" + pdfurl + "\">" + vals['TITLE'] + "</a></b>",
         vals['RAWAUTHORS'],
         "direct link: <a href=\"" + site + vals['URL'] + "\">" + site + vals['URL']+"</a>",
         vals['MONTH'] + " " + vals['YEAR'],
         vals['ABSTRACT'],
         table
         ]
    return "\n".join(s)

if __name__ == "__main__":
    for s in sys.argv[1:]:
        print s
        v = get_store(s)
        s = gen_wp(v)
        print s
