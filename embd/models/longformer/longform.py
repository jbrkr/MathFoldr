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

with urllib.request.urlopen("https://github.com/ToposInstitute/nlab-corpus/blob/main/nlab_plain.json?raw=true") as url:
    nlab = json.loads(url.read().decode())


model = LongformerModel.from_pretrained('allenai/longformer-base-4096', gradient_checkpointing=True)

tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096',
    truncation=True,
    max_length=10,
    return_tensors="pt")
rems = []
long_f_emb = []
ct = 0
for i in nlab:
    if len(i['content']) > 4096:
        ab = {
        'id': ct,
        'title': i['title'],
        'content': i['content'][4096:]
        }
        rems.append(ab)
        i['content'] = i['content'][:4096]
    input_ids = torch.tensor(tokenizer.encode(i['content'])).unsqueeze(0)  # Batch size 1
    outputs = model(input_ids)
    last_hidden_states = outputs[0] 
    ab = {
        'id': ct,
        'title': i['title'],
        'tensor': last_hidden_states
    }
    long_f_emb.append(ab)
    ct += 1

for i in long_f_emb:
    query = cursor.mogrify('INSERT INTO embedding (document_id, abstraction, model, tensor) VALUES (%s, %s, %s, %s)', (i['paper_id'], 'document', 'specter', i['tensor'], ))
    cursor.execute(query)
    conn.commit()