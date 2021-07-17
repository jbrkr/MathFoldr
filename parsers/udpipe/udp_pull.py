import requests
import time
import ast
import json
from read_file import read_json_file


### Read Corpus
link = '/work/nlab_plain.json'

read_file = read_json_file(link)


### Process 
ct = 0

for i in read_file:
    input_data = i['content']
    files = {
        'data': (None, input_data),
        'model': (None, 'english'),
        'tokenizer': (None, ''),
        'tagger': (None, ''),
        'parser': (None, ''),
    }
    response = requests.post('http://lindat.mff.cuni.cz/services/udpipe/api/process', files=files)
    byte_str = response.content
    dict_str = byte_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    out = mydata['result']
    i['UD Results'] = out
    ct += 1
    if ct % 100 == 0:
        print(ct/len(read_file))

### Write Outputs
with open('UDPipe_nLab.json', 'w', encoding='utf-8') as f:
            json.dump(read_file, f, ensure_ascii=False, indent=4)