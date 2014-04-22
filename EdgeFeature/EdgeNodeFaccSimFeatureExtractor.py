'''
Created on Apr 22, 2014
extract node facc sim feature
group 3:
    facc sim feature:
        Avg obj a, b co-doc cnt
        Avg obj a, b, co-doc with in window        
@author: cx
'''



'''
input: edge obj obj, facc dir
do:
    read edge-obj-obj
        keep a structure:
            obj-obj -> edge name
    traverse facc data ( via a facc data reader in GoogleAPI)
        for each pair in a clueweb doc:
        keep and update two dict:
            edge-> obj pair co-doc cnt
            edge -> obj pair co-doc with in window cnt


'''
