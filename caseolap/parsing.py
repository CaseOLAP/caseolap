import re
import itertools
import json
import sys
import os
import time
import traceback
from lxml import etree



class Parser(object):
    
    '''Class to parse the documents'''
    def __init__(self,file,pubmed_output_file, filestat_output_file, parsing_config):
        
        #input
        self.file = file
        self.fname = file.split('/')[-1].split('.')[0]
        
        self.pubmed_output_file = pubmed_output_file
        self.filestat_output_file = filestat_output_file
        self.parsing_config = parsing_config
        
        
        # containers
        self.filestat = {}
        self.result = {}
        
        
        
    def get_text(self,element, tag):
        e = element.find(tag)
        if e is not None:
            return e.text
        else:
            return '' 
        
        
    def parse_author(self,authors):
        author_name = []
        for author in authors:
            item = {}
            item['LastName'] = self.get_text(author, 'LastName')
            item['ForeName'] = self.get_text(author, 'ForeName')
            item['Initials'] = self.get_text(author, 'Initials')
            item['Suffix'] = self.get_text(author, 'Suffix')
            item['CollectiveName'] = self.get_text(author, 'CollectiveName')
            author_name.append(item)
        return author_name
    
    
    def get_pmid(self,article):
        # PMID - Exactly One Occurrance
        pmid = self.get_text(article, './/PMID')
        self.result['PMID'] = pmid
        return pmid
    
    
        
    def get_title(self, article):
        # Article title - Zero or One Occurrences
        self.result['ArticleTitle'] = self.get_text(article, './/ArticleTitle')
            
            
        
    def get_abstract(self,article,pmid):
        # Abstract - Zero or One Occurrences
        abstractList = article.find('.//Abstract')
        if abstractList != None:
                try:
                    abstract = '\n'.join([line.text for line in abstractList.findall('AbstractText')])
                    self.result['Abstract'] = abstract
                except:
                    self.result['Abstract'] = ''
                
        else:
            self.result['Abstract'] = ''
           
            
            
    def get_publishing_date(self,journal):
        # # Publishing Date
        if self.parsing_config['date']:
            self.result['PubDate'] = {}
            self.result['PubDate']['Year'] = self.get_text(journal, './/JournalIssue/PubDate/Year')
            self.result['PubDate']['Month'] = self.get_text(journal, './/JournalIssue/PubDate/Month')
            self.result['PubDate']['Day'] = self.get_text(journal, './/JournalIssue/PubDate/Day')
            self.result['PubDate']['Season'] = self.get_text(journal, './/JournalIssue/PubDate/Season')
            self.result['PubDate']['MedlineDate'] = self.get_text(journal, './/JournalIssue/PubDate/MedlineDate')

        
        
        
    def get_MeSH(self,article,pmid):
        # MeshHeading - Zero or More Occurrences
        headings = article.findall('.//MeshHeading')
        self.result['MeshHeadingList'] = []
        if headings:
                for heading in headings:
                    descriptor_names = heading.findall('DescriptorName')
                    qualifier_names = heading.findall('QualifierName')
                    if descriptor_names:
                        for descriptor_name in descriptor_names:
                            self.result['MeshHeadingList'].append(descriptor_name.text)
                    if qualifier_names:
                        for qualifier_name in qualifier_names:
                            self.result['MeshHeadingList'].append(qualifier_name.text)
        
            
            
            
    def get_filestat(self,filepmids):
        u_filepmids = list(set(filepmids))
        n_files = len(u_filepmids)
        self.filestat.update({"fname":str(self.fname),\
                              "pmids":n_files})
        
    
    
    def parse_pubmed_file(self,logfile):
        
        sys.stdout.flush()
        t1 = time.time()
        f = open(self.file, 'r')
        tree = etree.parse(f)
        
        articles = itertools.chain(tree.findall('PubmedArticle'), tree.findall('BookDocument'))
        filepmids = []
        count_article = 0
        
        for article in articles:
                count_article += 1
                
                # PMID
                pmid = self.get_pmid(article)
                filepmids.append(pmid)
                
                #Title
                if self.parsing_config['title']:
                    self.get_title(article)
                    
                # Abstract    
                if self.parsing_config['abstract']:    
                    self.get_abstract(article,pmid)
                    
                # MeSH    
                if self.parsing_config['MeSH']:    
                    self.get_MeSH(article,pmid)
            
                
            
                # Author List - Zero or More Occurrences
                if self.parsing_config['author']:
                    authors = article.findall('.//Author')
                    self.result['AuthorList'] = self.parse_author(authors)
                
                
                # Journal - Exactly One Occurrance
                if self.parsing_config['journal']:
                    journal = article.find('.//Journal')
                    self.result['Journal'] = self.get_text(journal, 'Title')
                
                # Publishing Date
                if self.parsing_config['date']:
                    self.get_publishing_date(journal)
                
                # Country Published
                if self.parsing_config['location']:
                    country = article.find('.//MedlineJournalInfo')
                    self.result['Country'] = self.get_text(country, 'Country')
                    

                # Dump to pubmed json file <----------------------------
                json.dump(self.result, self.pubmed_output_file)
                self.pubmed_output_file.write('\n')
                
       
        self.get_filestat(filepmids)  
        # Dump to pubmed stat json file <----------------------------
        json.dump(self.filestat, self.filestat_output_file)
        self.filestat_output_file.write('\n')
        t2 = time.time()
        
        print('Parsing finished, total',count_article, "articles parsed. Total time:",(t2 - t1))
        logfile.write('Parsing finished, total :' + str(count_article) + " articles parsed. Total time: " + str(t2 - t1))
        logfile.write("\n")
        f.close()                          
        
        
def parse_dir(source_dir, pubmed_output_file, filestat_output_file,ndir,parsing_config,logfile):
    k = 0
    total_files = len(os.listdir(source_dir))
    print( ndir + ' parsing is running with total bulk files: ', total_files)
    print("======================================================================")
    logfile.write( ndir + ' parsing is running with total bulk files: '+ str(total_files))
    logfile.write("\n")
    logfile.write("======================================================================")
    logfile.write("\n")
        
    if os.path.isdir(source_dir):
            for file in os.listdir(source_dir):
                if re.search(r'^pubmed18n\d\d\d\d.xml$', file) is not None:
                    k = k +1        
                    print(k," th file out of ",total_files," from " + ndir+ ": ", file," is being parsed....") 
                    logfile.write(str(k)+ " th file out of "+ str(total_files) + \
                            " from " + ndir + ": "+ file + " is being parsed....")
                    logfile.write("\n")
                    
                    PRS = Parser(os.path.join(source_dir, file),\
                                pubmed_output_file,\
                                filestat_output_file,\
                                parsing_config)
                    
                    PRS.parse_pubmed_file(logfile) 
   
    
    
    
    
    
