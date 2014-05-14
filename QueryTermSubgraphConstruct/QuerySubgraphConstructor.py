'''
Created on May 13, 2014
construct the subgraph from bfs walk
all level < n objects/terms connected to the query via Freebase
inherited from BfsQueryFreebase
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
from cxBase.base import cxConf,cxBaseC,DiscardNonAlphaNonDigit
import json
from GoogleFreebaseAPI.BfsQueryFreebase import *
from base.ExpTerm import *
from IndriRelate.IndriInferencer import LmBaseC
from copy import deepcopy
import math



class QuerySubgraphConstructorC(BfsQueryFreebaseC):
    def SetConf(self,ConfIn):
        super(QuerySubgraphConstructorC,self).SetConf(ConfIn)
        
        OutName = self.WorkDir + "/QuerySubgraph"
        self.QSubgraphOut = open(OutName,'w')  
        
        return True
    
    def CleanUp(self):
        super(QuerySubgraphConstructorC,self).CleanUp()
        self.QSubgraphOut.close()
        
        
    def ProcessPerObj(self,lPath,FbObj,prob,qid,query):
        
        #if it is the last level, then do not expand
        if len(lPath) >= self.BFSLvl:
            return True
        
        #api left for sub class to process a bfs'd result. like vote up a term in FbObj's name
        print "get obj[%s][%s] via [%s]" %(FbObj.GetId(),FbObj.GetName(),json.dumps(lPath))
        
        
        #three things:
            #out obj-term-edgetype-score (score is tf)
            #out obj-linked neighbor-edgetype-score (prob calculate by function in super)
            #out obj-cotype neighbor-edgetype-score   (same as before)
        
        name = DiscardNonAlphaNonDigit(FbObj.GetName().encode('ascii','replace')).lower()
        desp = DiscardNonAlphaNonDigit(FbObj.GetDesp().encode('ascii','replace')).lower() #TF it?
        
        NameLm = LmBaseC(name)
        DespLm = LmBaseC(desp)
        
        for term in NameLm.hTermTF:
            print >> self.QSubgraphOut,"%s\t%s\t%s\t%f" %(FbObj.GetId(),
                                                          term,
                                                          'objname',
                                                          math.log(NameLm.GetTFProb(term)))
        for term in DespLm.hTermTF:
            print >> self.QSubgraphOut,"%s\t%s\t%s\t%f" %(FbObj.GetId(),
                                                          term,
                                                          'objdesp',
                                                          math.log(DespLm.GetTFProb(term)))
            
            
        #2,3
        lNeighborObj = self.ExpandObjNeighbor(FbObj)
        hEdgeProb = self.CalculateEdgeProb(lNeighborObj)
        
        for edge,ObjId in lNeighborObj:
            print >> self.QSubgraphOut,"%s\t%s\t%s\t%f" %(FbObj.GetId(),
                                                          ObjId,
                                                          edge,
                                                          math.log(hEdgeProb[edge])
                                                          )
            
        lCoTypeObj = self.ExpandTypeNeighbor(FbObj)
        hEdgeProb = self.CalculateEdgeProb(lCoTypeObj)
        for edge,ObjId in lCoTypeObj:
            print >> self.QSubgraphOut,"%s\t%s\t%s\t%f" %(FbObj.GetId(),
                                                          ObjId,
                                                          edge,
                                                          math.log(hEdgeProb[edge]))
            
        
        return True
    
    def ProcessInitObj(self,path,FbObj,prob,qid,query):
        #just out qid_query-obj-edgetype(the last in path)-score (the prob)
        print "init searched obj [%s][%s]" %(FbObj.GetId(),FbObj.GetName())
        print >> self.QSubgraphOut, "%s_%s\t%s\t%s\t%f" %(qid,query,
                                                          FbObj.GetId(),
                                                          path[len(path)-1],
                                                          prob)
        return True
    
    
def QuerySubgraphConstructorUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    BFSer = QuerySubgraphConstructorC(ConfIn)
    
    for line in open(InName):
        qid,query = line.strip().split('\t')
        BFSer.BFS(qid,query)
    BFSer.CleanUp()
    return True