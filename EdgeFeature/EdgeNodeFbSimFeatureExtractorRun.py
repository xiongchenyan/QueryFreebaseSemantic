'''
Created on Apr 22, 2014
run node fb dump sim feature extraction
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from EdgeFeature.EdgeNodeFbSimFeatureExtractor import *


import sys

if 2 != len(sys.argv):
    print "conf:"
    EdgeNodeFbSimFeatureExtractorC.ShowConf()
    sys.exit()
    
    
Extractor = EdgeNodeFbSimFeatureExtractorC(sys.argv[1])
Extractor.Extract(True)

print "finished"
