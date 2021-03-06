'''
Created on Apr 21, 2014
get the list of edges appear in QExpTerm's PRA features
and the cnt

------
need to treat cotype edge and direct edge differently
but extract them the same?
------
whether is an edge feature (PRA) is depend on the json loads' type
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
import json
import pickle
import sys

'''
read exp term
for each feature:
    if is PRA feature
        for each edge
            if not stopedge
                add to dict
'''





hStopEdge = set(['search','desp','name','values'])

if 3 != len(sys.argv):
    print "2 para: q expterm with PRA feature + output edge pickle dict name"
    sys.exit()
    

hEdge = {}

cnt = 0
for line in open(sys.argv[1]):
    ExpTerm = ExpTermC(line.strip())
    cnt += 1
    if 0 == (cnt % 10000):
        print "process [%d] line" %(cnt)
    for feature in ExpTerm.hFeature:
        if not ExpTermC.IsPRAFeature(feature):
            continue
#         print "working on feature [%s]" %(feature)
        lEdge = SegEdgeFromPRAFeature(feature)
        for edge in lEdge:
            if edge in hStopEdge:
                continue
            if not edge in hEdge:                
                hEdge[edge] = 0
#             hEdge[edge] += 1
#             print "get edge [%s]" %(edge)
            

out = open(sys.argv[2],'w')
pickle.dump(hEdge,out)
out.close()
           
print "finished, [%d] edge" %(len(hEdge))
