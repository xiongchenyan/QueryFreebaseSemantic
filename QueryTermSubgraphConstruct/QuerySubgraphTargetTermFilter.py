'''
Created on May 13, 2014
filter out subgraph that does not connected to given target (candidate) terms
input: llExpTerm, graph dir,
do: for each lExpTerm
    locate its graph name (_%d qid)
    read,
    reverse graph,
    match start nodes (candidate terms)
    dfs for path that lead to query in 4 hop (term->obj->obj->obj->q)
        mark edge in these path as useful
    discard non-useful paths
    reverse back
output: a cleaned graph

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib/')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI/')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')


from cxBase.base import cxConf,cxBaseC
from GraphBase.base import NodeC,GraphC
from GraphBase.DFSer import DFSerC


from base.ExpTerm import *


class QuerySubgraphTargetTermFilterC(DFSerC):
    def Init(self):
        super(QuerySubgraphTargetTermFilterC,self).Init()
        self.GraphDumpDir = ""
        self.OutDir = ""
        
    @staticmethod
    def ShowConf():
        print "graphdumpdir\noutdir"
    def SetConf(self,ConfIn):
        super(QuerySubgraphTargetTermFilterC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.GraphDumpDir = conf.GetConf('graphdumpdir')
        self.OutDir = conf.GetConf('outdir')
        
        
    