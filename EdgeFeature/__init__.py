'''
related to extract edge feature from Freebase

'''


'''
features to be extracted:
Group 1: Edge Frequency Feature
    Edge Frequency
    Edge Category
    Edge lvl in ontology
Group 2: Connected Object Freebase Similarity
    Average:
        Fraction of Same category Attributes in Two Objects
        \sum_obj 1(obj notable for edge category)
        tf-idf text sim (obj's desp) + text sim (obj's name)        
        
Group 3: Connected Object FACC Similarity
    Average:
        objects' co-occur in Facc
        object's co-occur in window
        term in between (too hard ,not now)
'''


'''
How to:
Group 1 is easy, single run => edge: feature#value
Group 2,3, two runs:
    first run:
        out: edge: obj-obj
    second run:
        load edge:obj-obj
        traverse Fb dump/FACC
    (for fb dump)
        check the # of obj in edge think about how to deal with it
    (for facc):
        update edge: obj-obj's information
'''



'''
thus:
1: output all required edge
2: output all edge's occurance in Fb dump, edge obj obj
    check the size of edge's
3: Feature extraction:
    Group 1: just by edge:obj-obj file
    Group 2,3: traverse dumps, record useful information
'''
