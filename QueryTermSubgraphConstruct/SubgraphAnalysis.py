'''
Created on May 15, 2014
input: a directory of graphs
output: for now, the #of node, # of edge, # of edge type, top 5 edge category, in a file
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from GraphBase.base import *
from FreebaseDump.FbDumpBasic import GetDomain
from cxBase.WalkDirectory import WalkDir


import sys


def SegQid(FName):
    vCol = FName.split('_')
    return vCol[len(vCol)-1]

def CntDomainFromEdge(hEdge):
    hDomain = {}
    for item in hEdge:
        domain = GetDomain(item)
        if not domain in hDomain:
            hDomain[domain] = 1
        else:
            hDomain[domain] += 1
    return hDomain
            

if 3!= len(sys.argv):
    print "2 para: subgraph directory + output"
    sys.exit()
    

lFName = WalkDir(sys.argv[1])
out = open(sys.argv[2],'w')

for FName in lFName:
    qid = SegQid(FName)
    Graph = GraphC()
    Graph.ReadFromSimpleEdgeFile(FName)
    NodeCnt = Graph.GetNumOfNode()
    EdgeCnt = Graph.GetNumOfEdge()
    hEdge = Graph.GetEdgeCnt()
    hDomain = CntDomainFromEdge(hEdge)
    lDomain = hDomain.items()
    lDomain.sort(key=lambda item: item[1], reverse = True)
    
    ResStr = "%s\t%d\t%d" %(qid,NodeCnt,EdgeCnt)
    for domain,cnt in lDomain[:5]:
        ResStr +="\t%s_%d" %(domain,cnt)
    print >>out, ResStr
    
out.close()
