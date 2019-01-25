import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from collections import Counter
from caseolap.entitycount import *


'''
Input data directory
'''
input_file_textcube_pmid2cell = "./data/textcube_pmid2cell.json"
input_file_user_entity_list = "./input/entities.txt"

'''
output data directory
'''
output_file_entity_count = "./data/entitycount.txt"
output_file_entityfound_pmid2cell = "./data/entityfound_pmid2cell.txt"
logFilePath = "./log/entitycount_log.txt"


'''
Run the Entity Count Operation
'''

    
if __name__ == '__main__':

    logfile = open(logFilePath, 'w')
        
        
    EC = EntityCount()

    '''
    Prepare the intity dictionary
    '''
    EC.entity_dictionary(input_file_user_entity_list,logfile)

    '''
    Prepare documents in text-cube cell and entity_count bucket
    '''
    EC.entity_count_dictionary(input_file_textcube_pmid2cell,logfile)

    '''
    count the entity
    '''
    EC.entity_search(logfile)

    '''
    Save the entity count output
    '''
    EC.entity_count_output(output_file_entity_count,output_file_entityfound_pmid2cell,logfile)

    logfile.close()


