import json
import sys
import time


"""
This class build TextCube
"""
class TextCube(object):
    
    
    def __init__(self,cell_names):
        
        
        self.cell_names = cell_names
        self.concerned_cat = []
        self.pmid2cell = []
        
        
        
        
    """
    Collect all descendent MeSH terms for each root terms for a category
    """
    def descendent_MeSH(self,input_file_root_cat,input_file_meshtree,outputfile_MeSHterms_percat):
        
        print("descendent MeSH terms are being collected....")
        
        
        with open(input_file_root_cat, "r") as f_cat:
            for line in f_cat:
                self.concerned_cat.append(line.strip().split())
                
        self.num_cat = len(self.concerned_cat)
        
        self.MeSH_terms_per_cat = [set() for _ in range(self.num_cat)]
        with open(input_file_meshtree, "r") as f_tree:
            for line in f_tree:
                
                term_tree = line.strip().split(";")
                cur_term = term_tree[0]
                cur_tree = term_tree[1]

                for i in range(self.num_cat):
                    for cur_cat_tree in self.concerned_cat[i]:
                        if cur_cat_tree in cur_tree:
                            self.MeSH_terms_per_cat[i].add(cur_term)
                            
        
        MeSHset = []
        for item in self.MeSH_terms_per_cat:
            MeSHset.append(list(item))
        with open(outputfile_MeSHterms_percat, "w") as f_out:
            json.dump(MeSHset,f_out)

                    
    """
    Find corresponding papers for each category.
    """
    def cell2pmids_mapping(self,input_file_mesh2pmid,output_file_textcube_cell2pmid):
        
        print("Textcube cell to PMID mapping is being created....")
        self.cell2pmid = [set() for _ in range(len(self.cell_names))]
        with open(input_file_mesh2pmid, "r") as f_in:
            start = time.time()
            k = 0
            for line in f_in: 
                mesh2pmid = {}
                Info = json.loads(line.strip())
                for key,value in Info.items():
                    mesh2pmid.update({key:value})

                k = k+1
                if k%1000 ==0:
                    print(k,'MeSH analysed for textcube...!')

                for i in range(self.num_cat):
                    for cur_term in self.MeSH_terms_per_cat[i]:
                        if cur_term == key:
                            self.cell2pmid[i] = self.cell2pmid[i] | set(mesh2pmid[cur_term]) 
                            
        Cell2PMID = []
        for item in self.cell2pmid:
            Cell2PMID.append(list(item))
        with open(output_file_textcube_cell2pmid, "w") as f_out:
            json.dump(Cell2PMID, f_out)
            
            
            
                    
    """
    Serialize papers
    """
    def pmid2cell_mapping(self,output_file_textcube_pmid2cell):
        
        print("Textcube PMID to cell mapping is being created....")
        
        for i in range(self.num_cat):
            for cur_pmid in self.cell2pmid[i]:
                self.pmid2cell.append([cur_pmid, i])

        with open(output_file_textcube_pmid2cell, "w") as f_out:
            json.dump(self.pmid2cell, f_out)
            


    """
    Print cell statistics
    """
    def cell_statistics(self,output_file_textcube_stat): 
        
        print("Textcube cell statistics is being created....")
        
        with open(output_file_textcube_stat, "w") as f_stat:
            allpmid = [] 
            cell_count = [0 for i in range(self.num_cat)]
            for item in self.pmid2cell:
                allpmid.append(item[0])
                for i in range(self.num_cat):
                    if item[1] == i:
                        cell_count[i] += 1

            print('total pmids selected in class 1,2,3,4 and total is : ',\
                  cell_count,len(set(allpmid)))

            f_stat.write('total pmids selected in class 1,2,3,4 and total is : '
                   + str(cell_count) + " and  " + str(len(set(allpmid))))  


