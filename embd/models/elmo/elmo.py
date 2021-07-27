import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModel


tokenizer = AutoTokenizer.from_pretrained("huggingtweets/elmo_oxygen")
model = AutoModelWithLMHead.from_pretrained("huggingtweets/elmo_oxygen", output_hidden_states=True)

     
def get_word_idx(sent: str, word: str):
	return sent.split(" ").index(word)
    
def get_hidden_states(encoded, token_ids_word, model, layers):
    with torch.no_grad():
    	output = model(**encoded)
    states = output.hidden_states
    output = torch.stack([states[i] for i in layers]).sum(0).squeeze()
    word_tokens_output = output[token_ids_word]     
    return word_tokens_output.mean(dim=0)
    
def get_word_vector(sent, idx, tokenizer, model, layers):
     encoded = tokenizer.encode_plus(sent, return_tensors="pt")
         # get all token idxs that belong to the word of interest
     token_ids_word = np.where(np.array(encoded.word_ids()) == idx)
     
     return get_hidden_states(encoded, token_ids_word, model, layers)
        
def main(sent, idx_word, layers=None):
     # Use last four layers by default
     layers = [-4, -3, -2, -1] if layers is None else layers
     #sent = "I like cookies . vey very much"
     
     idx = get_word_idx(sent, idx_word)
    
     word_embedding = get_word_vector(sent, idx, tokenizer, model, layers)
         
     return word_embedding



