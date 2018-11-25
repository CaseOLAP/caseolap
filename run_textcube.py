import json
import sys
import time
from caseolap.textcube import *


'''
input data directories
'''
input_file_meshtree = "./input/mtrees2018.bin"  
input_file_mesh2pmid = "./data/mesh2pmid.json"
input_file_root_cat = './input/categories.txt'  
input_file_textcube_config = './config/textcube_config.json'  


'''
output data directories
'''
output_file_textcube_pmid2cell = './data/textcube_pmid2cell.json'
output_file_textcube_cell2pmid = './data/textcube_cell2pmid.json'
output_file_textcube_stat = './data/textcube_stat.txt'
outputfile_MeSHterms_percat = './data/meshterms_per_cat.json'



'''
Start Construction of Text - Cube
'''
    
if __name__ == '__main__':

    
    with open(input_file_textcube_config, "r") as f_config:
            cell_names = json.load(f_config)
    
    print("there are ", len(cell_names), "cells in the text cube!")
    
    """
    This class build TextCube
    """
    TC =  TextCube(cell_names)

    """
    Collect all decendent MeSH terms for each categories
    """
    TC.descendent_MeSH(input_file_root_cat,\
                       input_file_meshtree,\
                       outputfile_MeSHterms_percat)

    """
    Collect all PMID falling under cells of TextCube
    """
    TC.cell2pmids_mapping(input_file_mesh2pmid,\
                          output_file_textcube_cell2pmid)


    """
    Collect all categories assigned to each PMIDS
    """
    TC.pmid2cell_mapping(output_file_textcube_pmid2cell)


    """
    Collect statistics of Textcube
    """
    TC.cell_statistics(output_file_textcube_stat)




