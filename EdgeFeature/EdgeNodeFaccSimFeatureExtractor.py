'''
Created on Apr 22, 2014
extract node facc sim feature
group 3:
    facc sim feature:
        Avg obj a, b co-doc cnt
        Avg obj a, b, co-doc with in window        
@author: cx
'''



'''
input: edge obj obj, facc dir
do:
    read edge-obj-obj
        keep a structure:
            obj-obj -> edge name
    traverse facc data ( via a facc data reader in GoogleAPI)
        for each pair in a clueweb doc:
        keep and update two dict:
            edge-> obj pair co-doc cnt
            edge -> obj pair co-doc with in window cnt


'''

'''
4.29 tbd:
improve the cnt-correlation to PMI
4.30
implemented tbd: test and run
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from cxBase.base import *
from EdgeFeature.EdgeFeatureBase import *
from EdgeFeature.EdgeFeatureExtractor import *
from cxBase.KeyFileReader import KeyFileReaderC
from IndriRelate.IndriInferencer import LmBaseC
from Facc.FaccReader import FaccReaderC
from Facc.FaccBase import FaccAnnotationC
import os
import pickle
import ntpath
from copy import deepcopy
import math


class EdgeNodeFaccSimFeatureExtractorC(EdgeFeatureExtractorC):
    def Init(self):
        super(EdgeNodeFaccSimFeatureExtractorC,self).Init()        
        self.UWSize = 100
#         self.hEdge = {} #edge -> cnt in occur
#         self.hObjPairToEdge = {}
#         self.hEdgeCorCnt = {}
#         self.hEdgeUWCorCnt = {}
        self.hObjCnt = {} #cnt in facc
        self.hObjPairCnt = {} #cnt + uwcnt []
        self.FaccTotal = 0.0
        
    @staticmethod
    def ShowConf():
        EdgeFeatureExtractorC.ShowConf()
        print "maxoccurperedge\nuwsize"
        
    def SetConf(self,ConfIn):
        super(EdgeNodeFaccSimFeatureExtractorC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.UWSize = int(conf.GetConf('uwsize',self.UWSize))
        
        return True
    
    
    def ReadEdgeObjData(self):
        #read and make hEdge, hObjPairToEdge
        print "start read edge obj"
        EdgeObjReader = KeyFileReaderC()
        EdgeObjReader.MaxLinePerKey = self.MaxOccurPerEdge
        EdgeObjReader.open(self.EdgeObjIn)
        for lvCol in EdgeObjReader:
            lvCol = lvCol[:self.MaxOccurPerEdge]
            for vCol in lvCol:
                self.hObjCnt[vCol[1]] = 0
                self.hObjCnt[vCol[2]] = 0
                self.hObjCnt[vCol[1] + "\t" + vCol[2]] = [0,0]    
            del lvCol[:]
        EdgeObjReader.close()      
        print "total [%d] obj" %(len(self.hObjCnt))
        return True
    
    
    def MakeObjCorFromFacc(self):
        #read facc from FaccDir
        #update hEdgeCorCnt and hEdgeUWCorCnt
        
        FaccReader = FaccReaderC()        
        FaccReader.opendir(self.FaccDir)
        print "start read facc data"
        for lFacc in FaccReader:
            self.UpdateOneFacc(lFacc)
            del lFacc[:]
        
        
        out = open(self.OutDir + "/facccorrelation",'w')
        pickle.dump(self.hObjCnt,out)
        pickle.dump(self.hObjPairCnt,out)
        out.close()
            
        print "read facc data finished"        
        return True
    
    def UpdateOneFacc(self,lFacc):
        #update for one facc
        
        #O(len(lFacc)^2)
        print "working on facc [%s]" %(lFacc[0].DocNo)
        self.FaccTotal += 1.0
        lObj = []
        lObjPair = []
        lUWObjPair = []
        for i in range(len(lFacc)):
            if not lFacc[i].ObjId in lObj:
                if lFacc[i].ObjId in self.hObjCnt:
                    lObj.append(lFacc[i].ObjId) 
                    print "[%s] appear" %(lFacc[i].ObjId)
            for j in range(len(lFacc)):
                if i == j:
                    continue
                AnoA = lFacc[i]
                AnoB = lFacc[j]
                Key = AnoA.ObjId + "\t" + AnoB.ObjId
                if not Key in self.hObjPairCnt:
                    continue
                if not Key in lObjPair:
                    lObjPair.append(Key)
                    print "[%s] pair appear" %(Key)
                if math.fabs(AnoA.st - AnoB.st) <= self.UWSize:
                    if not Key in lUWObjPair:
                        lUWObjPair.append(Key)
                        print "[%s] uw pair appear" %(Key)
        
        for Obj in lObj:
            self.hObjCnt[Obj] += 1
        for Key in lObjPair:
            self.hObjPairCnt[Key][0] += 1
        for Key in lUWObjPair:
            self.hObjPairCnt[Key][1] += 1
        return True
    
    
    def Extract(self,DumpDict = False):
        self.ReadEdgeObjData()
        self.MakeObjCorFromFacc()
        return super(EdgeNodeFaccSimFeatureExtractorC,self).Extract(DumpDict)
    
    
    def ExtractOneEdge(self,lvCol):
        #actually only use infor kept in dicts
        print "start extacting for [%s]" %(lvCol[0][0])
        EdgeFeature = EdgeFeatureC()
        edge = lvCol[0][0]
        EdgeFeature.edge = edge
        
        EdgeFeature.AddFeature(self.ExtractFaccCor(lvCol))
        EdgeFeature.AddFeature(self.ExtractFaccUWCor(lvCol))
        
        return EdgeFeature
    
    
    def ExtractFaccCor(self,lvCol):
        hFeature = {}
        score = 0
        
        for vCol in lvCol:
            ObjA = vCol[1]
            ObjB = vCol[2]
            score += self.CalcPmi(ObjA, ObjB, 0)
        score /= float(len(lvCol))
        hFeature['AvgObjFaccCor'] = score 
        return hFeature
    
    def ExtractFaccUWCor(self,lvCol):
        hFeature = {}
        score = 0
        for vCol in lvCol:
            ObjA = vCol[1]
            ObjB = vCol[2]
            score += self.CalcPmi(ObjA, ObjB, 1)
        score /= float(len(lvCol))
        hFeature['AvgObjFaccUWCor'] = score 
        return hFeature
        
    def CalcPmi(self,ObjA,ObjB,UseIndex = 0):    
        PairKey = ObjA + "\t" + ObjB
        pa = 1
        pb = 1
        if ObjA in self.hObjCnt:
            pa = max(pa,self.hObjCnt[ObjA])
        if ObjB in self.hObjCnt:
            pb = max(pb,self.hObjCnt[ObjB])
        
        pa /= self.FaccTotal
        pb /= self.FaccTotal
        pab = pa * pb
        if PairKey in self.hObjPairCnt:
            pab = max(pab,self.hObjPairCnt[PairKey][UseIndex]/self.FaccTotal)
        return PMI(pa,pb,pab)   
            
    def EdgeFeatureOutName(self):
        return self.OutDir + "/nodefaccsim"        
        
