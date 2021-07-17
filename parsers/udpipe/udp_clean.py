
import json
json_to_dict = lambda filename : json.load(open(filename,))

udp_path = '/Volumes/dec15/7_9/down/UDPipe_nLab.json'

udp = json_to_dict(udp_path)
u_pt = list(udp)



post_process_udp = []
post_process_udp_doc = {}
for document in u_pt:
    processed_dict = {}
    udp_raw = document['UD Results']
    udp_split = re.split('\n#|\n1|\n2|\n3|\n4|\n5|\n6|\n7|\n8|\n9',udp_raw)
    processed_dict['meta'] = udp_split[:3]
    udp_content = udp_split[5:]
    
    sent_section_dict_list = []
    sent_section_dict = {}
    sent_section_sublist = []
    for j in range(len(udp_content)):
        currLine = udp_content[j]
        if currLine[:10] == ' sent_id =':
            sent_section_dict['table_data'] = sent_section_sublist
            sent_section_dict_list.append(sent_section_dict)
            sent_section_dict = {}
            sent_section_sublist = []
            sent_section_dict['sent_id'] = int(currLine[10:])
        elif currLine[:7] == ' text =':
            sent_section_dict['text'] = currLine[7:]
        elif currLine == ' newpar':
             # Append Previous to list
            sent_section_dict['table_data'] = sent_section_sublist
            sent_section_dict_list.append(sent_section_dict)
            sent_section_dict = {}
            sent_section_sublist = []
        else:
            table_data_section = re.split('\t',currLine)
            sent_section_sublist.append(table_data_section)
    
    sent_section_dict['table_data'] = sent_section_sublist
    sent_section_dict_list.append(sent_section_dict)
    
    processed_dict['sentence_parse'] = sent_section_dict_list
    
    post_process_udp_doc['title'] = document['title']
    
    post_process_udp_doc['UD Processed'] = processed_dict
    
    post_process_udp.append(post_process_udp_doc)
    post_process_udp_doc = {}




lenlist = []
tableList = []
for k in post_process_udp:
    gg = k['UD Processed']['sentence_parse']
    for i in gg:
        tables= i['table_data']
        for j in tables:
            tableRow = [
                k['title'],
                i['sent_id'],
                i['text']]+j
            
            lenlist.append(len(j))
            tableList.append(tableRow)




import pandas as pd
 
# Create the pandas DataFrame
ud_df = pd.DataFrame(tableList, columns = ['doc_title', 'sent_id', 'text', '_gap_1', 
                                           'form', 'lemma','upostag',
                                           'xpostag','feats','head',
                                           'deprel', '_gap_2', '_gap_3'])
 


file_name = 'udpipe2_nlab_wordlevel.csv'
ud_df.to_csv(file_name, sep='\t')





import json
with open('ud_parsed_data.json', 'w', encoding='utf-8') as f:
    json.dump(post_process_udp, f, ensure_ascii=False, indent=4)            