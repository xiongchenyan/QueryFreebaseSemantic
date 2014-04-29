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
        self.UWSize = 100
        self.hEdge = {} #edge -> cnt in occur
        self.MaxOccurPerEdge = 1000
        self.hObjPairToEdge = {}
        self.hEdgeCorCnt = {}
        self.hEdgeUWCorCnt = {}
        
    @staticmethod
    def ShowConf():
        EdgeFeatureExtractorC.ShowConf()
        print "maxoccurperedge\nuwsize"
        
    def SetConf(self,ConfIn):
        super(EdgeNodeFaccSimFeatureExtractorC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.MaxOccurPerEdge = int(conf.GetConf('maxoccurperedge',self.MaxOccurPerEdge))
        self.UWSize = int(conf.GetConf('uwsize',self.UWSize))
        
        return True
    
    
    def ReadEdgeObjData(self):
        #read and make hEdge, hObjPairToEdge
        print "start read edge obj"
        EdgeObjReader = KeyFileReaderC()
        EdgeObjReader.open(self.EdgeObjIn)
        for lvCol in EdgeObjReader:
            lvCol = lvCol[:self.MaxOccurPerEdge]
            self.hEdge[lvCol[0][0]] = len(lvCol)
            self.hEdgeCorCnt[lvCol[0][0]] = 0
            self.hEdgeUWCorCnt[lvCol[0][0]] = 0
            for vCol in lvCol:
                key = '\t'.join(vCol[1:])
                if not key in self.hObjPairToEdge:
                    self.hObjPairToEdge[key] = []
                self.hObjPairToEdge[key].append(vCol[0])
        EdgeObjReader.close()      
        return True
    
    
    def MakeObjCorFromFacc(self):
        #read facc from FaccDir
        #update hEdgeCorCnt and hEdgeUWCorCnt
        
        FaccReader = FaccReaderC()
        FaccReader.opendir(self.FaccDir)
        print "start read facc data"
        for lFacc in FaccReader:
            self.UpdateOneFacc(lFacc)
            
        print "read facc data finished"        
        return True
    
    def UpdateOneFacc(self,lFacc):
        #update for one facc
        
        #O(len(lFacc)^2)
        
        
        for i in range(len(lFacc)):
            for j in range(len(lFacc)):
                if i == j:
                    continue
                
                AnoA = lFacc[i]
                AnoB = lFacc[j]
                
                Key = AnoA.ObjId + "\t" + AnoB.ObjId
                if not Key in self.hObjPairToEdge:
                    continue
                edge = self.hObjPairToEdge[Key]
                self.hEdgeCorCnt[edge] += 1
                if math.fabs(AnoA.st - AnoB.st) <= self.UWSize:
                    self.hEdgeUWCorCnt[edge] += 1
        
        return True
    
    
    def Extract(self,DumpDict = False):
        self.ReadEdgeObjData()
        self.MakeObjCorFromFacc()
        return super(EdgeNodeFaccSimFeatureExtractorC,self).Extract(DumpDict)
    
    
    def ExtractOneEdge(self,lvCol):
        #actually only use infor kept in dicts
        EdgeFeature = EdgeFeatureC()
        edge = lvCol[0][0]
        EdgeFeature.edge = edge
        
        EdgeFeature.AddFeature(self.ExtractFaccCor(edge))
        EdgeFeature.AddFeature(self.ExtractFaccUWCor(edge))
        
        return EdgeFeature
    
    
    def ExtractFaccCor(self,edge):
        hFeature = {}
        score = 0
        if edge in self.hEdgeCorCnt:
            score = float(self.hEdgeCorCnt[edge]) / float(self.hEdge[edge])
        hFeature['AvgObjFaccCor'] = score 
        return hFeature
    
    def ExtractFaccUWCor(self,edge):
        hFeature = {}
        score = 0
        if edge in self.hEdgeUWCorCnt:
            score = float(self.hEdgeUWCorCnt[edge]) / float(self.hEdge[edge])
        hFeature['AvgObjFaccUWCor'] = score 
        return hFeature
        
        
            
            
    def EdgeFeatureOutName(self):
        return self.OutDir + "/nodefaccsim"        
        
