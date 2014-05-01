'''
Created on Apr 22, 2014
extract group 2 feature
@author: cx
'''



'''
input:
    FbDump, gzip format
    Edge: obj obj
output:
    edge: feature score
    
parallel in edge level?
    bottle necks:
        1 FbDump IO (1h per traverse?) Gzip is more in CPU?
        2 Edge: obj obj information memory (limit the # of occur used for each edge should be fine approximation)
        3 Obj cash center/read, load
    edge level solves 2 and 3

Need a Object information dump
    information required for each object:
        Lm of description
        Category fraction (lm of category lvl 1 domain)
        Notable type

then need two step:
    1: go through Fb dump to get all obj's infor
    2: go through all edge-obj-obj with obj's information dumped, and calc the score
'''


'''
4.29 add idf in cosine sim between obj desp

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
from FreebaseDump.FbDumpBasic import *
from FreebaseDump.FbDumpReader import FbDumpReaderC 
import os
import pickle
import ntpath
from copy import deepcopy
import json
class FbDumpObjInforC(object):
    #the class to keep object infor:
        #Lm of desp
        #category
    def Init(self):
        self.ObjId = ""
        self.DespLm = LmBaseC()
        self.DomainLm  = LmBaseC()
        self.hNotableType = {}       
        return
    
    def empty(self):
        if self.DespLm.empty() & self.DomainLm.empty():
            return True
        return False
    
    def clear(self):
        self.ObjId = ""
        self.DespLm.clear()
        self.DomainLm.clear()
        self.hNotableType.clear()
        
    
    def __init__(self,lObjvCol = []):
        self.Init()
        if [] != lObjvCol:
            self.FormFromObjDump(lObjvCol)
    
    def dump(self,OutName):
        out = open(OutName,'w')
        pickle.dump(self.hNotableType,out)
        pickle.dump(self.DespLm.hTermTF,out)
        pickle.dump(self.DomainLm.hTermTF,out)        
        out.close()
        return True
    

    
    def dumps(self):
        res = json.dumps(self.ObjId) + "\n" + json.dumps(self.DespLm.hTermTF)
        res += "\n" + json.dumps(self.DomainLm.hTermTF) + "\n" + json.dumps(self.hNotableType)
        return res
    
    def load(self,InName):
        try:
            InFile = open(InName)
        except IOError:
            print "obj's infor dump [%s] file open failed" %(InName)
            return False
        self.ObjId = FbDumpObjInforC.ReverseIdFromFName(InName)
        self.hNotableType = pickle.load(InFile)
        self.DespLm.hTermTF = pickle.load(InFile)
        self.DespLm.CalcLen()
        self.DomainLm.hTermTF = pickle.load(InFile)
        self.DomainLm.CalcLen()
        return True
    
    
    def GetFname(self):
        return self.ObjId[:200].replace('/','_')
        
    @staticmethod
    def ReverseIdFromFName(FName):
        return ntpath.basename(FName).replace('_','/')
    
    def FormFromObjDump(self,lObjvCol):
        #fill the attributes
        #tbd: check how the notable type in dump is
        self.ObjId = lObjvCol[0][0]
        
        NotableType = GetNotableType(lObjvCol)
        self.hNotableType[NotableType] = True
        
        Desp = GetDesp(lObjvCol)
        self.DespLm.AddRawText(Desp)
        
        
        for vCol in lObjvCol:
            domain = GetDomain(vCol[1])
            self.DomainLm.Insert(domain, 1)
        
        return True
        
        
    
    def __deepcopy__(self,memo):
        NewInfor = FbDumpObjInforC()
        NewInfor.ObjId = deepcopy(self.ObjId,memo)
        NewInfor.hNotableType = deepcopy(self.hNotableType,memo)
        NewInfor.DespLm = deepcopy(self.DespLm,memo)
        NewInfor.DomainLm = deepcopy(self.DomainLm,memo)
        return NewInfor
    
    
    



class EdgeNodeFbSimFeatureExtractorC(EdgeFeatureExtractorC):
    def Init(self):
        super(EdgeNodeFbSimFeatureExtractorC,self).Init()
        
        self.hTargetObj = {}
        self.ObjInforDir = ""
        self.MaxOccurPerEdge = 100
        self.CtfCenter = TermCtfC()
        
        
    @staticmethod
    def ShowConf():
        EdgeFeatureExtractorC.ShowConf()
        print "maxoccurperedge\nctf"
        
    def SetConf(self,ConfIn):
        super(EdgeNodeFbSimFeatureExtractorC,self).SetConf(ConfIn)
        self.ObjInforDir = self.OutDir + "/ObjInfor"
        if not os.path.isdir(self.ObjInforDir):
            os.makedirs(self.ObjInforDir)
            
        conf =cxConf(ConfIn)
        self.MaxOccurPerEdge = int(conf.GetConf('maxoccurperedge',self.MaxOccurPerEdge))
        
        self.CtfCenter.Load((conf.GetConf('ctf')))
        
        
    
            
            
            
    
    def LoadTargetObj(self):
        #load target obj ids in edge-obj-obj to hTargetObj
        
        KeyReader = KeyFileReaderC()
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
        #traverse FbDump
        #for each required obj id
            #make its information center
            #dump to dir
        
        print "start make target obj infor from dump"
        FbDumpReader = FbDumpReaderC()
        FbDumpReader.MaxLinePerKey = 10000
        FbDumpReader.open(self.FbDumpIn,'r')
        cnt = 0
        for lvColObj in FbDumpReader:
            ThisObjId = lvColObj[0][0]
            if not ThisObjId in self.hTargetObj:
                continue
            ObjInfor = FbDumpObjInforC()
            ObjInfor.ObjId = ThisObjId
            OutName = self.ObjInforDir + "/" + ObjInfor.GetFname()
            if os.path.isfile(OutName):
                continue
            print "read target obj [%s]" %(ThisObjId)
            ObjInfor = FbDumpObjInforC(lvColObj)
            ObjInfor.dump(OutName)
            cnt += 1
            ObjInfor.clear()
            del lvColObj[:] 
        print "obj infor dumped, total [%d] obj" %(cnt)
        return True
    
    
    def Extract(self,DumpDisk = False):
        self.LoadTargetObj()
        self.MakeTargetObjInfor()
        return super(EdgeNodeFbSimFeatureExtractorC,self).Extract(DumpDisk)
        
        
    def ExtractOneEdge(self,lvCol):
        #in: lvCol is edge-obj-obj
        #out: EdgeFeature
        
        
        lvCol = lvCol[:self.MaxOccurPerEdge]
       
        EdgeFeature = EdgeFeatureC()
        EdgeFeature.edge = lvCol[0][0]
        print "extracting for [%s]" %(EdgeFeature.edge)
        lObjPair = self.ReadConnectObjInfor(lvCol)
        
        print "load [%d] obj pair" %(len(lObjPair))
        
        
#         EdgeFeature.AddFeature(self.ExtractObjNotableCntFeature(lObjPair,EdgeFeature.edge))
        EdgeFeature.AddFeature(self.ExtractObjTextSimFeature(lObjPair))
        EdgeFeature.AddFeature(self.ExtractObjTypeProbFeature(lObjPair,EdgeFeature.edge))
        
        return EdgeFeature
    
    
    def EdgeFeatureOutName(self):
        return self.OutDir + "/nodefbsim"
    
    
    
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
    
    
    def ReadOneObjInfor(self,ObjId):
        ObjInfor = FbDumpObjInforC()
        ObjInfor.ObjId = ObjId
        if not ObjInfor.load(self.ObjInforDir + "/" + ObjInfor.GetFname()):
            ObjInfor.clear()
        return ObjInfor
        
    
    
    def ExtractObjTextSimFeature(self,lObjPair):
        hFeature = {}
        score = 0
        for ObjInforA,ObjInforB in lObjPair:
            score += LmBaseC.TfIdfCosine(ObjInforA.DespLm,  ObjInforB.DespLm)
        score /= len(lObjPair)
        hFeature['AvgObjTextSim'] = score
        
        return hFeature
    
    
    def ExtractObjNotableCntFeature(self,lObjPair,edge):
        hFeature = {}
        
        EdgeDomain = GetDomain(edge)
        
        if 'cotype' in EdgeDomain:
            EdgeDomain = EdgeDomain.replace('cotype','')
        
        score = 0
        
        for ObjInforA,ObjInforB in lObjPair:
            if EdgeDomain in ObjInforA.hNotableType:
                score += 1
            if EdgeDomain in ObjInforB.hNotableType:
                score += 1
                
        score /= lObjPair * 2.0
        
        hFeature['AvgObjNotableTypeSameCnt'] = score
        
        return hFeature
    
    
    def ExtractObjTypeProbFeature(self,lObjPair,edge):
        hFeature = {}
        
        EdgeDomain = GetDomain(edge)
        if 'cotype' in EdgeDomain:
            EdgeDomain = EdgeDomain.replace('cotype','')
        score = 0
        
        for A,B in lObjPair:
            score += (A.DomainLm.GetTFProb(EdgeDomain) 
                      + B.DomainLm.GetTFProb(EdgeDomain)) / 2.0
      
        score /= len(lObjPair)
        
        hFeature['AvgObjSameDomainProb'] = score
        return hFeature
    
        
    
    