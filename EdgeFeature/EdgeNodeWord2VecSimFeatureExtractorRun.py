'''
Created on May 6, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from EdgeFeature.EdgeNodeWord2VecSimFeatureExtractor import *


import sys

if 2 != len(sys.argv):
    print "conf:"
    EdgeNodeWord2VecSimFeatureExtractorC.ShowConf()
    sys.exit()
    
    
Extractor = EdgeNodeWord2VecSimFeatureExtractorC(sys.argv[1])
Extractor.Extract(True)

print "finished"