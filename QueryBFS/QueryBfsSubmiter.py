'''
Created on Apr 8, 2014
submit job as query bfs for each query
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from CrossValidation.CVJobSubmiter import *
import ntpath




class BfsQueryFreebaseSubmiterC(CVJobSubmiterC):
    
    def InitCollectRes(self):
        #sub class will collect and set data sources here
        print "unsupervised train folds, nothing to collect"
        return True
    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        conf = deepcopy(self.ConfBase)
        
        #to set fields:
            #in = train
            #paraset = paraname
            #evaoutdir = eval/fold_para_eval/
        
        conf.SetConf('in',FName[1])
        FoldIndex = self.Namer.SplitFoldId(FName[0])
        conf.SetConf('workdir',self.ConfBase.GetConf('workdir') + "/%d" %(FoldIndex) )
        return conf
    
    
    
    
    
def BfsQueryFreebaseSubmiterCUnitRun(ConfIn):
    Submiter = BfsQueryFreebaseSubmiterC(ConfIn)
    Submiter.Process()    
    return True


import sys

if 2 != len(sys.argv):
    print "1 para: a submiter conf"
    BfsQueryFreebaseSubmiterC.ShowConf()
    sys.exit()
    
BfsQueryFreebaseSubmiterCUnitRun(sys.argv[1])
print "finished"