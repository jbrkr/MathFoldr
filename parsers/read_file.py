import time
import json

def read_json_file(path):
    print("Processing: " + path)
    t1 = time.time()
    with open(path) as f:
        data = json.load(f)
    t = time.time() - t1
    print(t)
    print() 
    return data