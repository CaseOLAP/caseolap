import json


class MetadataUpdate():
    
    
    def __init__(self, cell_names):
        
            self.cell_names = cell_names
            self.pmid2pcount = dict()
            self.cell2pmids = {}         
            

    def pmid2phrase_update(self,input_file_entitycount,\
                           output_file_pmid2pcount,\
                           logfile):
        
        print("PMID to entity count count dictionary is being updated.....")
        logfile.write("PMID to entity count dictionary is being updated.....\n")
        logfile.write("================================================== \n")
    
        '''PMID to Entity count Dictionary'''
        with open(input_file_entitycount) as f1:
            for line in f1:
                item = line.split()
                pmid = item[0]
                if len(item)>1:
                    prot_freq = {}
                    for pf in item[1:]:
                        pfs = pf.split('|')
                        if len(pfs)>1:
                            prot_freq.update({pfs[0]:pfs[1]})
                            self.pmid2pcount.update({pmid:prot_freq})
                            
                logfile.write("PMID: " + str(pmid) + " Entities count : " + str(prot_freq))
                logfile.write("\n")


        with open(output_file_pmid2pcount, 'w') as fp:
                        json.dump(self.pmid2pcount, fp)
                
                


    def cell2pmid_update(self,input_file_textcube_pmid2cell,\
                         output_file_metadata_cell2pmids,\
                         logfile):
        
        print("Cell to PMID is updated for entity found PMIDS....")
        logfile.write("Cell to PMID is updated for entity found PMIDS.... \n")
        logfile.write("================================================== \n")
     
        for name in self.cell_names:
                self.cell2pmids[name] = []
        
        '''PMID to Category Dictionary'''
        with open(input_file_textcube_pmid2cell) as f2:
            pmid2cell = json.load(f2)
            for item in pmid2cell:
                if item[0] != 'doc_id':
                    if str(item[0]) in  self.pmid2pcount.keys():
                        for i,name in enumerate(self.cell_names):
                            if str(item[1]) == str(i):
                                self.cell2pmids[name].append(item[0])
                                
        for name in self.cell_names:                       
            logfile.write("Cell : " + name + " includes" + str(len(self.cell2pmids[name])) + " documents.")
            logfile.write("\n")

        with open(output_file_metadata_cell2pmids, 'w') as fc:
                        json.dump(self.cell2pmids, fc)       


