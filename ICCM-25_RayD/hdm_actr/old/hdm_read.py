# Implementation of HDM's function to read a corpus into memory
# Works with Python ACT-R, not Lisp ACT-R. See hdm_actr.py for the latter.
# Based on M.A. Kelly's Matlab files with BEAGLE:
# https://github.com/ecphory/BEAGLE-HHM/blob/master/HDM.m

import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *
from nltk.util import ngrams# as nltk_ngrams

# Takes in file name of tokenized corpus prepared with process_text.py
# and adds to memory
class CorpusModel(ACTR):
    goal = Buffer()
    # Buffer for holding retrieved chunk from memory
    hdm_retrieve = Buffer()
    hdm_module = HDM(hdm_retrieve)
    # memory module for holding test queries
    test_retrieve = Buffer()
    test_dm = Memory(test_retrieve)
    
    # TODO later: saving/loading HDM into/from pickle file
    def __init__(self, fname, n=3, test_queries=None):
        self.fname = fname
        self.n = n
        if test_queries is not None:
            for q in test_queries:
                test_dm.add(q)
        super().__init__()

    def init():
        total_ng = 0
        with open(self.fname) as fo:
            for line in fo:
                line = line.rstrip(".\n").rstrip(" ") 
                words = line.split(" ")
                # print(line)
                from nltk.util import ngrams
                # ^^ I have to import it here or it doesn't work for some reason :shrug:
                line_ngrams = ngrams(words, self.n)
                # print(list(line_ngrams))
                for ng in line_ngrams:
                    ngram_str = " ".join(list(ng))
                    # try:
                    hdm_module.add(ngram_str)
                    total_ng += 1
                    # print(ngram_str)
                    # except ZeroDivisionError:
                    #     print("Troublesome string: ", ngram_str)
                    #     raise ZeroDivisionError
        print(f"Added {total_ng} n-grams to HDM")              
        
            # hdm_module.add("a b c")
    # Get the next test query from memory
    # def recall_next(goal="test queries",
    #                 test_dm="busy:False", 
    #                 hdm_module="busy:False"):
    #     test_dm.request("?a ?b ?c", require_new=True)
    
    # Get test query in test buffer and query hdm with it
    # def test_mem_recall(goal="test queries", test_retrieve="?a ?b ?c",
    #                     test_dm="busy:False error:False", 
    #                     hdm_module="busy:False"):
    #     a = "?x" if a is "x" else a
    #     b = "?y" if b is "y" else b
    #     c = "?z" if c is "z" else c
    #     q = " ".join([a, b, c])
    #     hdm_module.request(q)
    #     print(f"requesting {q} from HDM")
    #     test_retrieve.clear()
        
    # Report result of HDM
    # def test(goal="test queries", hdm_retrieve="?a ?b ?c",
    #          hdm_module="busy:False error:False",
    #          ):
    #     print(f"{a} {b} {c}")
    #     hdm_retrieve.clear()
    
    # If error
    # def test_err(goal="load mem", hdm_module="error:True"):
    #     print("error retrieving memory from HDM")
    #     goal.clear()

def hdm_read(fname, n=3, test_queries=None):
    model = CorpusModel(fname, n=n, test_queries=test_queries)
    python_actr.log_everything(model)
    model.goal.set("test queries")
    model.run()

if __name__=="__main__":
    hdm_read(fname="sample_out.txt",
             n=3,
             test_queries=["situations may "])
    
   