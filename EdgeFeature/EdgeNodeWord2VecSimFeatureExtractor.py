'''    
Created on May 6, 2014
extract the average mid word2vec vector cosine
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from cxBase.base import *
from EdgeFeature.EdgeFeatureBase import *
from EdgeFeature.EdgeFeatureExtractor import *
from IndriRelate.CtfLoader import TermCtfC
from cxBase.KeyFileReader import KeyFileReaderC
from IndriRelate.IndriInferencer import LmBaseC
from word2vec.WordVecBase import *
import os
import pickle
import ntpath
from copy import deepcopy
import json



class EdgeNodeWord2VecSimFeatureExtractorC(EdgeFeatureExtractorC):
    
    def Init(self):
        super(EdgeNodeWord2VecSimFeatureExtractorC,self).Init()
        self.hTargetObj = {}
        self.Word2VecPath = ""
        self.ObjInforDir = ""
        self.MakeObjInfor = True
        
        
    @staticmethod
    def ShowConf():
        EdgeFeatureExtractorC.ShowConf()
        print "word2vec"
        
    def SetConf(self,ConfIn):
        super(EdgeNodeWord2VecSimFeatureExtractorC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.Word2VecPath = conf.GetConf('word2vec')
        self.ObjInforDir = self.OutDir + "/ObjInfor"
        if not os.path.isdir(self.ObjInforDir):
            os.makedirs(self.ObjInforDir)
        
        
    def LoadTargetObj(self):
        #load target obj ids in edge-obj-obj to hTargetObj
        
        KeyReader = KeyFileReaderC()
        KeyReader.MaxLinePerKey = self.MaxOccurPerEdge
        KeyReader.open(self.EdgeObjIn, 'r')
        print "start load target obj ids"
        for lEdgeObj in KeyReader:
            lEdgeObj = lEdgeObj[:self.MaxOccurPerEdge]
            for EdgeObj in lEdgeObj:
                self.hTargetObj[EdgeObj[1]] = True
                self.hTargetObj[EdgeObj[2]] = True      
            del lEdgeObj[:]
        print "load target obj ids done [%d]" %(len(self.hTargetObj))
        return True
        
    def MakeTargetObjInfor(self):
        #traverse word2vec dump
        #if objid in targetobj{} then write it into dict
        Word2VecReader = Word2VecReaderC()
        Word2VecReader.open(self.Word2VecPath)
        
        for wordvec in Word2VecReader:
            if not wordvec.Key() in self.hTargetObj:
                continue
            print "read target obj [%s]" %(wordvec.Key())
            
            OutName = self.ObjInforDir + "/" + wordvec.OutName()
            if os.path.isfile(OutName):
                continue
            print "new, dumping to disk"
            out = open(OutName,'w')
            print >> out, wordvec.dumps()
            out.close()
        print "make target obj infor finished"
        return True
    
    
    def ReadOneObjInfor(self,ObjId):
        wordvec = Word2VecC()
        wordvec.word = ObjId
        if not wordvec.load(self.ObjInforDir + "/" + wordvec.OutName()):
            wordvec.clear()
        return wordvec
    
    def ReadConnectObjInfor(self,lvCol):
        #lvCol is edge\tobjid \t objid
        lObjPair = [] #[(ObjInforA, B)]
        for vCol in lvCol:
            A = self.ReadOneObjInfor(vCol[1])
            B = self.ReadOneObjInfor(vCol[2])
            if A.empty() | B.empty():
                continue
            lObjPair.append([A,B])
        return lObjPair
    
    def EdgeFeatureOutName(self):
        return self.OutDir + "/nodeword2vecsim"
    
    def Extract(self,DumpDisk = False):
        if self.MakeObjInfor:
            self.LoadTargetObj()
            self.MakeTargetObjInfor()
        return super(EdgeNodeWord2VecSimFeatureExtractorC,self).Extract(DumpDisk)
        
        
    def ExtractOneEdge(self,lvCol):
        #in: lvCol is edge-obj-obj
        #out: EdgeFeature
        
        
        lvCol = lvCol[:self.MaxOccurPerEdge]
        
        EdgeFeature = EdgeFeatureC()
        EdgeFeature.edge = lvCol[0][0]
        print "extracting for [%s]" %(EdgeFeature.edge)
        lObjPair = self.ReadConnectObjInfor(lvCol)
        
        print "load [%d] obj pair" %(len(lObjPair))
        
        
        EdgeFeature.AddFeature(self.ExtractObjWord2VecFeature(lObjPair))
        return EdgeFeature
    
    
    def ExtractObjWord2VecFeature(self,lObjPair):
        score = 0
        for A,B in lObjPair:
            score += Word2VecC.cosine(A, B)
        score /= float(len(lObjPair))
        
        hFeature = {}
        hFeature['AvgObjWord2VecSim'] = score
        return hFeature
    
    
    
             
        