'''
Created on Apr 21, 2014
fetch target edge's occurance
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')


import sys
from cxBase.base import cxConf,cxBaseC
from FreebaseDump.FbDumpBasic   import *
from FreebaseDump.FbDumpReader import *
import pickle
import json

class EdgeOccurFetcherC(cxBaseC):
    def Init(self):
        self.hTargetEdge = {}
        self.TargetEdgePath = ""
        self.DumpIn = ""
        self.OutName = ""
    
    @staticmethod
    def ShowConf():
        print "targetedgein\ndumpin\nout"
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.TargetEdgePath = conf.GetConf('targetedgein')
        self.DumpIn = conf.GetConf('dumpin')
        self.OutName = conf.GetConf('out')
        
        EdgeIn = open(self.TargetEdgePath)
        self.hTargetEdge = pickle.load(EdgeIn)
        print "load [%d] target edge" %(len(self.hTargetEdge))
        return True
    
    
    
    
    def Process(self):
        
        FbDumpReader = FbDumpReaderC()
        FbDumpReader.open(self.DumpIn)
        
        
        out = open(self.OutName,'w')
        cnt = 0
        EdgeCnt = 0
        for lvCol in FbDumpReader:
#             print "read obj dump str:"
#             print json.dumps(lvCol)
#             print "-------------------\n"
            
            
            for vCol in lvCol:
                
                if vCol[1] in self.hTargetEdge:
                    print "get target edge [%s]" %(vCol[1])
                    ObjA = GetId(vCol[0])
                    ObjB = GetId(vCol[2])
                    if ("" != ObjA) & ("" != ObjB):
                        print >>out, vCol[1] + "\t" + ObjA + "\t" + ObjB
                        EdgeCnt += 1
#                 else:
#                     print "edge [%s] not needed" %(vCol[1])
                        
            cnt += 1
            if 0 == cnt % 100000:
                print "processed [%d] line [%d] target triple get" %(cnt,EdgeCnt)
                        
        out.close()
        return True
                        





if 2 != len(sys.argv):
    print "get edge occur in gzip dump\n 1 para conf\n"
    EdgeOccurFetcherC.ShowConf()
    sys.exit()
    
    
Fetcher = EdgeOccurFetcherC(sys.argv[1])
Fetcher.Process()

print "finished"



