import json

def write_json_file(file, pathname):
    with open(pathname, 'w', encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    print("wrote to " + pathname)