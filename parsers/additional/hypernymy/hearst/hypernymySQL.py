import psycopg2

connection = psycopg2.connect(
    host="xxxxxxx",
    database="postgres",
    user="postgres",
    password="xxxxxxx",
)
#connection.autocommit = True
cur = connection.cursor()

query = "select sentence_text, doc_id, sentence_id from sentences;"


def sql_return_list(qry):
    cur.execute(qry)
    output = cur.fetchall()
    out_list = [list(j) for j in output]
    return out_list


sents = sql_return_list(query)


hyd = [{
        'document_id':int(i[1]),
        'sentence_id': i[2],
        'sentence_text': i[0],
        'hyp': hy_hearst.find_hyponyms(i[0])
    } for i in sents]

hypernyms = []
flat_hyp = [j for j in hyd if len(j['hyp']) > 0]
[hypernyms.append(k) for k in flat_hyp]
print("Finished " + i)
print("Hypernyms: " + str(len(hypernyms)))


tups = []
for i in hypernyms:
    doc_id = i['document_id']
    sent_id = i['sentence_id']
    sent_text = i['sentence_text'].replace(')','>').replace('(','<').replace('"','')
    for j in i['hyp']:
        hyp_sentence = j['sentence'].replace(')','>').replace('(','<')
        hearst_pattern = j['hearst_pattern'].replace(')','>').replace('(','<')
        hyponym = j['hyponym']
        hypernym = j['hypernym']
        
        hyp_sentence = hyp_sentence.replace(')','>').replace('(','<').replace('"','')
        hearst_pattern = hearst_pattern.replace(')','>').replace('(','<').replace('"','')
        hyponym = hyponym.replace('"','')
        hypernym = hypernym.replace('"','')
        
        
        #.replace('"','')
        
        
        hyList = (
            doc_id,
            sent_id,
            sent_text,
            hyp_sentence,
            hearst_pattern,
            hyponym,
            hypernym
            )
        tups.append(hyList)


prefix = "INSERT INTO hypernyms (document_id,sentence_id, sentence_text, hyp_sentence_text, hearst_pattern, hyponym, hypernym ) VALUES "
q = prefix + ', '.join([str(i).replace('"',"'") for i in tups])    + ';'
cur.execute(q)
connection.commit()