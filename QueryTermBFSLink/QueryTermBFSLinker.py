'''
Created on Apr 9, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import cxConf,cxBaseC
import json
from GoogleFreebaseAPI.BfsQueryFreebase import *
from base.ExpTerm import *
from IndriRelate.IndriInferencer import LmBaseC
from copy import deepcopy

class QueryTermBFSLinkerC(BfsQueryFreebaseC):
    def SetConf(self,ConfIn):
        super(QueryTermBFSLinkerC,self).SetConf(ConfIn)
        
        OutName = self.WorkDir + "/QueryTermLink"
        self.QTermOut = open(OutName,'w')  
        
        return True
    
        
    def ProcessPerObj(self,lPath,FbObj,qid,query):
        #form a expterm for each term in FbObj's name and desp
        #output to QTermOut
        expterm = ExpTermC()
        expterm.qid = qid
        expterm.query = query
        
        
        name = FbObj.GetName()
        desp = FbObj.GetDesp() #TF it?
        
        NameLm = LmBaseC(name)
        DespLm = LmBaseC(desp)
        
        
        NameFeatureName = json.dumps(lPath + ['name'])
        for term in NameLm.hTermTF:
            ThisExpTerm = deepcopy(expterm)
            ThisExpTerm.hFeature[NameFeatureName] = NameLm.GetTFProb(term)
            print >> self.QTermOut, ThisExpTerm.dump()
        
        DespFeatureName = json.dumps(lPath + ['desp'])
        for term in DespLm.hTermTF:
            ThisExpTerm = deepcopy(expterm)
            ThisExpTerm.hFeature[DespFeatureName] = NameLm.GetTFProb(term)
            print >> self.QTermOut, ThisExpTerm.dump()          
        
        return True
    
    
    def dump(self):
        super(QueryTermBFSLinkerC,self).dump()
        self.QTermOut.close()
        return True




        
def QueryTermBFSLinkerUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    BFSer = QueryTermBFSLinkerC(ConfIn)
    
    for line in open(InName):
        qid,query = line.strip().split('\t')
        BFSer.BFS(qid,query)
    BFSer.dump()
    return True
        
           