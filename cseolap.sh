#!/usr/bin/env bash

python run_download.py &&

python run_parsing.py &&

python run_mesh2pmid.py &&

python run_index_init.py &&

python run_index_populate.py &&

python run_textcube.py &&

python run_entitycount.py &&

python run_metadata_update.py &&

python caseolap_score.py






