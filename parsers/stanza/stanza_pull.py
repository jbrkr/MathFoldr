from tqdm import tqdm
import stanza
from read_file import read_json_file

### Load Model
stanza.download('en', processors='tokenize,pos, mwt, lemma, depparse, ner')

stanford_model = stanza.Pipeline('en', processors='tokenize,pos, mwt, lemma, depparse, ner')


### Route Model Outputs
def stanford(text):
    doc = stanford_model(text)
    return doc

def stanford_doc_props(doc):
    docDict = {}
    docDict['text'] = doc.text
    docDict['sentences'] = doc.sentences
    docDict['entities'] = doc.entities
    docDict['num_tokens'] = doc.num_tokens
    docDict['num_words'] = doc.num_words
    return docDict

def stanford_sent_props(sent):
    sentDict = {}
    sentDict['text'] = sent.text
    sentDict['entities'] = sent.entities
    sentDict['doc'] = sent.doc
    sentDict['dependencies'] = sent.dependencies
    sentDict['tokens'] = sent.tokens
    sentDict['words'] = sent.words
    sentDict['sentiment'] = sent.sentiment
    return sentDict

def stanford_token_props(token):
    tokenDict = {}
    tokenDict['text'] = token.text
    tokenDict['id'] = token.id
    tokenDict['words'] = token.words
    tokenDict['misc'] = token.misc
    tokenDict['start_char'] = token.start_char
    tokenDict['end_char'] = token.end_char
    tokenDict['ner'] = token.ner
    return tokenDict

def stanford_span_props(span):
    spanDict = {}
    spanDict['doc'] = span.doc
    spanDict['text'] = span.text
    spanDict['tokens'] = span.tokens
    spanDict['words'] = span.words
    spanDict['type'] = span.type
    spanDict['start_char'] = span.start_char
    spanDict['end_char'] = span.end_char
    return spanDict



### Read Corpus
link = '/work/nlab_plain.json'
read_file = read_json_file(link)


### Process and Write Outputs
ct = 0
st_outs = []
for i in read_file:
    one_doc = stanford(i['content'])
    st_outs.append(one_doc.to_dict())
    ct += 1
    if ct % 250 == 0:
        print(ct/len(read_file))
        iter_file_name = 'stanza_nlab_'+str(ct)+'.json'
    	with open(iter_file_name, 'w', encoding='utf-8') as f:
            json.dump(st_outs, f, ensure_ascii=False, indent=4)
    	st_outs = []







