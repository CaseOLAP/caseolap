# CaseOLAP 

***1. Setting up Python environment*** : 

Install Anconda python and git in the Unix system. Creat the 'caseolap' python environment.

```
conda env create -f environment.yaml
```

***2. Download documents***

```
python run_download.py
```

***3. Parsing Documents***
```
python run_parsing.py
```

***4. MeSH to PMID mapping***

```
python run_mesh2pmid_mapping.py

```
***5. Document Indexing***

```
python run_index_init.py
python run_populate_init.py
```
***6. Document Indexing***

```
python run_textcube.py
```

***7. Entity Count***

```
python run_entitycount.py
```

***8. Metadata Update***
```python run_metadata_update.py
```

***9. CaseOLAP score Calculation***

```
python run_caseolap_score.py
```








