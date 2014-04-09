'''
Created on Apr 9, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from QueryTermBFSLinker import *

import sys
if 2 != len(sys.argv):
    print "1para conf:"
    QueryTermBFSLinkerC().ShowConf()
    sys.exit()
    
QueryTermBFSLinkerUnitRun(sys.argv[1])
print "finished"
    
