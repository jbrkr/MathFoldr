import pandas as pd
import json
json_to_dict = lambda filename : json.load(open(filename,))

nlabDir_path = '/Volumes/dec15/7_9/down/stanza_nlab_out/'

stanzafilenames = []
for i in range(40):
    ct = (1+i)*25
    output_path = nlabDir_path + 'stanza_nlab_'+ str(ct) + '0.json'
    
    stanzafilenames.append(output_path)
    
    file = json_to_dict(stanzafilenames[i])
    print(output_path)
    for documentCt in range(len(file)):
        currDocument = file[documentCt]
        overallDocCount = (ct-25)*10+documentCt
        for sentenceCt in range(len(currDocument)):
            currSentence = currDocument[sentenceCt]
            for token in currSentence:
                token['document_id'] = overallDocCount
                token['sentence_id'] = sentenceCt                
            if overallDocCount == 0:
                stanzaDF = pd.DataFrame(currSentence)
            else: 
                currSentenceDf = pd.DataFrame(currSentence)
                stanzaDF = stanzaDF.append(currSentenceDf)

    stanzaDF['model'] = 'stanza'
    stanzaDF['dataset'] = 'nLab'

    file_name = 'stanza_nlab_wordlevel_'+str(ct)+'.csv'
    stanzaDF.to_csv(file_name, sep='\t')
    stanzaDF = []
    currSentenceDf = []