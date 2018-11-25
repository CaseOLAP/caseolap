
from caseolap.mesh2pmid import *

'''
Input data directory
'''
parsed_data_inputfile = "./data/pubmed.json"


'''
Output data directory
'''
mesh2pmid_outputfile = "./data/mesh2pmid.json"
logFilePath = "./log/mesh2pmid_log.txt"
mesh2pmid_statfile = "./data/mesh2pmid_stat.json"



'''
Start MeSH to PMID mapping
'''
    
if __name__ == '__main__':
    
    '''
    Create MeSH to PMID mapping object
    '''
    mesh2PMID = MeSH2PMID()
    '''
    Create a MeSH to PMID mapping dictionary
    '''
    mesh2PMID.mesh2pmid_mapping(parsed_data_inputfile,mesh2pmid_outputfile,logFilePath)
    
    '''
    Create MeSH to PMID mapping statistics
    '''
    mesh2PMID.mesh2pmid_mapping_stat(mesh2pmid_statfile)
    
    
    
    
    

