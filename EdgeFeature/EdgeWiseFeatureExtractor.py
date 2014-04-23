'''
Created on Apr 21, 2014
Group 1 features:
    edge domain
    edge level in obtology
    edge cnt
    
just need the edge\tobj\tobj file


4/22/2014 2:13 implemented

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.base import cxConf, cxBaseC
from EdgeFeatureBase import EdgeFeatureC
from EdgeFeatureExtractor import *
from FreebaseDump.FbDumpBasic import *

import math

class EdgeWiseFeatureExtractorC(EdgeFeatureExtractorC):
    



    def EdgeFeatureOutName(self):
        return self.OutDir + "/edgewise"
    
    
    def ExtractOneEdge(self,lvCol):
        print "extracting for edge [%s]" %(lvCol[0][0])
        
        EdgeFeature = EdgeFeatureC()
        EdgeFeature.edge = lvCol[0][0]
        hEdgeDomainFeature = self.ExtractEdgeDomainFeature(lvCol)
        hEdgeCntFeature = self.ExtractEdgeCntFeature(lvCol)
        hEdgeLvlFeature = self.ExtractEdgeLvlFeature(lvCol)
        
        EdgeFeature.AddFeature(dict(hEdgeDomainFeature.items() + hEdgeCntFeature.items()
                                    +hEdgeLvlFeature.items()))
        print "features: [%s]" %(EdgeFeature.dumps())
        return EdgeFeature
        
   
   
    def ExtractEdgeDomainFeature(self,lvCol):
        hFeature = {}
        edge = lvCol[0][0]
        EdgeDomain = GetDomain(edge)
        hFeature['EdgeDomain' + EdgeDomain] = 1
        return hFeature
        
    def ExtractEdgeLvlFeature(self,lvCol):
        hFeature = {}
        edge = lvCol[0][0]
        Lvl = len(edge.strip('/').split('/'))
        hFeature['EdgeLvl'] = Lvl      
        return hFeature
   
    def ExtractEdgeCntFeature(self,lvCol):
        hFeature = {}
        hFeature['EdgeCnt'] = math.log(len(lvCol))       
        return hFeature       
        
