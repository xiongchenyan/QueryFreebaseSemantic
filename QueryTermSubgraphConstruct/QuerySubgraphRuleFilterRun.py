'''
Created on May 15, 2014
run filter graph
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from QueryTermSubgraphConstruct.QuerySubgraphRuleFilter import QuerySubgraphRuleFilterC


import sys

if 2 != len(sys.argv[1]):
    print "1 conf"
    QuerySubgraphRuleFilterC.ShowConf()
    sys.exit()
    
Filter = QuerySubgraphRuleFilterC(sys.argv[1])
Filter.Process()

print "finished"
return True
