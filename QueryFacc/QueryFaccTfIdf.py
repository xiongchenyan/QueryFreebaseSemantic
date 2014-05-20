'''
Created on May 20, 2014
get the tf-idf weight of each query's idf in facc
input: query, facc doc ana dir, facc idf
output: query-facc(name, mid)-tf-idf-tfidf
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

import math
import sys
from cxBase.base import cxBaseC,cxConf
from IndriRelate.CtfLoader import TermCtfC
from Facc.FaccDoc import FaccForDocC


class QueryFaccTfIdfC(cxBaseC):
    def Init(self):
        self.FaccDocDir = ""
        self.InName = ""
        self.OutName = ""
        self.FaccCtf = TermCtfC()
        
        
    @staticmethod
    def ShowConf():
        print "faccdocdir\nin\nout\nobjctf"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.FaccDocDir= conf.GetConf('faccdocdir')
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        CtfInName = conf.GetConf('objctf')
        if "" != CtfInName:
            self.FaccCtf.Load(CtfInName)
            print "ctf load from [%s]" %(CtfInName)
            
            
    def ProcessPerQ(self,query):
        lFaccDoc = FaccForDocC().ReadFaccDocs(self.FaccDocDir + "/" + query)
        hObjIdNameTf = {}
        for FaccDoc in lFaccDoc:
            for Facc in FaccDoc.lFacc:
                if not Facc.ObjId in hObjIdNameTf:
                    hObjIdNameTf[Facc.ObjId] = [Facc.entity,1]
                else:
                    hObjIdNameTf[Facc.ObjId][1] += 1
                    
        lObj = [[item,value[0],value[1],self.FaccCtf.GetCtfProb(item),value[1] * math.log(1.0/self.FaccCtf.GetCtfProb(item))] for item,value in hObjIdNameTf.items()]
        
        lObj.sort(key=lambda item: item[4], reverse = True)
        return lObj
    
    
    def Process(self):
        out = open(self.OutName,'w')
        for line in open(self.InName):
            qid,query = line.strip().split('\t')
            lObj = self.ProcessPerQ(query)
            for item in lObj:
                print >> out, qid + "\t" + query + "\t%s\t%s\t%f\t%f\t%f" %(item[0],item[1],item[2],item[3],item[4])
        out.close()
        return True
    
    
if 2 != len(sys.argv):
    print "conf"
    QueryFaccTfIdfC().ShowConf()
    sys.exit()
    
    
TfIdf = QueryFaccTfIdfC(sys.argv[1])
TfIdf.Process()
print "finished"
    


