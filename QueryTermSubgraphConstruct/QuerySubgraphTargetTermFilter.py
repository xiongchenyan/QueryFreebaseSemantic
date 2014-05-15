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
        print "start read expq"
        llExpTerm = ReadQExpTerms(InName)
        for lExpTerm in llExpTerm:
            print "processing q [%s]" %(lExpTerm[0].qid)
            self.ProcessPerQ(lExpTerm)
        return True
    
    def ProcessPerQ(self,lExpTerm):
        qid = lExpTerm[0].qid
        InName = self.GraphDumpDir + '/QuerySubgraph_' + qid
        OutName = self.OutDir + '/QuerySubgraph_' + qid
        
        InitGraph = GraphC()
        print "reading the graph from [%s]" %(InName)
        if not InitGraph.ReadFromSimpleEdgeFile(InName):
            return False
        InitGraph.OutSimpleEdgeFile(OutName +"_init")
        print "reversing it"
        ReverseGraph = InitGraph.GetReverse()
        ReverseGraph.OutSimpleEdgeFile(OutName+'_reverse')
        InitGraph.clear()
        print "marking start node"
        lStartNodeId = self.MarkStartNode(ReverseGraph,lExpTerm)
        print "[%d] start node" %(len(lStartNodeId))
        
        self.hUsefulEdge.clear()
        for StId in lStartNodeId:
            print "dfsing from [%d]" %(StId)
            self.DFS(StId, [], ReverseGraph)
            print "now target edge size [%d]" %(len(self.hUsefulEdge))
            #will update the hUsefulEdge
        print "filtering not useful ege"    
        ReverseGraph.DiscardNoneTargetEdge(self.hUsefulEdge)
        ReverseGraph.OutSimpleEdgeFile(OutName + "reversed_discard")
         
        ResGraph = ReverseGraph.GetReverse()
        ReverseGraph.clear()
        print "dumping res to [%s]" %(OutName)
        ResGraph.OutSimpleEdgeFile(OutName)
        ResGraph.clear()
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
    
    
    
    
    
    
        
        
    