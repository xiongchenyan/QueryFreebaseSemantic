'''
Created on May 15, 2014
rule based filter
in: subgraph dir
out: filtered dir
@author: cx
'''

'''
As of May 15, 2014:
discard cotype edge
discard edge in music, award. book domain
only keep node that is connected from node[0] "the query node"

'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from GraphBase.base import *
from FreebaseDump.FbDumpBasic import GetDomain
from cxBase.WalkDirectory import WalkDir
from cxBase.base import cxBaseC,cxConf
from QueryTermSubgraphConstruct.QuerySubgraphKeepReachable import QuerySubgraphKeepReachableC
import ntpath

class QuerySubgraphRuleFilterC(cxBaseC):
    def Init(self):
        self.FilterCotype = True
        self.lFilterDomain = []
        self.InGraphDir = ""
        self.OutGraphDir = ""
        
    @staticmethod
    def ShowConf():
        print "cotypefilter True\nfilterdomain\ningraphdir\noutgraphdir"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FilterCotype = bool(conf.GetConf('cotypefilter',self.CotypeFilter))
        self.filterdomain = conf.GetConf('filterdomain')
        if type(self.filterdomain) != list:
            self.filterdomain = [self.filterdomain]
        self.InGraphDir = conf.GetConf('ingraphdir')
        self.OutGraphDir = conf.GetConf('outgraphdir')
        
    
    
    def Process(self):
        lFName = WalkDir(self.InGraphDir)
        for FName in lFName:
            print "processing [%s]" %(FName)
            Graph = GraphC()
            Graph.ReadFromSimpleEdgeFile(FName)
            self.ProcessOneGraph(Graph)
            OutName = self.OutGraphDir + "/" + ntpath.basename(FName)
            Graph.OutSimpleEdgeFile(OutName)
        return True
        
        
    def ProcessOneGraph(self,Graph):
        #apply filter
        if self.FilterCotype:
            self.CotypeFilter(Graph)
        if len(self.lFilterDomain) != 0:
            self.DomainFilter(Graph)
        
        Keeper = QuerySubgraphKeepReachableC()
        Graph = Keeper.Process(Graph)
        return Graph
    
    
    def CotypeFilter(self,Graph):
        for i in range(len(Graph.lNode)):
            for j in Graph.lNode[i].hChild:
                llNewEdgeAttr = []
                for k in range(len(Graph.lNode[i].hChild[j])):
                    lEdgeAttr = Graph.lNode[i].hChild[j][k]
                    if 'cotype' in lEdgeAttr[0]:
                        continue
                    llNewEdgeAttr.append(lEdgeAttr)
                if len(llNewEdgeAttr) != 0:
                    Graph.lNode[i].hChild[j] = llNewEdgeAttr
                else:
                    del Graph.lNode[i].hChild[j]
        return True
    
    def DomainFilter(self,Graph):
        for i in range(len(Graph.lNode)):
            lToDel = []
            for j in Graph.lNode[i].hChild:
                llNewEdgeAttr = []
                for k in range(len(Graph.lNode[i].hChild[j])):
                    lEdgeAttr = Graph.lNode[i].hChild[j][k]
                    if GetDomain(lEdgeAttr[0]) in self.lFilterDomain:
                        continue
                    llNewEdgeAttr.append(lEdgeAttr)
                if len(llNewEdgeAttr) != 0:
                    Graph.lNode[i].hChild[j] = llNewEdgeAttr
                else:
                    lToDel.append(j)
            for j in lToDel:
                Graph.DeleteEdge((i,j))
        return True
                        
                        
        
        

