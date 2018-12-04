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
