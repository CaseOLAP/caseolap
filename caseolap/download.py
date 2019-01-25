

import os
import sys
import re
import time
import subprocess

'''
Download function downloads PubMed data =============================
'''
def download_pubmed(DATA_DIR,download_config,ftp_config,logfile):
        
        '''
        Downloading baseline files
        '''
        t1 = time.time()
        if download_config['baseline']:
            print('downloading baseline files. For detail look download logfile....')
            rc = os.system(str('wget -q -r --directory-prefix=%s --no-parent '+ ftp_config['baseline']) % DATA_DIR)
            if rc != 0:
                logfile.write("Return code of downloading pubmed baseline files via wget is %d, not zero." % rc)
                logfile.write("\n")
                logfile.write("Link: " + ftp_config['baseline'])
                logfile.write("\n")
                exit(rc)
            t2 = time.time()
            '''
            Report progress ------------
            '''
            print("Finished downloading PubMed baseline files. %fs" % (t2 - t1))
            print("Start downloading PubMed updatefiles.",ftp_config['update'])
            logfile.write("Finish downloading PubMed baseline files. %fs" % (t2 - t1))
            logfile.write("\n")
            logfile.write("Start downloading PubMed updatefiles......")
            logfile.write("\n")
            
        else:
            t2 = time.time()
        '''
        Downloading updatefiles files
        ''' 
        if download_config['update']:
            print('downloading update files. For detail look download logfile....')
            rc = os.system(str("wget -q -r --directory-prefix=%s --no-parent "+ ftp_config['update']) % DATA_DIR)
    
            if rc != 0:
                logfile.write("Return code of downloading PubMed update files via wget is %d, not zero." % rc)
                logfile.write("\n")
                logfile.write("Link: " + ftp_config['update'])
                logfile.write("\n")
                exit(rc)
            t3 = time.time()
            '''
            report progress ------------
            '''
            logfile.write("Finished downloading PubMed update files. %fs" % (t3 - t2))
            logfile.write("\n")
            print("Finished downloading PubMed update files. %fs" % (t3 - t2))
       
        
        
'''
MD5-checksum =============================
'''
            
def check_all_md5_in_dir(dir,logfile):
        
        if os.system("which md5sum 1>/dev/null") != 0:
            print("md5sum not found")           
            # Continue executing
            return

        count = 0
        print("==== Start checking md5 in %s ====" % dir)
        logfile.write("==== Start checking md5 in %s ====" % dir)
        
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if re.search('^medline17n\d\d\d\d.xml.gz$', file):
                    count += 1
                    check_md5(os.path.join(dir, file))
                    if count % 100 == 0:
                        print("%d files checked" % count)
            print("==== All md5 check succeeded (%d files) ====" % count)
            logfile.write("==== All md5 check succeeded (%d files) ====" % count) 
            logfile.write("\n")
        else:
            print("Directory not found: %s (for md5 check)" % dir)
            logfile.write("==== All md5 check succeeded (%d files) ====" % count) 
            logfile.write("\n")
        
        

def check_md5(file):
    if os.path.isfile(file) and os.path.isfile(file + ".md5"):

        # Work only on Linux, user "md5" for Mac
        stdout = subprocess.check_output("md5sum %s" % file, shell=True).decode('utf-8')

        md5_calculated = re.search('[0-9a-f]{32}', stdout).group(0)
        md5 = re.search('[0-9a-f]{32}', open(file + ".md5", 'r').readline()).group(0)

        if md5 != md5_calculated:
            print("Error: md5 check failed for file %s" % file)
            exit(1)
            
'''
Data extraction =================================
'''

 # Assume filename is *.gz
def extract(file,logfile):
    rc = os.system('gunzip -fqk %s' % file)
    if rc != 0:
        
        print("gunzip return code for file %s is %d, not zero" % (file, rc))
        logfile.write("gunzip return code for file %s is %d, not zero" % (file, rc))
        logfile.write("\n")
        
        exit(rc)
    return rc

def extract_all_gz_in_dir(dir,logfile):
        if os.path.isdir(dir):
            count = 0
            print("==== Start extracting in %s ====" % dir)
            t1 = time.time()
            for file in os.listdir(dir):
                if re.search('.*\.gz$', file):
                    extract(os.path.join(dir, file),logfile)
                    count += 1
                if count % 50 == 0:
                    
                    print("%d files extracted, %fs taken so far" % (count, time.time() - t1))
                    logfile.write("%d files extracted, %fs taken so far" % (count, time.time() - t1))
                    logfile.write("\n")
                    
                    
            print("==== All files extracted (%d files). Total time: %fs ====" % (count, time.time() - t1))
        else:
            print("Directory not found: %s (for extraction)" % dir)      
        
          
    
