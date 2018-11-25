import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from collections import Counter


"""
Entity Count Class
"""

class EntityCount(object):
    
    def __init__(self,):
        
        self.entity_dict = {}
        
    


    def entity_dictionary(self,input_file_user_entity_list):
        print("Entity dictionary is created.......")
        with open(input_file_user_entity_list, "r") as f_in:
            for line in f_in:
                # synonums seperated by "|" and represented by the first one on each line
                line_split = line.strip().split("|")
                self.entity_dict[line_split[0]] = line_split
                
        #print(self.entity_dict)
        
    
    
    def entity_count_dictionary(self,input_file_textcube_pmid2cell):
        print("Entity count dictionary is initiated.......")
        with open(input_file_textcube_pmid2cell, "r") as f_in:
            self.pmid_and_cat = json.load(f_in)
        self.concerned_pmid_set = set(map(lambda x: x[0], self.pmid_and_cat))
        self.entity_count_per_pmid = {pmid: Counter() for pmid in self.concerned_pmid_set}
        

       
        
    def entity_search(self,logFilePath):    
        """
        Search and count entities: to optimize and find count from indexer
        """
        print("Entity count is running .....")
        
        logfile = open(logFilePath, 'w')
        
        es = Elasticsearch(timeout=300)
        k = 0
        
        for entity_rep in self.entity_dict:
            for entity in self.entity_dict[entity_rep]:

                #print(entity)
                
                #entity_space_sep = "".join(map(lambda x: " " if x == "_" else x, entity))
                entity_space_sep = entity.replace("_", " ")

                # s = Search(using=es, index="pmc_all_index").query("match", abstract=entity_space_sep)
                s = Search(using=es, index="xpubmed")\
                            .params(request_timeout=300)\
                            .query("match_phrase", abstract=entity_space_sep)
                
                #print("s")

                num_hits = 0
                num_valid_hits = 0
                num_counts = 0

                for hit in s.scan():
                    num_hits += 1
                    cur_pmid = str(hit.pmid)

                    if cur_pmid not in self.concerned_pmid_set:
                        continue

                    abs_lower = hit.abstract.lower().replace("-", " ")
                    entity_lower = entity_space_sep.lower().replace("-", " ")
                    entity_cnt = abs_lower.count(entity_lower)


                    if entity_cnt == 0:
                        #print ("----------", entity_space_sep, "----------")
                        #print (abs_lower)
                        continue

                    else:
                        self.entity_count_per_pmid[cur_pmid][entity_rep] += entity_cnt
                        num_valid_hits += 1
                        num_counts += entity_cnt

                        logfile.write(str(entity) + "# hits:" +  str(num_hits)+\
                                            "# valid hits:" + str( num_valid_hits) +\
                                            "# counts:"+ str(num_counts))
                        logfile.write("/n")
                
                
            k = k +1
            if k%10 == 0:
                print(k,'entity successfully counted!')
                logfile.write(str(k) + "entity successfully counted!")
                logfile.write("/n")

        
    
    
    def entity_count_output(self,output_file_entity_count,output_file_entityfound_pmid2cell):
        
        '''
        paper entity count & paper category
        '''
        print("Entity count outpput is being saved...")
        
        with open(output_file_entity_count, "w") as f_entity,\
                open(output_file_entityfound_pmid2cell , "w") as f_pmid2cell:

            f_pmid2cell.write("doc_id\tlabel_id\n")

            paper_new_id = 1

            for cur_pmid,cur_cat in self.pmid_and_cat:

                if len(self.entity_count_per_pmid[cur_pmid]) == 0:
                    continue


                '''
                print paper category
                '''
                f_pmid2cell.write(str(cur_pmid) + "\t" + str(cur_cat) + "\n")


                '''
                print paper entity count
                '''
                f_entity.write(str(cur_pmid))


                for entity in self.entity_count_per_pmid[cur_pmid]:
                    f_entity.write(" " + entity +"|" + str(self.entity_count_per_pmid[cur_pmid][entity]))


                f_entity.write("\n")


            paper_new_id += 1

        
