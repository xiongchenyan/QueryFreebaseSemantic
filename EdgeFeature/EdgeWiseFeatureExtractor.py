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
class EdgeWiseFeatureExtractorC(EdgeFeatureExtractorC):
    



    def EdgeFeatureOutName(self):
        return self.OutDir + "/edgewise"
    
    
    def ExtractOneEdge(self,lvCol):
        EdgeFeature = EdgeFeatureC()
        EdgeFeature.edge = lvCol[0][0]
        hEdgeDomainFeature = self.ExtractEdgeDomainFeature(lvCol)
        hEdgeCntFeature = self.ExtractEdgeCntFeature(lvCol)
        hEdgeLvlFeature = self.ExtractEdgeLvlFeature(lvCol)
        
        EdgeFeature.AddFeature(dict(hEdgeDomainFeature.items() + hEdgeCntFeature.items()
                                    +hEdgeLvlFeature.items()))
        
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
        hFeature['EdgeCnt'] = len(lvCol)       
        return hFeature       
        
