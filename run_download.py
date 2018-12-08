'''
Import required libraries
'''

import os
import sys
from caseolap.download import *
import json as json



'''
Input and output data file path
'''

DATA_DIR = './'
logFilePath = './log/download_log.txt'
download_config_file_path = './config/download_config.json'
ftp_config_file_path = './config/ftp_config.json'



'''
Start the download,verification and extraction process
'''
                   

if __name__ == '__main__':
    
    logfile = open(logFilePath, "w") 
    
    with open(download_config_file_path, 'r') as f1:
        download_config = json.load(f1)
    
    with open(ftp_config_file_path, 'r') as f2:
        ftp_config = json.load(f2)
    
    BASELINE_DIR = os.path.join(DATA_DIR, 'ftp.ncbi.nlm.nih.gov/pubmed/baseline/')
    UPDATE_FILES_DIR = os.path.join(DATA_DIR,'ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/')
    
    if not os.path.isdir(DATA_DIR):
        print("Directory not found:", DATA_DIR) 
        
        
    '''
    Start download ---------------------
    '''
    
    #download_pubmed(DATA_DIR,download_config,ftp_config,logfile)
    
    ''' 
    verify download -----------------
    '''
    
    check_all_md5_in_dir(BASELINE_DIR,logfile)
    check_all_md5_in_dir(UPDATE_FILES_DIR,logfile)
    
    '''
    Extract downloaded files --------------
    '''
    
    extract_all_gz_in_dir(BASELINE_DIR,logfile)
    extract_all_gz_in_dir(UPDATE_FILES_DIR,logfile)
    
    logfile.close()
    
    
    
    
    
    
    
    
    
    
    
