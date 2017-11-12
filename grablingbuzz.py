#!/usr/local/bin/python

import re, urllib
import os.path
import sys


maxtoget = 100
localstore="lingbuzz"

def processlingbuzz(parturl):
    # we need to find: 
    # title of paper
    # authors (last names only?)
    # date (year only?)
    # html content
    base = "http://ling.auf.net"
    url = "http://ling.auf.net" + parturl
    id = parturl.replace("/", "_")
    id = id.replace("?", "_")
    outfn = "%s/%s" % (localstore, id)
    print "storing data in " + outfn
    if os.path.isfile(outfn):
        print outfn + " already exists"
        return True
    else:
        f = urllib.urlopen(url)
        str = '';
        for s in f.read():
            str += s
        str = str.replace("\n", ' ')
        str = str.replace('\r', ' ')
#        str = str.replace("^M", ' ')
        str = str.replace('href="/lingbuzz', 'href="'+base+'/lingbuzz')
        m = re.search('''<center>(.*?<a href="?([^\>]+?)"?>([^\<]+)</a>.*?<br/>(.*?)<br/>([A-Za-z]+) +([0-9]+).*?</p>(.*)<table.*)<tr><td>Downloaded:''', str, flags=re.IGNORECASE)
        if (m == None):
            print "CANNOT parse str for " + url + ": " + str
            sys.exit(-1)
        text = m.group(1)
        pdfurl = m.group(2)
        title = m.group(3)
        rawauthors = m.group(4)
        rawauthors = m.group(4)
        month = m.group(5)
        year = m.group(6)
        abstract = m.group(7)
        authors = []
        lastnames = []
        for a in re.findall('''>([^<>]+)</a>''', rawauthors, re.I):
            authors.append(a)
            am = re.search('''((((V[oa]n)|(De)) )?[^ ]+)\s*$''', a, re.I)
            if (am != None):
                lastnames.append(am.group(1))
        authortitle = ", ".join(lastnames)
        if (len(lastnames) == 2):
            authortitle = " & ".join(lastnames)        
        elif (len(lastnames) > 2):
            authortitle = ", ".join(lastnames[0:-1]) + " & " + lastnames[-1]
        authortitle += " (" + year + ")"

        of = open(outfn, 'w')        
        of.write("ID: lingbuzz_" + id + "\n")
        of.write("URL: " + url + "\n")
        of.write("PDFURL: " + pdfurl + "\n")
        of.write("HEADER: " + authortitle + " - " + title + "\n")
        of.write("TITLE: " + title + "\n")
        of.write("AUTHORTITLE: " + authortitle + "\n")
        of.write("RAWAUTHORS: " + rawauthors + "\n")
        of.write("AUTHORS: " + ", ".join(authors) + "\n")
        of.write("LASTNAMES: " + ", ".join(lastnames) + "\n")        
        of.write("MONTH: " + month + "\n")
        of.write("YEAR: " + year + "\n")
        of.write("ABSTRACT: " + abstract + "\n")
        of.write("HTML: " + text + "\n")        
        of.close()
    return False

def fetchlingbuzz():
    baseurl="http://ling.auf.net/lingbuzz/phonology?start="
    counter = 0
    bad = 0
    print "looking to get " + str(maxtoget) + " docs"
    while ((bad == 0) and (counter < maxtoget)):
        url = baseurl+str(counter+1)
        print "fetching from " + url
        pcounter = counter
        for i in re.findall('''\[pdf\]</a></td><td><a href=["'](.[^"']+)["']''', urllib.urlopen(url).read(), re.I):
            if (counter < maxtoget):
                alreadydone = processlingbuzz(i)
                if (alreadydone):
                    return counter
                counter += 1
        if (pcounter == counter):
        # if we didn't find anything on the last page, stop looking
            bad = 1
    return counter

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        maxtoget = int(sys.argv[1])
    fetchlingbuzz()
