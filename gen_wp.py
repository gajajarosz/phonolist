#!/usr/local/bin/python

import re, urllib
import os.path
import sys


def get_store(fn):
    tr = {}
    fh = open(fn, 'r')
    for line in fh:
        line = line.replace(r'\r', ' ')
        v = line.strip().split(": ", 1)
        if len(v)>1: tr[v[0]] = v[1]
        else: 
            v[0]=v[0].replace(r':','')
            tr[v[0]] = ""
    #print tr
    fh.close()
    return tr

def gen_wp(vals):
    site = 'http://ling.auf.net'
    tm = re.search('''(\<table.*$)''', vals['HTML'], flags=re.IGNORECASE)
    if (tm == None):
        print "Can't find table in " + vals['HTML']
        sys.exit(-1)
    table = tm.group(1)
    s = [vals['AUTHORTITLE'] + " - " + vals['TITLE'],
         "",
         "<b><a href=\"" + vals['PDFURL'] + "\">" + vals['TITLE'] + "</a></b>",
         vals['RAWAUTHORS'],
         "direct link: <a href=\"" + vals['URL'] + "\">" + vals['URL'] + "</a>",
         vals['MONTH'] + " " + vals['YEAR'],
         vals['ABSTRACT'],
         table,
         "\n\n"
         ]
    return "\n".join(s)

if __name__ == "__main__":
    for s in sys.argv[1:]:
        print s
        v = get_store(s)
        s = gen_wp(v)
        print s
