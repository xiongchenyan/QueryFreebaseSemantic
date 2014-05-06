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
import math

class EdgeOccurFetcherC(cxBaseC):
    def Init(self):
        self.hTargetEdge = {}
        self.TargetEdgePath = ""
        self.DumpIn = ""
        self.OutName = ""
        self.MaxOccurPerEdge = 10000
    
    @staticmethod
    def ShowConf():
        print "targetedgein\ndumpin\nout\nmaxoccurperedge 10000"
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.TargetEdgePath = conf.GetConf('targetedgein')
        self.DumpIn = conf.GetConf('dumpin')
        self.OutName = conf.GetConf('out')
        self.MaxOccurPerEdge = int(conf.GetConf('maxoccurperedge',self.MaxOccurPerEdge))
        EdgeIn = open(self.TargetEdgePath)
        self.hTargetEdge = pickle.load(EdgeIn)
        print "load [%d] target edge" %(len(self.hTargetEdge))
        return True
    
    
    
    def GetAllInstanceObj(self,lvCol):
        lObj = []
        for vCol in lvCol:
            if len(lObj) >= math.sqrt(self.MaxOccurPerEdge):
                break
            if IsInstanceEdge(vCol[1]):
                ObjId = GetId(vCol[2])
                if "" != ObjId:
                    lObj.append(vCol[2])
        return lObj
                
        
        
    
    
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
                    if self.hTargetEdge[vCol[1]] >= self.MaxOccurPerEdge:
                        continue
                    print "get target edge [%s]" %(vCol[1])
                    ObjA = GetId(vCol[0])
                    ObjB = GetId(vCol[2])
                    if ("" != ObjA) & ("" != ObjB):
                        print >>out, vCol[1] + "\t" + ObjA + "\t" + ObjB
                        self.hTargetEdge[vCol[1]] += 1
                        EdgeCnt += 1
#                 else:
#                     print "edge [%s] not needed" %(vCol[1])
                        
                        
            #add: output instance occur of cotype/edge            
            
            
            if ('cotype' + lvCol[0][0]) in self.hTargetEdge:
                
                edge = 'cotype' + lvCol[0][0]
                if self.hTargetEdge[edge] >= self.MaxOccurPerEdge:
                    continue
                print "get target edge [%s]" %(edge)
                lObjId = self.GetAllInstanceObj(lvCol)
                for i in range(len(lObjId)):
                    for j in range(len(lObjId)):
                        if i == j:
                            continue
                        print >>out, edge + "\t" + lObjId[i] + "\t" + lObjId[j]
                        EdgeCnt += 1
                        self.hTargetEdge[edge] += 1
                        if self.hTargetEdge[edge] >= self.MaxOccurPerEdge:
                            break
                        
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



