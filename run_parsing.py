
import json
import sys
import os
import time
from caseolap.parsing import *
import traceback
from lxml import etree

'''
input data files
'''
DATA_DIR = './'
baseline_files = 'ftp.ncbi.nlm.nih.gov/pubmed/baseline'
update_files = 'ftp.ncbi.nlm.nih.gov/pubmed/updatefiles'
parsing_config_file = 'config/parsing_config.json'

'''
output data files 
'''
pubmed_output_file = './data/pubmed.json'
filestat_output_file = './data/filestat.json'
logFilePath = './log/parsing_log.txt'


'''
Start data parsing process --------------
'''
    

if __name__ == '__main__':
        
    t1 = time.time()

    with open(parsing_config_file,'r') as f:
        parsing_config = json.load(f)

    print(parsing_config)
    
    pubmed_output_file = open(pubmed_output_file, 'w')
    filestat_output_file = open(filestat_output_file, 'w')


    # Pars Baseline    
    parse_dir(os.path.join(DATA_DIR,baseline_files),\
              pubmed_output_file,filestat_output_file,\
              "baseline",parsing_config,logFilePath)
    
    # Pars Update Files
    parse_dir(os.path.join(DATA_DIR,update_files),\
              pubmed_output_file,filestat_output_file,\
              "updatefiles",parsing_config,logFilePath)
    
    
    pubmed_output_file.close()
    filestat_output_file.close()

    t2 = time.time()
    
    print("<><> Parsing finished, results dumped to %s <><>" % pubmed_output_file)
    print("<><> TOTAL TIME: %fs <><>" % (t2 - t1))
        
        
        
        
        
        
        