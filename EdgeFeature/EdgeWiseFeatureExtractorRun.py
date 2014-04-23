'''
Created on Apr 22, 2014
run edge wise feature extraction
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
from EdgeWiseFeatureExtractor import *
import sys

if 2 != len(sys.argv):
    print "conf:"
    EdgeWiseFeatureExtractorC.ShowConf()
    sys.exit()
    
    
Extractor = EdgeWiseFeatureExtractorC(sys.argv[1])
Extractor.Extract(True)

print "finished"
