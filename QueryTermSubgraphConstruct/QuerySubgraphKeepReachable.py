'''
Created on May 15, 2014
dfs the graph from node[0] (start node)
and mark node reached as positive
discard those not useful node
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')


from cxBase.base import cxConf,cxBaseC
from GraphBase.base import NodeC,GraphC
from GraphBase.DFSer import DFSerC


class QuerySubgraphKeepReachableC(DFSerC):
    
    def Init(self):
        super(QuerySubgraphKeepReachableC,self).Init()
        self.hReachedNode = {}
        self.StartNode = 0 
    
    def Process(self,Graph):
        
        self.DFS(self.StartNode, [], Graph)
        lDelNodeName = []
        for i in range(len(Graph.lNode)):
            if not  i in self.hReachedNode:
                lDelNodeName.append(Graph.lNode[i].name)
        Graph.BatchDelNode(lDelNodeName)
        return Graph
    
    
    def ProcessCurrentNode(self,CurrentNodeId,lPath,Graph):
        self.hReachedNode[CurrentNodeId] = True
    
    