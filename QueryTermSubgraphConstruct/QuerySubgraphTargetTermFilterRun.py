'''
Created on May 14, 2014
run
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

import sys
from cxBase.base import cxConf
from QueryTermSubgraphConstruct.QuerySubgraphTargetTermFilter import QuerySubgraphTargetTermFilterC


if 2 !=len(sys.argv):
    print "conf:"
    QuerySubgraphTargetTermFilterC.ShowConf()
    print "in"
    sys.exit()
    
conf = cxConf(sys.argv[1])
InName = conf.GetConf('in')
Filter = QuerySubgraphTargetTermFilterC(sys.argv[1])
Filter.Process(InName)
print "finished"
