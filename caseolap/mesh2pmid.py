
import time
import re
import sys
import os
from collections import defaultdict
import json


class MeSH2PMID(object):
    
    
    def __init__(self):
        self.mesh2pmid = dict()
        self.mesh2pmid_stat = {}


    def mesh2pmid_mapping(self,parsed_data_inputfile, mesh2pmid_outputfile,logfile):
        
        mesh2pmid_fout = open(mesh2pmid_outputfile, "w")
        
        with open(parsed_data_inputfile, "r") as data_fin:

            start = time.time()
            k = 0
            
            print('MeSH to PMID mapping is running......')
            
            for line in data_fin: ## each line is single document
               
                    k = k+1
                    paperInfo = json.loads(line.strip())

                    data_dict = {}

                    '''
                    update PMID
                    '''
                    data_dict["pmid"] = paperInfo.get("PMID", "-1")
                    

                    '''
                    update MeSH Heading 
                    '''
                    data_dict["mesh_heading"] = " ".join(paperInfo["MeshHeadingList"])
                    

                    '''
                    collect Mesh2PMID 
                    '''
                    if data_dict["pmid"] != "-1":
                        for mesh in paperInfo["MeshHeadingList"]:
                            if mesh not in self.mesh2pmid:
                                   self.mesh2pmid[mesh] = []
                            self.mesh2pmid[mesh].append(data_dict["pmid"])

                    if k%500000 == 0:
                        print(k,' MeSH mapping done!')
                        logfile.write("Total" + str(k) +' MeSH to PMID mapping done!')
                        logfile.write("\n")
                    


            '''
            Dumping mapping table
            '''
            for key,value in self.mesh2pmid.items():
                json.dump({key:value}, mesh2pmid_fout)
                mesh2pmid_fout.write('\n')

            mesh2pmid = dict()

            end = time.time()
            print("Finish MeSH to PMID mapping. Total escaped time %s (seconds) " % (end - start) )
            
            
    def mesh2pmid_mapping_stat(self, mesh2pmid_statfile,logfile): 
        
        print('MeSH to PMID mapping stat is running......')
        logfile.write('MeSH to PMID mapping stat is running......')
        logfile.write("\n")
        
        
        
        for key,value in self.mesh2pmid.items():
            self.mesh2pmid_stat[key] = len(value)
            
        with open(mesh2pmid_statfile,'w') as fstat:
            json.dump(self.mesh2pmid_stat,fstat)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
