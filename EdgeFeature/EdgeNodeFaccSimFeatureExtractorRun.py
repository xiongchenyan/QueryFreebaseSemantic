'''
Created on Apr 23, 2014
run Edge Node Facc Sim feature
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from EdgeFeature.EdgeNodeFaccSimFeatureExtractor import *


import sys

if 2 != len(sys.argv):
    print "conf:"
    EdgeNodeFaccSimFeatureExtractorC.ShowConf()
    sys.exit()
    
    
Extractor = EdgeNodeFaccSimFeatureExtractorC(sys.argv[1])
Extractor.Extract(True)

print "finished"

