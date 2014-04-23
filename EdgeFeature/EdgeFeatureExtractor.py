'''
Created on Apr 21, 2014
the root class the extract feature for edge
need two passes...

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')


from cxBase.base import cxConf, cxBaseC
from EdgeFeatureBase import EdgeFeatureC
import os
from cxBase.KeyFileReader import *


#the base class of edge feature extraction
    #3 sub class:
        #Group 1 ,2 ,3 features
class EdgeFeatureExtractorC(cxBaseC):
    def Init(self):
        self.OutDir = ""
        self.EdgeObjIn = ""
        self.FbDumpIn = ""
        self.FaccDir = ""
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.OutDir = conf.GetConf('out')
        if not os.path.isdir(self.OutDir):
            os.makedirs(self.OutDir)
            
        self.EdgeObjIn = conf.GetConf('in')
        self.FbDumpIn = conf.GetConf('fbdumpin')
        self.FaccDir = conf.GetConf('faccdir')
        
        
    @staticmethod
    def ShowConf():
        print "out\nin\nfbdumpin\nfaccdir"
    
    def Extract(self,DumpDisk = False):
        
        KeyReader = KeyFileReaderC()
        KeyReader.open(self.EdgeObjIn)
        
        if DumpDisk:
            out = open(self.EdgeFeatureOutName(),'w')
        lEdgeFeature = []
        for lvCol in KeyReader:
            EdgeFeature = self.ExtractOneEdge(lvCol)
            lEdgeFeature.append(EdgeFeature)
            if DumpDisk:
                print "dumping feature for [%s]" %(EdgeFeature.edge)
                print >>out, EdgeFeature.dumps()
        if DumpDisk:
            out.close()
        return lEdgeFeature
    
    
    def ExtractOneEdge(self,lvCol):
        print "ExtractOneEdge to be implemented in sub classes"
        return False
    
    
    def EdgeFeatureOutName(self):
        print "EdgeFeatureOutName to be implemented in sub classes"