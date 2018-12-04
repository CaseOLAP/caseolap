# CaseOLAP :

CaseOLAP is a cloud computing platform for phrase-mining. specifically, for user-defined entity-category association. It has five major steps; 'downloading', 'parsing', 'indexing', 'entity count' and 'CaseOLAP score calculation'. There are mltiple steps in a single major step, which are based on user's interest in entity list and categories as well as data set being used. This pipeline describes these major steps for PubMed abstracts as text data, the mitochondrial proteins as entity list, and MeSH descriptors attached to abstracts as categories.


***1. Setting up Python environment*** : 

Install Anconda python and git in the Unix system. Creat the 'caseolap' python environment.

```
conda env create -f environment.yaml
```
---------------------------
***2. Download documents***

Set up the FTP data address at 'config/ftp_config.json' and select 'baseline' or 'updatefiles' in 'config/download_config.json'. This will download the data file from source to the cloud storage, check the integrity of download data, and extract them.

```
python run_download.py
```
-------------------------------

***3. Parsing Documents***
```
python run_parsing.py
```
---------------------------
***4. MeSH to PMID mapping***

```
python run_mesh2pmid_mapping.py

```
---------------------------
***5. Document Indexing***

```
python run_index_init.py
python run_populate_init.py
```
---------------------------
***6. Document Indexing***

```
python run_textcube.py
```
---------------------------
***7. Entity Count***

```
python run_entitycount.py
```
---------------------------
***8. Metadata Update***
```python run_metadata_update.py
```
---------------------------
***9. CaseOLAP score Calculation***

```
python run_caseolap_score.py
```








