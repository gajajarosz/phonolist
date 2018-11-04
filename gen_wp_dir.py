#!/usr/local/bin/python

import re, urllib
import os.path
import sys
import glob
from gen_wp import get_store, gen_wp

def check_all(indir, newdir):
    wp = set(glob.glob(indir + "/*.wp"))
    nonwp = set(glob.glob(indir + "/*[0-9]"))
    miss = 0
    found = 0
    for nw in nonwp:
        if (nw + ".wp" in wp):
            found += 1
        else:
            print "couldn't find " + nw
            miss += 1
            v = get_store(nw)            
            s = gen_wp(v)
            pwp = nw + ".wp"
            tmp = newdir + "/" + os.path.basename(pwp) 
            fh = open(pwp, "w")
            fh.write(s)
            fh.close()
            fh = open(tmp, "w")
            fh.write(s)
            fh.close()
    print "Found " + str(found) + " old entries; " + str(miss) + " new entries"
    
    
if __name__ == "__main__":
    indir = sys.argv[1]
    newdir = sys.argv[2]
    check_all(indir, newdir)
