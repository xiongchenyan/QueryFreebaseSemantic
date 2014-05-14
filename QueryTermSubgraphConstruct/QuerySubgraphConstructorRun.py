'''
Created on May 13, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from QueryTermSubgraphConstruct.QuerySubgraphConstructor import *
import sys
if 2 != len(sys.argv):
    print "1 para conf:"
    QuerySubgraphConstructorC().ShowConf()
    sys.exit()
    
QuerySubgraphConstructorUnitRun(sys.argv[1])
print "finished"
    

