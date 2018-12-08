
import json

from caseolap.metadata_update import *


'''
Input file path
'''
input_file_entitycount = 'data/entitycount.txt'
input_file_textcube_pmid2cell = 'data/textcube_pmid2cell.json'
input_file_entityfound_pmid2cell = 'data/entityfound_pmid2cell.txt'

'''
output file path
'''
output_file_metadata_pmid2pcount = 'data/metadata_pmid2pcount.json'
output_file_metadata_cell2pmids = 'data/metadata_cell2pmids.json'
logFilePath = "./log/metadata_updata_log.txt"




if __name__ == '__main__':
    
    logfile = open(logFilePath, "w") 
    
    with open("./config/textcube_config.json",'r') as f:
        cell_names = json.load(f) 


    '''
    Initiate metadata update class
    '''
    MU = MetadataUpdate(cell_names)


   
    '''
    Update PMID to phrase count
    '''
    MU.pmid2phrase_update(input_file_entitycount,\
                          output_file_metadata_pmid2pcount,\
                          logfile)


    '''
    Update  entity found cell to PMID
    '''
    MU.cell2pmid_update(input_file_textcube_pmid2cell,\
                        output_file_metadata_cell2pmids,\
                        logfile)    
    
    logfile.close()
