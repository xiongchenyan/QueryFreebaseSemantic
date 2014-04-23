'''
Created on Apr 21, 2014
the base structure for edge feature
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from cxBase.base import *
from cxBase.FeatureBase import *

import json


class EdgeFeatureC(cxFeatureC):
    def Init(self):
        super(EdgeFeatureC,self).Init()
        self.edge = ""
        self.lDomain = []
        
        
        
    def dumps(self):
        return self.edge + '\t' + super(EdgeFeatureC,self).dumps()
    
    def loads(self,line):
        vCol = line.split('\t')
        self.edge = vCol[0]
        super(EdgeFeatureC,self).loads('\t'.join(vCol[1:]))
        return
    
    
    def __deepcopy__(self,memo):
        return EdgeFeatureC(self.dumps())
    
    
        
    
    
    