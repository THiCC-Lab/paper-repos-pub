
# Go to https://www.nltk.org/data.html to download Punkt tokenizer and stopwords first

import math
# TODO later: train Punkt on corpus instead of using pretrained
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
 
# Input: raw corpus txt file name, output file name
# Output: corpus split it into sentence per line file with punctuation tokenized, stop words removed, 
#         troublesome characters removed, and too large or small sentences removed
def process_text(fname_in, fname_out, MAX_LINE=math.inf):
    MIN_SENT_LEN = 2
    MAX_SENT_LEN = 100
    with open(fname_in,'r') as fo_in, open(fname_out, 'w+') as fo_out:
        i = 0
        for line in fo_in:
            if i > MAX_LINE-1:
                break
            sentences = sent_tokenize(line)
            # print(sentences)
            words = [word_tokenize(s) for s in sentences]
            # remove sentences with too few or too many words
            words = [s for s in words if len(s) >= MIN_SENT_LEN and len(s) <= MAX_SENT_LEN]
            # set lowercase
            words = [[w.lower() for w in s] for s in words]
            # remove stopwords
            stopwords_list = set(stopwords.words('english'))
            filtered_words = [[w for w in s if w not in stopwords_list] for s in words]
            # remove ":" because it interferes with ACT-R slot:value syntax
            # TODO later: use regexp to swap out : with something instead of just removing it
            filtered_words = [[w for w in s if ":" not in w] for s in filtered_words] 
            # print(filtered_words)
            # put words in each sentence back together, and add newline for each sentence
            joined_words = [" ".join(s) + "\n" for s in filtered_words]
            # combine sentences into string and write to out file
            joined_sents = " ".join(joined_words)
            # print(joined_sents)
            fo_out.write(joined_sents) 
            i += 1
    print(f"processed {i} lines") 

if __name__=="__main__":
    process_text("sample_text.txt", "sample_out.txt")