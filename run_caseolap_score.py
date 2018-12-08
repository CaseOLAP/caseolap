import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from caseolap.caseolap_score import *


'''
Input data directories
'''
inputfile_cell2pmids = './data/metadata_cell2pmids.json'
inputfile_pmid2pcount = './data/metadata_pmid2pcount.json'



'''
Output data path
'''
result_dir = "result/"
logFilePath = "./log/caseolap_score_log.txt"

if __name__ == '__main__':

    logfile = open(logFilePath, "w") 
    
    with open(inputfile_cell2pmids, 'r') as f:
        cell2pmids = json.load(f)
        
    with open(inputfile_pmid2pcount, 'r') as f:
        pmid2pcount = json.load(f)


    ### Test Run
    C = Caseolap(cell2pmids,pmid2pcount,result_dir,logfile)
    C.cell_pmids_collector(dump =True,verbose =True)
    #C.cell_pmids
    C.cell_pmid2pcount_collector()
    #C.cell_pmid2pcount
    C.all_protein_finder(dump =True,verbose = True)
    #C.all_proteins
    C.all_protein_finder()
    #C.all_proteins
    #C.cell_uniqp   
    C.cell_p2tf_finder()
    #C.cell_p2tf
    C.cell_tf_finder()
    #C.cell_tf
    C.cell_pop_finder(dump=True)
    #C.cell_pop
    C.cell_p2pmid_finder()
    #C.cell_p2pmid
    C.cell_ntf_finder()
    #C.cell_ntf
    C.cell_ndf_finder()
    #C.cell_ndf
    C.cell_rel_finder()
    #C.cell_rel
    C.cell_dist_finder(dump=True)
    #C.cell_dist
    C.cell_cseolap_finder(dump=True)
    #C.cell_caseolap
    logfile.close()