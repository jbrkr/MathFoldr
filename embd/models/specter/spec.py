import urllib.request, json 

from transformers import LongformerModel, LongformerTokenizer
import torch
import psycopg2
 
conn = psycopg2.connect(
    host="xxxxxxx",
    database="postgres",
    user="postgres",
    password="xxxxxxx",
)
#connection.autocommit = True
cursor = conn.cursor()

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

from typing import Dict, List
import json

import requests


URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16


def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    """Splits a longer list to respect batch size"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


SAMPLE_PAPERS = [
    {
        "paper_id": "A",
        "title": "Angiotensin-converting enzyme 2 is a functional receptor for the SARS coronavirus",
        "abstract": "Spike (S) proteins of coronaviruses ...",
    },
    {
        "paper_id": "B",
        "title": "Hospital outbreak of Middle East respiratory syndrome coronavirus",
        "abstract": "Between April 1 and May 23, 2013, a total of 23 cases of MERS-CoV ...",
    },
]
SAMPLE_PAPERS = spnl

def embed(papers):
    embeddings_by_paper_id: Dict[str, List[float]] = {}

    for chunk in chunks(papers):
        # Allow Python requests to convert the data above to JSON
        response = requests.post(URL, json=chunk)

        if response.status_code != 200:
            raise RuntimeError("Sorry, something went wrong, please try later!")

        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]

    return embeddings_by_paper_id




with urllib.request.urlopen("https://github.com/ToposInstitute/nlab-corpus/blob/main/nlab_plain.json?raw=true") as url:
    nlab = json.loads(url.read().decode())


sentences = [i['content'] for i in nlab]
spnl = []
ct = 0
for i in nlab:
     
    a = {
        "paper_id": str(ct),
        "title": i["title"],
        "abstract": i['content'],
    }
    spnl.append(a)
    ct+=1
# Tokenize sentences  



emb_list_specter = []
start = 0
for i in range(729):
    
    end = start + 16
    section = spnl[start:end]
    all_embeddings = embed(section)
    emb_list_specter.append(all_embeddings)
    start += 16

ct = 0
for i in emb_list_specter:
    for j in range(len(i)):
        ab = list(i.values())[j]
        spnl[ct]['tensor'] = ab
        ct += 1

for i in spnl:
    query = cursor.mogrify('INSERT INTO embedding (document_id, abstraction, model, tensor) VALUES (%s, %s, %s, %s)', (i['paper_id'], 'document', 'specter', i['tensor'], ))
    cursor.execute(query)
    conn.commit()