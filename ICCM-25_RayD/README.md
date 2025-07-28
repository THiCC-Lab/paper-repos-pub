We aim to represent the world and social knowledge of agents in disaster management to model their decisions. The approach we take is to add the contents of domain-related corpora into ACT-R's memory, specifically a [Holographic Declarative Memory](https://doi.org/10.1111/cogs.12904) module (Kelly M.A. et al 2020) rather than ACT-R's in-built Declarative Memory (DM). Here we specify how to use our implementation of HDM in `hdm_actr.py` to work remotely with Lisp ACT-R including reading in a corpus using HDM.

# HDM with Canonical ACT-R
## Requirements
- [Python 3.11+](https://www.python.org/downloads/)
- [Numpy](https://numpy.org/install/)
- [SciPy](https://scipy.org/install/)
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
- [Scikit-Learn](https://scikit-learn.org/stable/install.html)
- [Clozure Common Lisp (CCL)](https://github.com/Clozure/ccl/releases/latest) 
    - or some other Lisp implementation, see [ACT-R reference manual](http://act-r.psy.cmu.edu/actr7.x/reference-manual.pdf) p22
- [Quicklisp](https://www.quicklisp.org/beta/)
- [Lisp-based ACT-R](http://act-r.psy.cmu.edu/software/)
- [Natural Language Toolkit (NLTK)](https://www.nltk.org/install.html)
- (Optional) Jupyter Notebook Requirements for your OS/Python set up  
## Running
1. Start ACT-R. 
    - Start your lisp version. This was developed with Clozure Common Lisp.
    - Load quicklisp.
    - Navigate to and load the `load-act-r.lisp` file.
2. Start HDM 
    - Open a python interpreter at this directory in an activated environment in which the prerequisite python libraries were installed.
    - Import `hdm_actr.hdm_actr`.
    - It should display the "ACT-R connection has been started." on the Python side and nothing on the ACT-R side. There may be a warning about chunk-ct, but these can be safely ignored.
    - You can use the `run_hdm.ipynb` Jupyter notebook to do this for you.
3. Run any ACT-R command and load models as normal.



## Current Functionality
The minimum required functions for a memory module, `(add)` and `(retrieve)`, as well as the convenience function `(dm)` are implemented. Properties of the HDM object for a model can be accessed on the Python side for debugging in the interpreter. The HDM object is in `hdm_actr.hdm_modules["model file name"]`.

Running ACT-R models from the GUI is not currently supported. Please use the terminal instead. 

**NOTE:** HDM retrieve works differently from DM. The original full chunk isn't stored in memory, so HDM's request function recalls slot/value pair(s) rather than an entire chunk. Here's how to change Lisp code written for DM:
- HDM as currently implemented can only retrieve the part of the chunk you specify with slots in the retrieval pattern. In the Lisp code, specify each unknown value wanted as `slotname [UNKNOWN_STR]`. The variable `UNKNOWN_STR` can be changed at the top of hdm_actr.py. By default, `UNKNOWN_STR = unknown`.  
- Use `define-chunks (...)` instead of `add-dm(...)` when defining a goal chunk to be later passed into `goal-focus`. HDM doesn't keep the chunk defined in ACT-R's memory.
- Ignore ACT-R warnings about chunks being deleted. Chunks used in slots should still work fine.

 Slot pulling is disabled my default, but if you set  `pull_slots=True` in HDM's python constructor, then it will (attempt to) retrieve the entire chunk like ACT-R does. Currently off by default while being tested more thoroughly.

 You can set and the get the following parameters using the `sgp` command (see
 [ACT-R manual](http://act-r.psy.cmu.edu/actr7.x/reference-manual.pdf) p120-121 for more):
 - `pull-slots` - whether or not to pull slots (default `nil` - False)
 - `hdm-v` - the verbosity of HDM's output (default `nil` - False)
 - `time-scale` - constant multiplied by the oscillators used for tracking chunks. the time scale should be lower the more chunks are added to the model. (default $10^{-5}$)
 - `hdm-O` -  Number of oscillators drawn from to make Time Learning Context Vector (default 15)
 - `hdm-T` - Number of Elements in Time Learning Context Vector (default 320)
 - `hdm-k` -  HDM HRR encoding dimension (default 512)
 - `slot-pulling-threshold` - (float from 0.0 to 1.0) Pull potential slots above this similarity threshold (default 0.1)
 - `slot-pulling-approach` - can be `top-n` to pick the top `n` slots to add to the request, `threshold` to add all slots above the similarity threshold, or `top-n-with-threshold` to add up the top `n` slots above the similarity threshold.

Getting parameter(s) is `(sgp :[param-name] ...)`, setting parameter(s) is `(sgp :[param-name] [param value] ...)`, and listing all parameters with documentation is simply `(sgp)`. Remember that `False` in Lisp is `nil` and `True` is `t` (or any non-nil value). Common Lisp parameters are effectively read as case insensitive by default so e.g. `(sgp HDM-V)` is fine as well.

You can also set `:slot-pull`, `:threshold`, `:n`, and `:approach` as request parameters to override the global parameters set by `(sgp)`.

## Future Features / Work in Progress
- We are testing a feature to request pulling up the whole chunk, with some noise, without explicitly requesting each slot. It currently works on limited tests but uses a static `slot_pulling_threshold` that may need to be adjusted by the modeler. We are planning a more flexible selection approach for the most likely relevant slots in the chunk. 
- making corpora reading methods faster - current method which adds sentence-by-sentence would only recommend for documents up to a dozen sentences
    - can try using add-values-dm with syntax `(add-values-dm this is a sentence)` to enter in corpora manually, possibly entering n-grams at a time like our python-actr implementation does.



# Reading Corpora Into HDM
 Much of the code here is based off of Dr. Kelly's [MATLAB files](https://github.com/ecphory/BEAGLE-HHM) for the BEAGLE-HMM model. Currently, we have read the NIMS corpus into memory and plan to build a basic decision model off of it. The raw text of NIMS is in `sample_text.txt` with the encoding UTF-16. We recommend using the Lisp ACT-R Python connection version as it is more up to date. 

## Lisp ACT-R - Python Connection
From the ACT-R interpreter, use the `(preprocess-text "[input_filename]" "[output_filename]")` 
to read an input plaintext file into an output file formatted to be read 
by HDM. Then, after loading an ACT-R model call `(read-corpus-hdm [filename]`)` to add the corpus into memory. 

The same corresponding methods can be called in the python interpreter or jupyter notebook with `hdm_actr.preprocess_text` and `hdm_actr.read_corpus_hdm`.

If filename paths are relative, they are relative to `hdm_actr.py`'s location. The absolute path can be used instead.

## Python-Based ACT-R
**Note:** This is the older python code in the `old` folder. It is no longer being maintained and file paths may need to be changed. To use the most current implementation, use the ACT-R commands specified above that are defined in `hdm_actr.py`.
### Prerequisites
- Python 3.11 and numpy installed
- Recommended: create and activate a Python environment
- Install Python ACT-R from [this](https://git.psu.edu/thicc-lab/python_actr/-/tree/main?ref_type=heads) repository
- Install the Natural Language Toolkit (NLTK) from [these](https://www.nltk.org/install.html) instructions
- Download the Punkt tokenizer (`punkt`) and stop word list (`stopwords`) using any of [these](https://www.nltk.org/data.html) methods

### Pipeline
First, run the `process_text` function from `old/process_text.py` with the file name of the input raw text, the file name of the desired output, and optionally a max line number after which text will be ignored. `old/process_text` separates the corpus into sentences and outputs each by line, tokenizes the words by punctuation, removes troublesome special characters, and removes stopwords.

Next, run `hdm_read` from `old/hdm_read.py` with the file name of the output from `process_text`. It will create an ACT-R model with an HDM module representing the text by adding it to memory n-gram by n-gram. The default is `n=3`, corresponding to trigrams, but this can be changed as an input parameter.

## Debugging Tips
- Relative filenames are relative to hdm_actr/hdm_actr.py so using absolute paths may be easier.
- Use either forward slashes or double backslashes `\\` in the file path string so you're not specifying an escape character.
- Check the file encoding of the text files are the same ones your OS uses. For example, a .txt file preprocessed on mac may output a file in UTF-8. Preprocessing that file on windows, may use UTF-16 as the system default, would error. Save text files in different encodings using a text editor and/or change the encoding parameters in the functions above as needed.