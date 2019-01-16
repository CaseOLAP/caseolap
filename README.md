# CaseOLAP :

CaseOLAP is a cloud computing platform for phrase-mining. specifically, for user-defined entity-category association. It has five major steps; 'downloading', 'parsing', 'indexing', 'entity count' and 'CaseOLAP score calculation'. There are mltiple steps in a single major step, which are based on user's interest in entity list and categories as well as data set being used. This pipeline describes these major steps for PubMed abstracts as text data, the mitochondrial proteins as entity list, and MeSH descriptors attached to abstracts as categories.

### Publication: [Cloud-Based Phrase Mining and Analysis of User-Defined Phrase-Category Association in Biomedical Publications](https://www.jove.com/video/59108/cloud-based-phrase-mining-analysis-user-defined-phrase-category)


***1. Setting up Python Environment*** : 

Install Anconda python and git in the Unix system. Creat the 'caseolap' python environment.

```
conda env create -f environment.yaml
```
---------------------------
***2. Download Documents*** : 

Set up the FTP data address at 'config/ftp_config.json' and select 'baseline' or 'updatefiles' in 'config/download_config.json'. This will download the data file from source to the cloud storage, check the integrity of download data, and extract them.

```
python run_download.py
```
-------------------------------

***3. Parsing Documents*** : 
Set up the parameters for parsing at 'config/parsing_config.json'. Based on the items selected. Parsed data for each document becomes available as JSON dictionary.
```
python run_parsing.py
```
---------------------------
***4. MeSH to PMID Mapping***

Create a mapping table for each MeSH term. There are multiple MeSH attached to a single document.

```
python run_mesh2pmid_mapping.py

```
---------------------------
***5. Document Indexing***
Create a Elasticsearch indexing database for parsed documents. To initiate the index select the parameters in 'config/indrx_init.json' and to populate the index, select parameters at 'config/index_populate.json'.

```
python run_index_init.py
python run_populate_init.py
```
---------------------------
***6. Text-Cube Creation***: 

 Create a user-defined categories at 'input/categories.txt'. Create a data-cube for text data (i.e. a text-cube) for making text-data more functional for information extraction and manipulation.
 
```
python run_textcube.py
```
---------------------------
***7. Entity Count***
Create a user-defined entities in 'input/entities.txt'. Use Elasticsearch indexing database to search and count entities and documents including such entities.

```
python run_entitycount.py
```
---------------------------
***8. Metadata Update***

Update the metadata for Textcube from entity-count result.

```
python run_metadata_update.py

```
---------------------------
***9. CaseOLAP score Calculation***

Create the CaseOLAP score based on entity count and document count data using ```Integrity```, ```Popularity``` and ```Distintiveness```.

```
python run_caseolap_score.py
```








