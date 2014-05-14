'''
Created on May 13, 2014
filter out subgraph that does not connected to given target (candidate) terms
input: llExpTerm, graph dir,
do: for each lExpTerm
    locate its graph name (_%d qid)
    read,
    reverse graph,
    match start nodes (candidate terms)
    dfs for path that lead to query in 4 hop (term->obj->obj->obj->q)
        mark edge in these path as useful
    discard non-useful paths
    reverse back
output: a cleaned graph

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


from base.ExpTerm import *


class QuerySubgraphTargetTermFilterC(DFSerC):
    def Init(self):
        super(QuerySubgraphTargetTermFilterC,self).Init()
        self.GraphDumpDir = ""
        self.OutDir = ""
        self.hUsefulEdge = {}
        
    @staticmethod
    def ShowConf():
        print "graphdumpdir\noutdir"
    def SetConf(self,ConfIn):
        super(QuerySubgraphTargetTermFilterC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.GraphDumpDir = conf.GetConf('graphdumpdir')
        self.OutDir = conf.GetConf('outdir')
        
        
    
    def Process(self,InName):
        llExpTerm = ReadQExpTerms(InName)
        for lExpTerm in llExpTerm:
            self.ProcessPerQ(lExpTerm)
        return True
    
    def ProcessPerQ(self,lExpTerm):
        qid = lExpTerm[0].qid
        InName = self.GraphDumpDir + '/QuerySubgraph_' + qid
        OutName = self.OutDir + '/QuerySubgraph_' + qid
        
        InitGraph = GraphC()
        InitGraph.ReadFromSimpleEdgeFile(InName)
        ReverseGraph = InitGraph.GetReverse()
        
        lStartNodeId = self.MarkStartNode(ReverseGraph,lExpTerm)
        
        for StId in lStartNodeId:
            self.DFS(StId, [], ReverseGraph)
            #will update the hUsefulEdge
            
        self.DiscardNoneUsefulEdge(ReverseGraph,self.hUsefulEdge)
        ResGraph = ReverseGraph.GetReverse()
        
        ResGraph.OutSimpleEdgeFile(OutName)
        
        print "query [%s] finished" %(qid)
        return True
    
    
    def ProcessCurrentNode(self,CurrentNodeId,lPath,Graph):
        #if current node is a query node, then mark all edge in lpath as useful
        if not self.IsAQueryNodeName(Graph.lNode[CurrentNodeId].name):
            return True
        
        for edge in lPath:
            self.hUsefulEdge[edge] = True       
        return True
    
    def IsAQueryNodeName(self,name):
        if '_' in name:
            return True
        return False
    
    def MarkStartNode(self,Graph,lExpTerm):
        #get all term nodein lExpTerm, and mark as start node
        lStartNodeId = []
        for ExpTerm in lExpTerm:
            term = ExpTerm.term
            if term in Graph.hNode:
                lStartNodeId.append(Graph.hNode[term])
        return lStartNodeId
    
    
    def DiscardNoneUsefulEdge(self,Graph,hTargetEdge):
        Graph.DiscardNoneTargetEdge(hTargetEdge)
        return True
    
    
    
    
    
    
        
        
    