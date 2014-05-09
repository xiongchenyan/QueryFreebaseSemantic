'''
Created on Apr 9, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import cxConf,cxBaseC,DiscardNonAlphaNonDigit
import json
from GoogleFreebaseAPI.BfsQueryFreebase import *
from base.ExpTerm import *
from IndriRelate.IndriInferencer import LmBaseC
from copy import deepcopy
import math
class QueryTermBFSLinkerC(BfsQueryFreebaseC):
    def SetConf(self,ConfIn):
        super(QueryTermBFSLinkerC,self).SetConf(ConfIn)
        
        OutName = self.WorkDir + "/QueryTermLink"
        self.QTermOut = open(OutName,'w')  
        
        return True
    
        
    def ProcessPerObj(self, lPath,FbObj,prob,qid,query):
        #form a expterm for each term in FbObj's name and desp
        #output to QTermOut
        expterm = ExpTermC()
        expterm.qid = qid
        expterm.query = query
        
        
        name = DiscardNonAlphaNonDigit(FbObj.GetName().encode('ascii','replace')).lower()
        desp = DiscardNonAlphaNonDigit(FbObj.GetDesp().encode('ascii','replace')).lower() #TF it?
        
        NameLm = LmBaseC(name)
        DespLm = LmBaseC(desp)
        
        
#         print "q[%s] obj [%s] get [%d] in name [%d] in desp" %(query,
#                                                                FbObj.GetId().encode('utf-8','ignore'),
#                                                                len(NameLm.hTermTF),
#                                                                len(DespLm.hTermTF))
#         print "name[%s] desp [%s]" %(name.encode('utf-8','ignore'),
#                                      desp.encode('utf-8','ignore'))
        NameFeatureName = json.dumps(lPath + ['name'])
        for term in NameLm.hTermTF:
            ThisExpTerm = deepcopy(expterm)
            ThisExpTerm.term = term
            ThisExpTerm.hFeature[NameFeatureName] = prob + math.log(NameLm.GetTFProb(term))
            print >> self.QTermOut, ThisExpTerm.dump()
        
        DespFeatureName = json.dumps(lPath + ['desp'])
        for term in DespLm.hTermTF:
            ThisExpTerm = deepcopy(expterm)
            ThisExpTerm.term = term
            ThisExpTerm.hFeature[DespFeatureName] = prob + math.log(DespLm.GetTFProb(term))
            print >> self.QTermOut, ThisExpTerm.dump()          
        return True
    
    
#     def dump(self):
#         super(QueryTermBFSLinkerC,self).dump()
#         self.QTermOut.close()
#         return True

    def CleanUp(self):
        super(QueryTermBFSLinkerC,self).CleanUp()
        self.QTermOut.close()


        
def QueryTermBFSLinkerUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    InName = conf.GetConf('in')
    BFSer = QueryTermBFSLinkerC(ConfIn)
    
    for line in open(InName):
        qid,query = line.strip().split('\t')
        BFSer.BFS(qid,query)
    BFSer.CleanUp()
    return True
        
           