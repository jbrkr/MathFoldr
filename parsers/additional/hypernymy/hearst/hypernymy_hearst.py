import re
import nltk
from nltk.tag import PerceptronTagger
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
import itertools
chunk_patterns=r'''NP:{<DT>?<JJ.*>*<NN.*>+}
                      {<NN.*>+}
                '''


h = [ (
                '(NP_\\w+ (, )?such as (NP_\\w+ ?(, )?(and |or )?)+)',
                'first'
            ),
            (
                '(such NP_\\w+ (, )?as (NP_\\w+ ?(, )?(and |or )?)+)',
                'first'
            ),
            (
                '((NP_\\w+ ?(, )?)+(and |or )?other NP_\\w+)',
                'last'
            ),
            (
                '(NP_\\w+ (, )?include (NP_\\w+ ?(, )?(and |or )?)+)',
                'first'
            ),
            (
                '(NP_\\w+ (, )?especially (NP_\\w+ ?(, )?(and |or )?)+)',
                'first'
            ),
            (
                    '((NP_\\w+ ?(, )?)+(and |or )?any other NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?some other NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?be a NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?like (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    'such (NP_\\w+ (, )?as (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?like other NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?one of the NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?one of these NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?one of those NP_\\w+)',
                    'last'
                ),
                (
                    'example of (NP_\\w+ (, )?be (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?be example of NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?for example (, )?'
                    '(NP_\\w+ ?(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?which be call NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?which be name NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?mainly (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?mostly (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?notably (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?particularly (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?principally (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?in particular (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?except (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?other than (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?e.g. (, )?(NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ \\( (e.g.|i.e.) (, )?(NP_\\w+ ? (, )?(and |or )?)+'
                    '(\\. )?\\))',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?i.e. (, )?(NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and|or)? a kind of NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and|or)? kind of NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and|or)? form of NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?which look like NP_\\w+)',
                    'last'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?which sound like NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?which be similar to (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?example of this be (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?type (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )? NP_\\w+ type)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?whether (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(compare (NP_\\w+ ?(, )?)+(and |or )?with NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?compare to (NP_\\w+ ? (, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '(NP_\\w+ (, )?among -PRON- (NP_\\w+ ? '
                    '(, )?(and |or )?)+)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and |or )?as NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )? (NP_\\w+ ? (, )?(and |or )?)+ '
                    'for instance)',
                    'first'
                ),
                (
                    '((NP_\\w+ ?(, )?)+(and|or)? sort of NP_\\w+)',
                    'last'
                ),
                (
                    '(NP_\\w+ (, )?which may include (NP_\\w+ '
                    '?(, )?(and |or )?)+)',
                    'first'
                ),]



nounphrase_chunker=nltk.RegexpParser(chunk_patterns)

hearst_patterns= h

pos_tagger=PerceptronTagger()





def prepare(raw_text):
    sentences=nltk.sent_tokenize(raw_text.strip())
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[pos_tagger.tag(sent) for sent in sentences]
    return sentences

def chunk(raw_text):
    sentences=prepare(raw_text.strip())
    all_chunks=[]
    for sentence in sentences:
        chunks=nounphrase_chunker.parse(sentence)
        all_chunks.append(prepare_chunks(chunks))
    all_sentences=[]
    for raw_sentence in all_chunks:
        sentence = re.sub(r"(NP_\w+ NP_\w+)+",lambda m: m.expand(r'\1').replace(" NP_", "_"),raw_sentence)
        all_sentences.append(sentence)

    return all_sentences

def prepare_chunks(chunks):
    terms=[]
    for chunk in chunks:
        label=None
        try:
            label=chunk.label()
        except:
            pass
        if label is None:
            token=chunk[0]
            terms.append(token)
        else:
            np='NP_'+'_'.join([a[0] for a in chunk])
            terms.append(np)
    return ' '.join(terms)



def remove_np_term(term):
    return term.replace('NP_','').replace('_',' ')

def find_hyponyms(rawtext):
    hypo_hypernyms=[]
    np_tagged_sentences=chunk(rawtext)

    for sentence in np_tagged_sentences:
        for (hearst_pattern,parser) in hearst_patterns:
            matches=re.search(hearst_pattern,sentence)
            if matches:
                matched_pattern=hearst_pattern
                match_str=matches.group(0)
                nps=[a for a in match_str.split() if a.startswith('NP_')]

                if parser=='first':
                    hypernym=nps[0]
                    hyponyms=nps[1:]
                else:
                    hypernym=nps[-1]
                    hyponyms=nps[:-1]
                for i in range(len(hyponyms)):
                    hypo_hypernyms.append({'sentence': sentence,
                                           'hearst_pattern': matched_pattern,
                                           'hyponym': remove_np_term(hyponyms[i]),
                                           'hypernym': remove_np_term(hypernym)})
    return hypo_hypernyms