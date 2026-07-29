# Adapted from Dr. Mary Kelly's HDM code and simple_declarative.py in the ACT-R
# tutorial files. Depends on the actr interface `actr.py` from the tutorial.

from hdm_actr.hrr import HRR
from hdm_actr.oscillators import TimeVector
from hdm_actr import actr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import argparse
from enum import Enum, auto
import threading
import numpy as np
import copy
import math
from collections import OrderedDict
from time import perf_counter
from pathlib import Path
import json

# Remove the default module and the commands it creates which
# are being redefined.
actr.undefine_module('declarative')
actr.remove_command('add-dm')
actr.remove_command('dm')
actr.remove_command('sdp')

# To support multiple models keep a dictionary of model name to module instances
hdm_modules = {}

# Setting what symbol you use as a placeholder for a slot's unknown value in a
# lisp-side ACT-R retrieval request. The word will be reserved and can't be
# used elsewhere as a slot/value in the retrieval request, though it can still
# be used as a slot or value when adding to memory.
UNKNOWN_STR = "unknown"
# In requests, all symbols starting with this will be the negation. For
# example, color:!black will mean requesting a chunk with a color that is *not*
# black. This string will be reserved for that purpose in requests (not in
# corpus!), so feel free to redefine it as needed.d 
NEGATION_STR = "!"
# An Enum to keep track of special symbols such as the unknown value in
# requests so they can be processed as normal words in corpora. e.g. "?" for
# punctuation 
class SpecialSymbols(Enum):
    UNKNOWN = UNKNOWN_STR
    # cleaner representation in interpreter output
    def __repr__(self): 
        if self.name == "UNKNOWN":
            return f"<{UNKNOWN_STR}>"
    
    def __str__(self):
        return self.__repr__()
# 
# Marks and stores value being negated in Chunk contents.
class Negation():
    def __init__(self, val):
        self.val = val
    # cleaner representation in interpreter output
    def __repr__(self) -> str:
        return f"{NEGATION_STR}<{self.val}>"

# checks type of value to see if it's a negation, unknown, or a normal value 
def val_type(val):
    if val == SpecialSymbols.UNKNOWN:
        return "unknown"
    if isinstance(val, Negation):
        return "negation"
    return "text"


class Chunk():
    # Takes list of chunk arguments passed to add-dm corresponding to one chunk
    # and/or the chunk's name in ACT-R memory. For has slots case, assumes
    # chunks were successfully definec. It stores a data structure named
    # contents, which is either a dictionary for slot-value chunks or a list
    # for values-only chunks. It can also have a list of unknowns for query chunks.

    def __init__(self, chunk_args, chunk_name=None, 
                 has_slots=True, check_defined=True,
                 store_chunk=False, request=False, is_dict=False):
        self.name = chunk_name
        # contains slots / indices of unknown values
        # empty indicates no unknowns
        self.unknowns = []
        print("Inside init", chunk_args)
        if has_slots:
            self.has_slots = True
            # important to keep ordered? I believe order matters in adding to memory
            # format contents as slot:value dictionary
            self.contents = OrderedDict()
            if check_defined:
                # The chunk was defined in ACT-R's memory, so we can use
                # ACT-R's built in methods to get the slots and values for the
                # chunk. Probably being called inside add-dm. The chunk may be
                # empty. 
                assert chunk_name # need name for act-r fn calls
                # Get the list of slots from ACT-R associated with the chunk's
                # name
                slots_list = actr.chunk_filled_slots_list(chunk_name, True)
                # loop over slots to get values from ACT-R
                if slots_list is not None:
                    for slot in slots_list:
                        val = actr.chunk_slot_value(chunk_name, slot)
                        # In case the slots and values aren't strings (is this
                        # possible?) putting this since HDM uses strings
                        # internally.
                        self.contents[str(slot)] = str(val)
                else:
                    # handle name-only case with no slot:value pairs
                    print(f"{chunk_name} as name-only chunk")
                    self.name_only = True
            else:
                # The chunk hasn't already been defined in ACT-R's memory. This
                # means we can't use ACT-R's built-in methods and will have to
                # format the chunk args into a chunk ourselves. This is likely
                # a request chunk.
                if is_dict == True:
                    print("we are directly adding dict")
                    self.contents=chunk_args
                else: 
                    if len(chunk_args) % 2 != 0:
                        actr.print_warning("HDM: Invalid request chunk format")
                        raise Exception(f"Chunk args {chunk_args} not even length - invalid format")
                    else:
                        # strip whitespace
                        chunk_args = [c.strip(" ") for c in chunk_args]
                        # put each pair into slot/val dict
                        ca_itr = iter(chunk_args)
                        for ca in ca_itr:
                            self.contents[ca] = next(ca_itr)
                        # if this is a request chunk, note slot/index of unknowns
                        if request:
                            for s, v in self.contents.items():
                                if v.lower() == UNKNOWN_STR.lower():
                                    self.unknowns.append(s)
                                    # set value of each unknown to unknown enum to prep for HDM
                                    self.contents[s] = SpecialSymbols.UNKNOWN
                                # If this is a negation, make it a Negation object
                                # and store its value. It's an unknown too so keep
                                # track of it as well.
                                if v.lower().startswith(NEGATION_STR.lower()):
                                    self.unknowns.append(s)
                                    self.contents[s] = Negation(v[1:])
                        if len(self.unknowns) > 0: 
                            print("Request chunk with multiple unknowns")
        else:
            # Second case: list of values 
            self.has_slots = False
            # Assuming check_defined = False bc you can't define a values-only
            # list in ACT-R.
            # Input validation - check that the input is a flat list of strings
            for c in chunk_args:
                if c is None or (not isinstance(c, str)):
                    raise Exception("Values list chunk must be 1D list of strings") 
            # Store value list
            self.contents = chunk_args
            if request:
                # Note index of unknowns and replace with unknown enum to prep for HDM
                for i, v in enumerate(self.contents):
                    if v.lower() == UNKNOWN_STR.lower():
                        self.unknowns.append(i)
                        self.contents[i] = SpecialSymbols.UNKNOWN
                    if v.lower().startswith(NEGATION_STR.lower()):
                        self.unknowns.append(i)
                        self.contents[i] = Negation(v[1:])
                    
            
    
    # so we have informative statements in interpreter
    def __repr__(self) -> str:
        return f"Name: {self.name} \nContents: {self.contents}"
    
    # ~~replaces HDM's chunk_to_str~~
    # no longer needed bc HDM modifies chunk.contents directly now
    def __str__(self) -> str:
        if self.has_slots:
            out = []
            for s, v in self.contents.items():
                out.append(f"{s}:{v}")
            return " ".join(out)
        else:
            return " ".join(self.contents)

    # For output logging, need to store chunk as json so it can be analyzed easily later
    def json_rep(self):
        if not self.has_slots:
            raise NotImplementedError
        print("logging output")
        return json.dumps(self.contents)
    # replaces HDM's HDM.chunk_to_list
    #
    # if querying = True, list only includes first unknown slot/value or value
    # because HDM's request_value can only handle one unknown at a time

    def to_list(self, querying=False):
        # for slotted chunks, HDM wants format [[slot1, val1], [slot2, val2]..]
        # doing the same but each [a,b] is (a,b). should be fine?
        if self.has_slots:
            if querying and len(self.unknowns) > 1:
                out = []
                for s, v in self.contents.items():
                    if s not in self.unknowns:
                        out.append((s, v))
                    elif s == self.unknowns[0]:
                        out.append((s, v))
                return out
            else:
                return list(self.contents.items())
        else:
            if querying and len(self.unknowns) > 1:
                out = []
                for i, v in enumerate(self.contents):
                    if i not in self.unknowns:
                        out.append(v)
                    elif i == self.unknowns[0]:
                        out.append(v)
                return out
            else:
                return self.contents
    
    # fn to convert [(s,v), (s,v)] -> [s, v, s, v]
    # for use as chunk args, for example
    def to_flat_list(self):
        if self.has_slots:
            out = []
            for k, v in self.contents.items():
                out.append(k)
                out.append(v)
            return out
        else:
            return self.contents
    
    def has_unknowns(self):
        return len(self.unknowns) != 0
    
    # replaces first unknown with new retrieved value
    def replace_unknown(self, new):
        if not self.has_unknowns():
            raise Exception("No unknowns to replace")
        # this works for both with and without slots!
        unk = self.unknowns.pop(0)
        self.contents[unk] = new
    
    def add_unknown(self, slot):
        """add slot `slot` with unknown value to chunk"""
        # if the slot has a value in the chunk, don't overwrite it with an
        # unknown
        if slot in self.contents:# and slot not in self.unknowns:
            # should I call an exception here instead? I feel like it will
            # happen often enough during the time encoding checking process that
            # it should just be ignored
            return
        self.contents[slot] = SpecialSymbols.UNKNOWN #"?"#UNKNOWN_STR
        self.unknowns.append(slot)
        

# global variable for setting parameters, if needed
# TODO: transfer HDM param defaults here and make HDM constructor use this
CONFIG = {}

# HDM class to hold the module info and handle operations
class HDM():

    def __init__(self, latency=0.05,threshold=-4.6,slot_pulling_threshold=0.1,maximum_time=10.0,
                 finst_size=4,finst_time=3.0, N=512, verbose=False, forgetting=1.0,
                noise=0.0, T=320, O=15, time_scale=10e-5, pull_slots=True,
                slot_pulling_approach='top-n', slot_pulling_n=4, log_outcomes=None):
        self.lock = threading.Lock() # To avoid potential issues always lock access when changing things
        # self.chunks = []             # list of all the chunk objects
        
        self.N = N
        self.verbose = verbose
        # "The environment vectors represent the perceptual features of a
        # stimulus." (Kelly et al 2020) The env dictionary maps the name of
        # each stimulus (a "value" in ACT-R chunking) to a HRR.
        self.env = {SpecialSymbols.UNKNOWN: HRR(N=self.N)}
        # Used for encoding the unknown value being requested in request
        # vectors.
        self.placeholder = self.env[SpecialSymbols.UNKNOWN] #HRR(N=self.N)
        # The memory vectors represent the associations a stimulus has with
        # other stimuli. Recorded as dictionary where key is stimulus name
        # "e.g. red" and value is HRR vector representing those associations.
        # In ACT-R's slot-value chunking, these are the values.
        self.mem={} # replaces self.chunks
        # These are the slots (e.g. "color") recorded as permutations
        # (re-orderings) to be bound with an environment vector to get an HRR
        # representing a slot-value pair. Each one is an N-size random
        # shuffling from the sequence 1...N.
        self.slots={}
        # I believe ")" or "left" is P_before in the Kelly at al 2020, the slot
        # used for encoding lists of values i.e. words in a corpus. 
        self.left = np.random.permutation(self.N)
        
        # Initializing a function for tracking time (which # chunk we're on) as
        # a vector of oscillators (see Brown 2000) and storing relevant
        # parameters. 
        self.time_vector = TimeVector(O_n=O, T_n=T, scale=time_scale)
        self.T = T
        self.O = O
        self.time_scale = time_scale
        # Storing the associations between slots in terms of which chunks they
        # were added into at the same time. Each slot name maps to a time HRR.
        self.time_mem={}
        self.time_env = {}
        self.time_hrr_mat_n = None
        for i in range(T):
            # not using slots (permutations) for time vectors, so commenting out
            # self.time_slots[f"T_{i}"] = np.random.permutation(self.N)
            # is it ok to use the same keys here? it's not a normal part of 
            # a chunk so I figured
            self.time_env[f"T_{i}"] = HRR(N=self.N)
        self.chunk_count = 0
        self.pending = False         # any event for an ongoing retrieval/failure
        self.error = False           # did the last request fail
        self.lf = 1                  # value of :lf parameter
        self.esc = False             # is the :esc parameter set

        # adding some act-r params
        self.ans = 0.0
        self.rt = 0.0
        self.bll = 0.0

        # Initializing various other parameters used for HDM retrieval.
        self.adaptors=[]
        self.latency=latency
        self.threshold=self.logodds_to_cosine(threshold)
        self.slot_pulling_threshold = slot_pulling_threshold
        self.maximum_time=maximum_time
        self.partials=[]
        self.finst=Finst(self,size=finst_size,time=finst_time)
        self._request_count=0
        self.inhibited=[] # list of inhibited values
        self.forgetting=forgetting
        self.noise=noise
        self.lastUpdate = 0.0
        self.pull_slots = pull_slots
        self.slot_pulling_approach = slot_pulling_approach
        self.slot_pulling_n = slot_pulling_n
        # write info to file for testing purposes
        self.log_outcomes = log_outcomes
        # which parameters to log
        # self.log_params = []
        # print("creating an HDM object")
        

    def reset(self):
        self.lock.acquire()
        self.mem = {}
        self.env={SpecialSymbols.UNKNOWN: HRR(N=self.N)}
        self.placeholder = self.env[SpecialSymbols.UNKNOWN]
        self.slots={}#')': np.random.permutation(self.N)}
        self.left = np.random.permutation(self.N)
        # adding time tracking
        self.time_mem={}
        for i in range(self.T):
            # self.slots[f"T_{i}"] = np.random.permutation(self.N)
            self.time_env[f"T_{i}"] = HRR(N=self.N)
        self.time_vector = TimeVector(O_n=self.O, T_n=self.T, scale=self.time_scale)
        self.chunk_count = 0
        self.pending = False
        self.error = False
        self.lock.release()
    
    
    # function for adding noise over time to memory    
    def addNoise(self):
        # weight by time difference
        diff = self.now() - self.lastUpdate
        for value in self.mem.keys():
            noiseVector = HRR(N=self.N)
            self.mem[value] = self.mem[value] + (self.noise * diff * noiseVector)
        self.lastUpdate = self.now()
            

        # generate Gaussian vectors and random permutations for values & slots without
    # chunkList is a list of attributes, each attribute is a string
    def defineVectors(self,chunkList):
        for attribute in chunkList:
            # check to see if there is a slot, or if it's just a value without a slot
            if isinstance(attribute, tuple):
                slot,value = attribute
                # if it's a new slot, create a new random permutation
                if slot not in self.slots.keys():
                    self.slots[slot] = np.random.permutation(self.N)
                if slot not in self.time_mem.keys():
                    self.time_mem[slot] = HRR(data=np.zeros(self.N))
            else:
                value = attribute
            # if it starts with ! (i.e., not) just ignore that for now
            if val_type(value) == 'negation':
                value = value.val
            # if it's a new value, create a new random vector
            # same as in self.env.keys() I guess?
            if value not in self.env.keys():
                self.env[value] = HRR(N=self.N)#,text=value)
                self.mem[value] = HRR(data=np.zeros(self.N))#self.env[value]
                # self.time_mem[value] = HRR(data=np.zeros(self.N))#

           
            



    def addWithSlots(self,chunk):

        # convert chunk to a list of (slot,value) pairs
        chunkList = chunk.to_list()
        # define random Gaussian vectors and random permutations for any undefined values and slots
        self.defineVectors(chunkList)
        # Get HRR vector for entire chunk
        whole_chunk_vec = self.getWholeChunkVec(chunkList)
        # Get vector representing the chunk's time order to enable full-chunk
        # recall and then convolve it with whole-chunk HRR representation
        
        chunk_time_vec =  self.getChunkTime(self.chunk_count) * whole_chunk_vec
        
        # update the memory vectors with the information from the chunk by
        # constructing queries that each value is the answer to 
        for p in range(0,len(chunkList)):
            # For each slot-value pair, replace the value with a placeholder
            # vector so we can construct queries that the value is the answer to
            # create a copy of chunkList
            query = copy.deepcopy(chunkList)
            # replace p's value with ? in query, but leave slot as is
            # query[p][1] = '?'
            # ^^ doesn't work with tuples, so replacing with:
            query[p] = (query[p][0], SpecialSymbols.UNKNOWN)
            print(f"The value getting replaced: {chunkList[p][1]}")
            print(f"Query vector: {query}")
            # compute chunk vector
            chunkVector = self.getUOGwithSlots(query)
            # update time memory not replacing anything with "?" because
            # storing entire chunk at once
            self.updateTimeMemory(chunkList[p], chunk_time_vec)
            # update memory
            self.updateMemory(chunkList[p][1],chunkVector)


    # add a chunk to memory
    # when the chunk is just a list of values
    # without slots
    def addJustValues(self,chunk):
        # convert chunk to a list of values
        chunkList = chunk.to_list()
        # define random Gaussian vectors for any undefined values
        self.defineVectors(chunkList)
        # update the memory vectors with the information from the chunk
        for p in range(0,len(chunkList)):
            # create a copy of chunkList
            query = copy.deepcopy(chunkList)
            # replace p with ? in query
            query[p] = SpecialSymbols.UNKNOWN
            # compute chunk vector
            chunkVector = self.getUOG(query)
            # update memory
            self.updateMemory(chunkList[p],chunkVector)

    # function for constructing a vector that represents chunkList
    # where chunkList is a list of values without slots
    # and p is the location of ? in chunkList
    # returns chunk, an HRR representing all unconstrained open grams in chunkList
    # that include the ? at p.
    # When slots are not used, the permutation "left" is used to preserve order
    def getUOG(self, chunkList):
        numOfItems = len(chunkList)
        chunk = HRR(data=np.zeros(self.N))
        sum   = HRR(data=np.zeros(self.N))
        p     = numOfItems # initially, this will be set to index of ? when ? is found
        for i in range (0,numOfItems):
            # get the vector for the value i
            value = chunkList[i]
            # set p as the location of the placeholder ?
            if val_type(value) == 'unknown':
                p = i
            # TODO: fully implement value negation
            # if value starts with ! then negate the environment vector
            if val_type(value) == 'negation':
                valVec = -1 * self.env[value.val]
            # otherwise use the environment vector as is
            else:
                valVec = self.env[value]
            # compute the chunk vector 
            if i == 0:
                sum = valVec
            elif (i > 0) and (i < p):
                leftOperand = chunk + sum
                leftOperand = leftOperand.permute(self.left)
                chunk       = chunk + leftOperand.convolve(valVec)
                sum         = sum + valVec
            elif i == p:  # force all skip grams to include item p
                leftOperand = chunk + sum
                leftOperand = leftOperand.permute(self.left)
                chunk       = leftOperand.convolve(valVec)
                sum         = valVec
            else: # i > p, i > 0
                leftOperand = chunk + sum
                leftOperand = leftOperand.permute(self.left)
                chunk       = chunk + leftOperand.convolve(valVec)
        return chunk


    # function for constructing a vector that represents chunkList
    # where chunkList is a list of values WITH slots as permutations
    # returns chunk, an HRR representing all unconstrained open grams in chunkList
    # that include the ?
    # Represents Equation 5 in HDM paper
    def getUOGwithSlots(self, chunkList):
        if self.verbose: print(f"UOGwithSlots called on {chunkList}")
        numOfItems = len(chunkList)
        chunk = HRR(data=np.zeros(self.N))
        sum   = HRR(data=np.zeros(self.N))

        p     = numOfItems # initially, this will be set to index of ? when ? is found
        for i in range (0,numOfItems):
            # get the vector for the slot value pair at i
            slotvalue = chunkList[i]
            slot  = slotvalue[0]
            value = slotvalue[1]
            # set p as the location of the placeholder ?
            if val_type(value) == 'unknown':
                p = i
            # if value starts with ! then negate the environment vector
            if val_type(value) == 'negation':
                valVec = -1 * self.env[value.val]
            # otherwise use the environment vector as is
            else:
                valVec = self.env[value]
            # permute the environment vector by the slot
            valVec = valVec.permute(self.slots[slot])
            # compute the chunk vector 
            if i == 0:
                sum = valVec
                
            elif (i > 0) and (i < p):
                leftOperand = chunk + sum
                chunk       = chunk + leftOperand.convolve(valVec)
                sum         = sum + valVec
                
            elif i == p:  # force all skip grams to include item p
                leftOperand = chunk + sum
                chunk       = leftOperand.convolve(valVec)
                sum         = valVec
                
            else: # i > p, i > 0
                leftOperand = chunk + sum
                chunk       = chunk + leftOperand.convolve(valVec)
                
        return chunk 
    
    # constructs chunk without UOG, not centered around queried memory vector
    # e_v1 permute by  + ...
    def getWholeChunkVec(self, chunk_list):
        chunk = HRR(data=np.zeros(self.N))
        for (slot, value) in chunk_list:
            # if value starts with ! then negate the environment vector
            if val_type(value) == 'negation':
                valVec = -1 * self.env[value.val]
            # otherwise use the environment vector as is
            else:
                valVec = self.env[value]
            if val_type(value) != 'unknown':
                chunk += valVec.permute(self.slots[slot])
        return chunk

    # Return the HRR time vector evaluated at t=chunk order (1st, 2nd, etc) 
    def getChunkTime(self, t=None):
        if t is None:
            t = self.chunk_count
        # get time context vector at cth chunk
        Tc = self.time_vector.eval(t)
        # construct time HRR by repeated fractional bindings and convolution
        time_hrr = self.time_env["T_0"] ** Tc[0]
        for i in range(1, self.T):
            # time_hrr = time_hrr.convolve(self.env[f"T_{i}"] ** Tc[i])
            time_hrr *= self.time_env[f"T_{i}"] ** Tc[i]
        return time_hrr
    
    def hrr_mat(self,chunk_count):
         time_hrr_mat = [self.getChunkTime(t) for t in range(chunk_count)] 
         self.time_hrr_mat_n = time_hrr_mat
         print("done",self.time_hrr_mat_n)

        

    # for updating a memory vector for value with chunk vector
    def updateMemory(self,value,chunking):
        if val_type(value) == 'negation':
            if value.val not in self.mem:
                self.mem[value.val] = -1*chunking
            else:
                self.mem[value.val] = self.forgetting * self.mem[value.val] - chunking
        else:
            if value not in self.mem:
                self.mem[value] = chunking
            else:
                self.mem[value] = self.forgetting * self.mem[value] + chunking

    # update memory vector with time-chunk vector
    # given (slot, value) tuple
    def updateTimeMemory(self, slot_value, chunk_hrr):
        slot, value = slot_value
        # not doing forgetting for now
        self.time_mem[slot] += chunk_hrr
        # self.time_mem[value] += chunk_hrr
        

    # This assumes the module's lock is already held.
    def add_chunk_to_dm (self, chunk):
        assert isinstance(chunk, Chunk)
        # add noise to memory
        if self.noise != 0:
            self.addNoise()
        # assign any unassigned values in chunk
        # self.assignValues(chunk)
        if chunk.has_slots:
            # call addWithSlots to add a chunk with slot:value pairs to memory
            print("add with slots")
            self.addWithSlots(chunk)
            self.chunk_count += 1
        else:
            # call addJustValues to add a chunk with values and no slots to memory
            print("add values")
            self.addJustValues(chunk)
        

    # default request function, call this make sure to call from outer request
    # function or there may be concurrency issues
    def request(self, chunk, slot_pull=None, require_new=None, n=None, threshold=None, approach=None):
        """
        Return memory chunk matching request chunk.

        The `approach` for pulling the entire chunk can be `top_n` or
        `threshold`, with n supplied as a corresponding argument for the former
        and `threshold` for the latter.
        """
        # internal helper to use arg settings if defined else model default settings
        def default_arg(arg_p, mod_p):
            if arg_p is None:
                return mod_p
            return arg_p
        try:
            slot_pull = default_arg(slot_pull, self.pull_slots)
            n = default_arg(n, self.slot_pulling_n)
            approach = default_arg(approach, self.slot_pulling_approach)
            threshold = default_arg(threshold, self.slot_pulling_threshold)
        except Exception as e:
            actr.print_warning(f"Error setting slot pulling parameters {e}")
            print("Slot pulling parameter defaults may not have been set correctly")
        self._request_count+=1
        # add noise to memory
        if (self.noise != 0):
            self.addNoise()
        # clear list of inhibited values from previous queries
        self.inhibited = []
        # assign any unassigned values in chunk string and load inhibited values into self.inhibited
        print(f"Assigning values to chunk {chunk}")
        # does this even do anything without the bound dictionary?
        # self.assignValues(chunk)
        print(f"Chunk is now {chunk}")
        if not slot_pull:
            if not chunk.has_unknowns():
                actr.print_warning("Request has no unknowns")
                # TODO: implement resonance
                # return self.resonance(chunk)
                return
        else:
            # Try to pull slots of the chunk being requested so the request asks
            # for the entire chunk, not just part of it. Choose slots whose
            # time-memory vectors yield reconstructed time HRR vectors most
            # similar to the actual time HRRs.
            #
            # get chunk query vector and its inverse
            query_vec = self.getWholeChunkVec(chunk.to_list())
            query_vec_inv = ~query_vec
            # can only select one timestep i.e. one set of slots corresponding to
            # one chunk, so keep track of which timestep is best by some metric
            # which is calculated depends on approach
            best_timestep = 0
            best_timestep_metric = 0
            slots_to_add = [] 
            

            

            for t in range(self.chunk_count):
                # calculate the time HRR vector at time step t
                # time_hrr = self.getChunkTime(t)
                # keep track of the best slots for each timestep and their
                # corresponding similarities with time_hrr
                sims_t = []
                slots_t = []
                metric_t = 0
                # assuming time_mem only keeps track of slots for time efficiency
                # reasons - check if still true
                for (slot_name, mt) in self.time_mem.items():
                    # if mt in self.slots.keys():
                    # compare actual time to reconstructed time vector
                    sim = self.time_hrr_mat_n[t].compare(mt * query_vec_inv)
                    # print(f"Time Step {t}, slot {slot_name}, sim {sim}")
                    if (approach == "threshold" or "top-n-with-threshold"):
                        # only consider slots above similarity threshold 
                        if sim > threshold:
                            sims_t.append(sim)
                            slots_t.append(slot_name)
                    else:
                        # or just add every slot to possible list
                        sims_t.append(sim)
                        slots_t.append(slot_name)
                if (approach == "top-n" or approach == "top-n-with-threshold") and n != 0:
                    # sort slot similarities with corresponding slots
                    inds = np.argsort(np.array(sims_t))
                    # take top n slots and sims
                    slots_t = np.array(slots_t)[inds][-n:]
                    sims_t = np.array(sims_t)[inds][-n:]
                    # if approach == "top_n_with_threshold":
                    #     # filter out slots within top n below minimum similarity threshold
                    #     slots_t = slots_t[sims_t > threshold]
                    #     sims_t = sims_t[sims_t > threshold]
                # calculate total similarity of slots selected by approach
                metric_t = sum(sims_t)
                # keep track of which timestep (chunk) is most likely to be the
                # one being requested  
                if metric_t > best_timestep_metric:
                    best_timestep = t
                    best_timestep_metric = metric_t
                    slots_to_add = slots_t
            # add pulled slots to chunk
            # print(f"adding slots to request chunk: {slots_to_add}")
            for slot in slots_to_add:
                chunk.add_unknown(slot)
            # print(f"Chunk with slots added: ", chunk)
            # print(f"New Chunk Contents: {chunk.contents}, New chunk unknowns: {chunk.unknowns}")\
            # self.assignValues(chunk)
            # assignValues currently doesn't do anything but putting it here for when we fix it ^^
            # request and fill in unknown values in request chunk
        while chunk is not None and chunk.has_unknowns():
            chunk = self.requestValue(chunk, require_new)
        if self.log_outcomes is not None and self.log_outcomes != "":
            try:
                with open(self.log_outcomes, "a") as f:
                    if chunk is not None:
                        f.write(chunk.json_rep())
                    else:
                        f.write("{}")
            except Exception as e:
                actr.print_warning("file cannot be found, does not exist, or cannot be written to")
        return chunk



    def requestValue(self,chunk,require_new=False):
        if self.verbose: print(f"Requesting unknown {chunk.unknowns[0]} of chunk {chunk}")
        # check if chunk has slots
        assert isinstance(chunk, Chunk)
        if chunk.has_slots:
            queryVec = self.queryWithSlots(chunk)
        else:
            queryVec = self.queryJustValues(chunk)
        if self.verbose:
            print(f"Query vec for request {chunk.to_list(querying=True)} created")
        highestCosine = self.threshold
        bestMatch = 'none'
        if self.verbose:
            print('inhibited values: ' + str(self.inhibited))
            print('Finst contains: ' + str(self.finst.obj))
        # find the best match to the query vector in memory
        for mem,memVec in self.mem.items():
            # skip inhibited values
            if mem not in self.inhibited:
                # skip previously reported values if require_new is true
                if (not require_new) or (not self.finst.contains(mem)):
                    thisCosine = memVec.compare(queryVec)
                    if self.verbose:
                        print(mem, thisCosine)
                    if thisCosine > highestCosine:
                        highestCosine = thisCosine 
                        bestMatch = mem

        if bestMatch == 'none':
            if self.verbose:
                actr.model_output("Output ")
                print('No matches found above threshold of cosine =', self.threshold)
            # self.fail(self._request_count)
            return None
        else:
            # replace the placeholder '?' with the retrieved memory 'bestMatch'
            chunk.replace_unknown(bestMatch)
            if self.verbose:
                print('Best match is ' + bestMatch)
                print('with a cosine of ' + str(highestCosine))
                print('output chunk = ' + str(chunk))
            # chunkObj = Chunk(chunk)
            # chunkObj.activation = highestCosine
            chunk.activation = highestCosine
            print('with a cosine of ' + str(highestCosine))
            self.finst.add(bestMatch)
            return chunk
            # self.recall(chunkObj,matches=[],request_number=self._request_count)
    
    # performs multiple queries to determine the "coherence" of the chunk
    # TODO: resonance
    def resonance(self,chunk):
        raise NotImplementedError


    # compute the coherence / activation of a chunk
    # called by resonance
    # called by request when no ? values are present
    # if logodds=True, the convert from mean cosine to logodds and return logodds
    def get_activation(self,chunk,logodds=False):
        raise NotImplementedError

    # create a query vector for a chunk consisting of slot:value pairs.
    # the query vector consists of the open n-grams of the slot:value pairs.
    # only open n-grams that contain ? are included.
    # the query vector must have one and only one query item "?".
    def queryWithSlots(self,chunk):
        assert isinstance(chunk, Chunk)
        if self.verbose: print(f"Querying with slots on chunk {chunk}")
        # convert chunk to a list of (slot,value) pairs with first unknown, if
        # multiple
        chunkList = chunk.to_list(querying=True)
        # define random Gaussian vectors and random permutations for any
        # undefined values and slots
        if self.verbose: print("Defining vectors for undefined vals/slots")
        self.defineVectors(chunkList)
        print("thirs option for error")
        # construct the query vector
        
        queryVec = self.getUOGwithSlots(chunkList)
        return queryVec
    
    # create a query vector for a chunk consisting of slot:value pairs.
    # the query vector consists of the open n-grams of the values.
    # only n-grams that contain ? are included.
    # the query vector must have one and only one query item "?".
    def queryJustValues(self,chunk):
        # convert chunk to a list of values
        chunkList = chunk.to_list(querying=True)
        # define random Gaussian vectors for any undefined values
        self.defineVectors(chunkList)
        print("fourth option for error")
        # get all combinations ranging from pairs of slot-value pairs to sets
        queryVec = self.getUOG(chunkList)
        return queryVec
    
    # Converts vector cosine (which approximates root probability)
    # to a log odds ratio (which is what ACT-R activation estimates) 
    def cosine_to_logodds(self,cosine):
        if cosine > 0.999:
            cosine = 0.999
        return math.log(cosine**2 / (1 - cosine**2))

    # Converts log odds ratio or ACT-R activation
    # to a root probability (which the cosine approximates)
    def logodds_to_cosine(self,logodds):
        return math.sqrt(np.exp(logodds) / (np.exp(logodds) + 1))

# Called by every function below that accesses an HDM object. The function gets
# it from the hdm_modules dictionary that the create() module puts an HDM
# object into. The name parameter can be accessed from the lisp side of the
# connection via actr.py's current_model() method 
def current_module(name) -> HDM:
    return hdm_modules[name.lower()]

# utility class to handle lisp arguments to python functions
class LispArgParser(argparse.ArgumentParser):
    # overriding this from base class so it prints warning to ACT-R terminal
    # instead of stderr and raises an exception (to be handled in function) and
    # exits instead of exiting the python interpreter
    def error(self, message):
        actr.print_warning(message)
        # actr.print_warning(self.format_usage())
        actr.print_warning(self.format_help())
        raise Exception(message)
    # these five lines of code took me like two hours to work out right lol

# Functions and ACT-R commands for the scheduled events to handle retrievals

def retrieved_chunk(name, *chunk_list):
    # assert chunk_list is not None 
    print(f"retrieved_chunk called on {chunk_list}")
    module = current_module(name)

    module.lock.acquire()
    module.pending = False
    actr.schedule_set_buffer_chunk("retrieval",chunk_list,0,"declarative",":max")
    module.lock.release()

actr.add_command('retrieved-chunk',retrieved_chunk,'Python declarative module successful retrieval event.')


def retrieval_failure(name):
    print("Retrieval failure")
    module = current_module(name)

    module.lock.acquire()
    module.pending = False
    module.error = True
    actr.call_command("set-buffer-failure","retrieval")
    module.lock.release()

actr.add_command('retrieval-failure',retrieval_failure,'Python declarative module unsuccessful retrieval event.')

actr.add_command('start-retrieval',None,'Signal for the start of a retrieval request')



# Module interface functions

# Called by Lisp ACT-R to create the declarative (now HDM) module
def create (name):
    global hdm_modules
    # create HDM python object and store in hdm_modules dictionary so
    # `current_module(name)` can return it
    hdm_modules[name.lower()] = HDM(time_scale=10e-3)
    return name

actr.add_command('create-pDM',create,'Creation function for Python holographic declarative module.')


def delete (name):
    global hdm_modules

    del hdm_modules[name.lower()] 

actr.add_command('delete-pDM',delete,'Deletion function for Python holographic declarative module.')


def reset (name):
    current_module(name).reset()

actr.add_command('reset-pDM',reset,'Reset function for Python holographic declarative module')


def query(name,buffer,slot,value):
    # from name, get module from function that indexes dictionary
    module = current_module(name)
    s = slot.lower()

    # make it lowercase if it can be
    if hasattr(value,'lower'):
        v = value.lower()
    else:
        v = value
    #get properties from module object
    module.lock.acquire()
    pending = module.pending
    error = module.error
    module.lock.release()

    # if user queried if state = free/busy/pending, return boolean 
    # based on module object current attributes, otherwise return err
    if s == 'state':
        if v == 'free':
            return not(pending)
        elif v == 'busy':
            return pending
        elif v == 'error':
            return error
        else:
            actr.print_warning('Unknown state query %s to declarative module' % v)
            return False
    else:
        actr.print_warning('Unknown query %s %s to declarative module' % (s,v))
        return False

actr.add_command('query-pDM',query,'Query function for Python declarative module')

# 
def request (name,buffer,spec):

    module = current_module(name)

    module.lock.acquire()

    module.error = False

    if module.pending :
        actr.call_command("model_warning","A retrieval event has been aborted by a new request")
        actr.call_command("delete-event",module.pending)
        module.pending = False


    actr.schedule_event_now("start-retrieval",None,"declarative",output="medium")

    
    # format ACT-R request into a usable format for the HDM object's request
    # function 
    try:
        request_chunk_args = actr.chunk_spec_to_chunk_def(spec)
        if module.verbose:
            print(f"Creating request chunk with args {request_chunk_args}")
            print(f"Full request spec: {actr.chunk_spec_slot_spec(spec)}")
        
        # get request parameters
        # get slots/values and parameters/values in request
        slots_vals = actr.chunk_spec_slot_spec(spec)
        kwargs = {}
        # add params/values to kwargs
        for p in slots_vals:
            # format returned by chunk-spec-slot-spec is ["=", "param", "val"] for
            # each slot/val or param/val pair
            assert len(p) == 3
            op, par, val = p[0], p[1], p[2] 
            assert isinstance(par, str)
            if par.startswith(":"): # this is a param/val pair!
                # get rid of ":" and replace "-" with "_" so python doesn't get
                # mad
                par = par.lstrip(":")
                par = par.replace("-", "_")
                par = par.lower()
                if isinstance(val, str):
                    # val = val.replace("-", "_")
                    val = val.lower()
                kwargs[par] = val
        request_chunk = Chunk(request_chunk_args, request=True, check_defined=False)
    except Exception as e:
        actr.print_warning(f"Error reading request spec into HDM: {e}")
        module.lock.release()
        return
    if module.verbose: print(f"Requesting chunk {request_chunk}")
    # Use HDM to check similarity btwn query and memory vectors and construct a
    # retrieved chunk from memory
    match = module.request(request_chunk, **kwargs)
    if module.verbose: print(f"Match: {match}")
    
    # if :esc is t then :lf controls the timing
    if module.esc :
        time = module.lf
    else:
        time = 0
     
    if match:
        #  put constructed chunk into ACT-R retrieval buffer if match found
        if hasattr(match, "activation"):
            logodds = module.cosine_to_logodds(match.activation)
        else:
            logodds = module.cosine_to_logodds(module.threshold)
        time=module.latency * math.exp(-logodds)
        if time>module.maximum_time: 
            time=module.maximum_time 
        module.pending = actr.schedule_event_relative(time,"retrieved-chunk",match.to_flat_list(),"declarative",destination="declarative",output="medium")
    else:
		# otherwise trigger ACT-R retrieval failure
        logodds = module.cosine_to_logodds(module.threshold)
        time=module.latency * math.exp(-logodds)
        if time>module.maximum_time: 
            time=module.maximum_time 
        module.pending = actr.schedule_event_relative(time,"retrieval-failure",None,"declarative",destination="declarative",output="medium")

    # should always free the chunk-spec resources when no longer needed
    actr.release_chunk_spec(spec)
    module.lock.release()

actr.add_command('request-pDM',request,'Request function for Python declarative module')

def sgp(*args):
    return actr.call_command("sgp", args)

# can be used to set or get module parameters called by sgp if param owned by
# HDM rather than directly
#
# if just param name, return it if param name and value, set named param to
# that value and return it if valid handles either one param arg from Lisp
# ACT-R code or multiple args for my code since sgp doesn't seem to be working
# over remote python connection 
def params (name, argsl):
    
    # print(f"input to param is: {name} with {argsl}")
    try:
        # prepare lisp side arguments for python argument parser
        #
        # Lisp's `false` is `nil` which becomes `None` over connection. We turn
        # them into empty strings because argparse bool interprets anything
        # else as True 
        argsl = [a if a != None else "" for a in argsl]
        # argparse takes strings
        argsl = [str(a) for a in argsl]
        # lisp isn't case sensitive
        argsl = [a.lower() for a in argsl] 
        # lisp uses ":param" syntax, argparse uses --param for arg options
        argsl = [a.replace(":", "--") for a in argsl]
        # print(f"New arsgl is {argsl}")
    except Exception as e:
        actr.print_warning(f"(params) arguments formatted incorrectly: {e}")
        return
    try:
        # get HDM object
        module = current_module(name)
        if module.verbose: print("params called")
    except:
        # TODO: set global settings here
        actr.print_warning(f"module {name} not defined!")
        return
    module.lock.acquire()

    # set parser to option GET if we're getting the specified parameter instead
    # of setting it
    class Option(Enum):
        GET = 1
    parser = LispArgParser(prog="params")
    # TODO: maybe LispArgParser method to eliminate redundancy below?
    parser.add_argument("--lf", nargs="?", const=Option.GET, type=float)
    parser.add_argument("--esc", nargs="?", const=Option.GET, type=bool)
    parser.add_argument("--ans", nargs="?",  const=Option.GET, type=float)
    parser.add_argument("--rt", nargs="?",  const=Option.GET, type=float)
    parser.add_argument("--bll", nargs="?",  const=Option.GET, type=float)
    parser.add_argument("--hdm-v", nargs="?",  const=Option.GET, type=bool)
    parser.add_argument("--hdm-k", nargs="?", const=Option.GET, type=int)
    parser.add_argument("--pull-slots", nargs="?", const=Option.GET, type=bool)
    parser.add_argument("--time-scale", nargs="?", const=Option.GET, type=float)
    parser.add_argument("--slot-pulling-threshold", nargs="?", 
                        const=Option.GET, type=float)
    parser.add_argument("--hdm-t", nargs="?", const=Option.GET, type=int)
    parser.add_argument("--hdm-o", nargs="?", const=Option.GET, type=int)
    parser.add_argument("--slot-pulling-approach", nargs="?", const=Option.GET, type=str)
    parser.add_argument("--slot-pulling-n", nargs="?", const=Option.GET, type=int)
    parser.add_argument("--log-outcomes", nargs="?", const=Option.GET, type=str)
    # argument for trying to get every single param
    parser.add_argument("--get-all-params", nargs="?", const=Option.GET, type=str)
    # try to parse arguments into args
    try:
        args = parser.parse_args(argsl)
    except Exception as e:
        print(f"Error specifying HDM parameter: {e}")
        module.lock.release()
        return
    
    # internal helper function to warn users that changing a parameter will
    # require resetting the model 
    def warn_reset(p):
        if module.verbose:
            actr.print_warning(f"Resetting parameter {p} will reset HDM.")
    # 
    # loop over all param k, value v (or GET) pairs
    # in namespace params not specified should be set to None by argparser
    arg_params = []
    reset = False
    for k, v in vars(args).items():
        if v is not None: 
            # param being set or gotten
            arg_params.append(k)
            if v is not Option.GET: 
                # then we're in case where param is being set
                try:
                    match k:
                        # as per arg preprocessing above, these should all be
                        # lowercase and with "-" replaced with "_" 
                        case "lf":
                            module.lf = args.lf
                        case "esc":
                            module.esc = args.esc
                        case "ans":
                            module.ans = args.ans
                        case "rt":
                            module.rt = args.rt
                        case "bll":
                            module.bll = args.bll
                        case "hdm_v":
                            module.verbose = args.hdm_v
                        case "hdm_k":
                            module.N = args.hdm_k
                            warn_reset("N (HDM encoding dimension)")
                            reset = True
                        case "pull_slots":
                            module.pull_slots = args.pull_slots
                        case "time_scale":
                            module.time_scale = args.time_scale
                            warn_reset("time scale")
                            reset = True
                        case "slot_pulling_threshold":
                            module.slot_pulling_threshold = args.slot_pulling_threshold
                        case "hdm_t":
                            module.T = args.hdm_t
                            warn_reset("T (learning context vector dimension)")
                            reset = True
                        case "hdm_o":
                            module.O = args.hdm_o
                            warn_reset("O (oscillator number)")
                            reset = True
                        case "slot_pulling_approach":
                            module.slot_pulling_approach = args.slot_pulling_approach
                        case "slot_pulling_n":
                            module.slot_pulling_n = args.slot_pulling_n
                        case "log_outcomes":
                            module.log_outcomes = args.log_outcomes
                        case _:
                            actr.print_warning(f"{k} is not an HDM parameter")
                            # don't add this invalid parameter to argument
                            # param list or there will be an error later since
                            # its return value can't be specified
                            arg_params.pop()
                except Exception as e:
                    actr.print_warning(f"Error setting specified HDM parameters {e}")
                    module.lock.release()
                    return
    # whether set/get case, return parameter value(s)
    pars = {"lf": module.lf, "esc": module.esc, 
            "ans": module.ans, "rt": module.rt, "bll": module.bll,
            "hdm_v": module.verbose,
            "hdm_k": module.N, "pull_slots": module.pull_slots,
            "time_scale": module.time_scale, 
            "slot_pulling_threshold": module.slot_pulling_threshold,
            "hdm_t": module.T, "hdm_o": module.O,
            "slot_pulling_approach": module.slot_pulling_approach,
            "slot_pulling_n": module.slot_pulling_n,
            "log_outcomes": module.log_outcomes}
    # if --get-all-params is an argument, return dictionary of all param names -
    # values. usually used for logging
    try:
        if args.get_all_params is not None:
            # return everything
            module.lock.release()
            return pars
    except:
        print("error accessing get_all_params this way")
        module.lock.release()
        return
    
    ret_vals = [pars[p] for p in arg_params]
    # Lisp-side calls - just one parameter set/get at a time
    if len(ret_vals) == 1:
        ret_vals = ret_vals[0]
    # None of the arguments were HDM parameters
    elif len(ret_vals) == 0:
        actr.print_warning("None of the arguments matched an HDM parameter")
        ret_vals = None
    module.lock.release()
    # If required after changing a parameter need to do this after releasing
    # because reset() itself needs to acquire a lock
    if reset:
        module.reset()
    return ret_vals

actr.add_command('params-pDM',params,'Parameter function for Python declarative module')


def buffer_cleared(name,buffer,chunk):

    module = current_module(name)

    module.lock.acquire()

    # create a chunk-spec that describes the chunk and use ACT-R's matching
    # to search the list of chunks for a match

    spec = actr.define_chunk_spec(chunk)


    module.lock.release()

actr.add_command('cleared-pDM',buffer_cleared,'Chunk cleared from a buffer function for Python declarative module')


# Define the module with a buffer called retrieval, add the :lf parameter, monitor the :esc parameter,
# and get notified when a buffer is cleared.
actr.define_module('declarative', # module name
                   
                   [['retrieval', None, [':slot-pull', ':approach', ':threshold', ':N'], None, None, None]],
                    #  buffer-def, with the buffer-name specified without any parameters
                   # remote parameters, where "owner" is whether this module
                   # and only this module owns this parameter:
                   [[':lf', [['owner',True],['valid-test','nonneg'], # use an internal ACT-R function to test it
                             ['default-value',1.0],['warning','non-negative number'],
                             ['documentation','Latency Factor (from Python)']]],
                    [':esc',[['owner',False]]],
                    [':ans',[['owner',True], ['default-value', 0.0], 
                                ['documentation', ":ans from act-r test addd"]]],
                    [':rt',[['owner',True], ['default-value', 0.0], 
                                ['documentation', ":rt from act-r test addd"]]],
                    [':bll',[['owner',True], ['default-value', 0.0], 
                                ['documentation', ":bll from act-r test addd"]]],

                    [':hdm-v', [['owner',True], ['default-value', False], 
                                ['documentation', "HDM Output Verbosity"]]],
                    [':hdm-k', [['owner', True], ['default-value', 512],
                                ['documentation', 'HDM HRR encoding dimension']]],
                    [':pull-slots', [['owner', True], ['default-value',True],
                                     ['documentation', 'Attempt to retrieve entire chunk by guessing slots to add']]],
                    [':time-scale', [['owner', True], ['default-value', 10e-5], 
                                     ['documentation', 'Time scale for temporal oscillators.']]],
                    [':slot-pulling-threshold', [['owner', True], ['default-value', 0.1],
                                                 ['documentation', 'Pull potential slots above this similarity threshold']]],
                    [':hdm-T', [['owner', True], ['default-value', 320],
                                ['documentation', 'Number of Elements in Time Learning Context Vector']]],
                    [':hdm-O', [['owner', True], ['default-value', 15],
                                ['documentation', 'Number of oscillators drawn from to make Time Learning Context Vector']]],
                    [':slot-pulling-approach', [['owner', True], ['default-value', 'threshold'],
                                                ['documentation',
                                                 ("threshold - pull slots with similarity above :slot-pulling-threshold \n"
                                                  "top-N - pull the top :slot-pulling-n most similar slots")]]],
                    [':slot-pulling-N', [['owner', True], ['default-value', 4],
                                         ['documentation',
                                          ("the number of top most similar slots to pull when "
                                           ":slot-pulling-approach is set to top-N. no effect otherwise.")]]],
                    [':log-outcomes', [['owner', True], ['default-value', None],
                                         ['documentation',
                                          "log retrieved chunks to given file name"]]]
                    ],
                   [['version','1.1P'],
                    ['documentation','HDM modified from simple_declarative.py.'],
                    ['creation','create-pDM'],['delete','delete-pDM'],['query','query-pDM'],['request','request-pDM'],
                    ['notify-on-clear','cleared-pDM'],['reset','reset-pDM'],
                    ['params','params-pDM']])



# This function is going to be callable from within productions just
# like the original ACT-R add-dm command.
#
# If there is a current model, pass the parameters off to define-chunks
# to create them and then add all of the created chunks into DM and
# return the names of those chunks.
def add_dm_generic(chunk_defs, delete_after=True):
    # don't process empty/invalid calls
    if chunk_defs is None or (not hasattr(chunk_defs, "__len__")) or len(chunk_defs) == 0:
        return
    print("Calling add_dm on chunk defs: ", chunk_defs)
    model = actr.current_model()
    if not(model):
        actr.print_warning('Add-dm called with no current model.')
        return False
    module = current_module(model)
    module.lock.acquire()
    
    try:
        # Define the chunks in ACT-R memory so we can get chunk names (and later
        # slot-value pairs) from chunk defs. This way we don't need to validated
        # and format the chunk defintion inputs into chunks ourselves. If
        # delete_after = True, then we will later delete them from memory so they
        # don't continue to take up space.
        chunk_names = actr.define_chunks(*chunk_defs)
        # If the chunk_defs don't form a valid chunk, stop. Error messages were
        # already handled by ACT-R in the call to define_chunks.
        if chunk_names is None:
            module.lock.release()
            return
        # Add each chunk
        for cn in chunk_names:
            # check that the chunk was successfully defined
            if cn is not None and actr.chunk_p(cn) is not None:
                # don't actually need to pass in chunk args since already
                # defined in ACT-R chunk memory
                chunk_i = Chunk(None, cn, has_slots=True, check_defined=True)
                module.add_chunk_to_dm(chunk_i)
                print("..............n")
                print(chunk_i)
                if delete_after:
                    # TODO: suppress ACT-R warnings about this 
                    actr.delete_chunk(cn)
        module.lock.release()
        return chunk_names
    except Exception as err:
        actr.print_warning(f"HDM error adding chunk to memory: {err}")
        module.lock.release()
 
 # Takes a (possibly recursively nested) list of slots and values from Lisp's
 # add-dm command. We set delete_after to true because HDM doesn't store chunks
 # in memory.
def add_dm(*chunk_defs):
    return add_dm_generic(chunk_defs, delete_after=True)

actr.add_command('add-dm',add_dm,'Add chunks to holographic declarative memory.',True,"add-dm",True)

def add_goal_dm(*chunk_defs):
    return add_dm_generic(chunk_defs, delete_after=False)

actr.add_command('add-goal-dm', add_goal_dm, 
    "Add a goal to HDM, so keep the chunks defined in memory unlike normal.",
     True, "add-goal-dm", True)


# currently takes a simple tuple list of strings 
#
# TODO: modify so it takes either tuple list of strings or tuple of arbitrarily
# nested string arrays using recursion
def add_values_dm(*vals):
    print("Calling add_values_dm on values: ", vals)
    model = actr.current_model()
    if not(model):
        actr.print_warning('Add-values-dm called with no current model.')
        return False
    # Making sure vals is a valid tuple of strings
    if vals is None or (not hasattr(vals, "__len__")) or len(vals) == 0:
        return
    # Enforce current requirement that add-values-dm only takes a flat list of
    # strings
    for V in vals:
        if V is None or (not isinstance(V, str)):
            return
    module = current_module(model)
    module.lock.acquire()
    chunk = Chunk(list(vals), has_slots=False)
    module.add_chunk_to_dm(chunk)
    module.lock.release()
    return
    
actr.add_command('add-values-dm', add_values_dm, "Add only values, not slot/chunk pairs to HDM", True,"add-values-dm",True)


# arguments: filename in, filename out
# (if not provided it's "[filename_in]_out"), and encoding (if not provided
# uses system default)
def preprocess_text(*raw_args):
    # lisp arguments
    parser = LispArgParser(prog="preprocess-text")
    parser.add_argument("fname_in", help="input file name of plaintext file")
    parser.add_argument("fname_out", nargs="?",
                        help="output file name. default: input file name with 'out' appended")
    parser.add_argument("encoding", nargs="?",
                        help="input and output file encoding, otherwise use system default")
    parser.add_argument("max_line", nargs="?", type=int,
                        help="if provided, only read up to this many lines of input")
    parser.add_argument("max_sent_len", nargs="?", type=int)
    try:
        args = parser.parse_args(raw_args)
        # get filenames as paths to avoid backslash escape issues
        args.fname_in = Path(args.fname_in)
        # set default name of out file
        if args.fname_out is None:
            # append _out before file extension e.g. a.txt --> a_out.txt 
            args.fname_out = args.fname_in.with_stem(args.fname_in.stem + "_out")
        else:
            args.fname_out = Path(args.fname_out)
        if args.max_sent_len is None: args.max_sent_len = 100
    except Exception as err:
        print(err)
        return 
    print(args.fname_in)
    # if len(args) < 2 or len(args) > 3:
    #     actr.print_warning("Invalid number of arguments - format is [input filename] [output filename] [encoding (optional)]")
    # fname_in, fname_out = args[0], args[1]
    # encoding = None
    # if len(args) > 2:
        # encoding = args[2]
    # actr.model_output("preprocess-text takes in a plaintext file")
    # actr.print_warning("preprocess-text takes in a plaintext file")
    # MIN_SENT_LEN = 2
    # MAX_SENT_LEN = 100
    try: 
        with (open(args.fname_in, mode='r', encoding=args.encoding) as fo_in,
              open(args.fname_out, mode='w', encoding=args.encoding) as fo_out):
            i = 0
            for line in fo_in:
                if args.max_line is not None and i > args.max_line - 1:
                    break
                sentences = sent_tokenize(line)
                # print(sentences)
                words = [word_tokenize(s) for s in sentences]
                # remove sentences with too few or too many words
                words = [s for s in words if len(s) <= args.max_sent_len]
                # set lowercase
                words = [[w.lower() for w in s] for s in words]
                # remove stopwords
                stopwords_list = set(stopwords.words('english'))
                # # remove UNKNOWN_STR and "?" because it interferes with HDM's input
                # stopwords_list.add(UNKNOWN_STR)
                # stopwords_list.add("?")
                filtered_words = [[w for w in s if w not in stopwords_list]
                                  for s in words]
                # put words in each sentence back together, and add newline for each sentence
                joined_words = [" ".join(s) + "\n" for s in filtered_words]
                # combine sentences into string and write to out file
                joined_sents = " ".join(joined_words)
                # print(joined_sents)
                fo_out.write(joined_sents)
                i += 1 
            actr.print_warning(f"{i} lines preprocessed")
    except Exception as e:
        actr.print_warning(f"Error reading in input file and/or writing to output file: \n {e}")
        return
actr.add_command('preprocess-text', preprocess_text,'Prepare an input file to be read into HDM.',True,"preprocess-text")

# Read a file with given name into memory
# Assumes it's already been preprocessed with process_text.py 
# Arguments: filename, optional encoding (default is system default)
def read_corpus_hdm(*raw_args):
    # read in arguments
    parser = LispArgParser(prog="read-corpus-hdm", 
                           description="read a plaintext file sentence by sentence into HDM")
    parser.add_argument("fname", help="input file name of plaintext file")
    parser.add_argument("encoding", nargs="?",
                        help = "input and output file encoding, otherwise use system default")
    try:
        args = parser.parse_args(raw_args)
        args.fname = Path(args.fname)
    except Exception as err:
        # LispArgParser will print errors/help message out to ACT-R lisp
        # terminal, so need to worry about that here. just printing python
        # error message to python terminal if needed
        print(err)
        return
    # if len(args) < 0 or len(args) > 2:
    #     actr.print_warning("Invalid parameters - format is [filename] [encoding (optional)]")
    # if len(args) == 2:
    #     encoding = args[1]
    # fname = args[0]
    # encoding = None
    model = actr.current_model()
    # actr.model_output("read-corpus-hdm takes in a file output by preprocess-text")
    if not(model):
        actr.print_warning('read-corpus-hdm called with no current model.')
        return False
    module = current_module(model)
    module.lock.acquire()
    try:
        # read line by line i.e. sentence by sentence
        with open(args.fname, mode="r", encoding=args.encoding) as fo:
                line_i = 1
                for line in fo:
                    start_time = perf_counter()
                    line = line.rstrip(".\n").rstrip(" ") 
                    words = line.split(" ")
                    # Debugging: Print line #, 1st 10 characters of sentence, num words 
                    if module.verbose: 
                        print(f"{line_i}. \"{line[:10]:10}\" | {len(words):2}w | ", end="")
                    # make a values-list chunk out of the list of words
                    chunk = Chunk(words, None, 
                                has_slots=False,
                                check_defined=False,
                                store_chunk=False)
                    print("printing chunk")
                    print(chunk)
                    # add chunk representing sentence to HDM memory
                    module.add_chunk_to_dm(chunk)
                    if module.verbose:
                        # how long did adding chunk take?
                        end_time = perf_counter()
                        time_elapsed = (end_time - start_time) * 1000
                        print(f"{(end_time - start_time):.2f}ms")
                    line_i += 1
                actr.model_output(f"Read in {line_i-1} sentences to HDM")
    except Exception as err:
        actr.print_warning(f"Error reading file into HDM: {err}")
    module.lock.release()
actr.add_command('read-corpus-hdm', read_corpus_hdm,'Read a formatted corpus file into HDM.',True,"read-corpus-hdm")

# This replaces the original ACT-R dm command which can be used
# to print out all the chunks in DM or a specified subset of them.
# Prints list of tokens in memory vector space and displays a graph of them
# Currently uses PCA to reduce to two dimensions, but considering nonlinear
# dimensionality reduction methods like t-SNE and UMAP
# Takes a list of terms (not chunk names, those aren't stored!)
def dm(*tokens):    
    # actr.print_warning("Not yet implemented")
    # raise Exception("Not yet implemented")
    model = actr.current_model()
    if not(model):
        actr.print_warning('(dm) called with no current model.')
        return(False)

    else:
        module = current_module(model)
        module.lock.acquire()
        # get the names of values "keys" and their corresponding memory vectors
        # "values"

        try:
            keys, values = module.mem.keys(), module.mem.values()
            slots = module.slots.keys()
            # not sure how to do newline through interface...
            actr.model_output("HDM does not store individual chunks, printing stored memory slots/vals instead")
            keys_sorted = sorted(keys)
            slots_sorted = sorted(slots)
            actr.model_output("Slots:")
            for s in slots_sorted:
                # if not s.startswith("T_"):
                actr.model_output(s)
            actr.model_output("-"*10)
            actr.model_output("Values:")
            for k in keys_sorted:
                actr.model_output(k)
        except Exception as e:
            actr.print_warning(f"Error while accessing and printing slots and values list: \n {e}")
            module.lock.release()
            return
        try:
            if tokens != ():
                # select subset of chunks to graph
                # check each one is valid
                actr.model_output("Only graphing terms given as arguments")
                new_keys = []
                new_values = []
                for term in tokens:
                    if term in keys:
                        new_keys.append(term)
                        new_values.append(module.mem[term])
                    else:
                        actr.print_warning(f"Token {term} not stored in memory. Terms must be values.")
                keys = new_keys
                values = new_values
        except Exception as e:
            actr.print_warning(f"Error accessing given tokens from memory: \n {e}")
            module.lock.release()
        if len(values) < 2:
            if len(values) > 0:
                # PCA's algorithm requires at least three points to project
                # them onto 2D space
                actr.print_warning("Must specify at least 3 points to graph.")
            # if no terms were given, just return 
            module.lock.release()
            return
        mem_vecs = [hrr.v for hrr in list(values)]
        mem_keys = list(keys)
        module.lock.release()

        try:
            mem_vecs = np.vstack(mem_vecs)
            mem_vecs = StandardScaler().fit_transform(mem_vecs)
            mem_emb = PCA(n_components=2).fit_transform(mem_vecs)
            plt.scatter(mem_emb[:,0], mem_emb[:,1], c="m")
            for i in range(len(mem_keys)):
                # truncate and replace with ... if too long
                mem_key = mem_keys[i]
                if len(mem_key) > 10:
                    mem_key = mem_key[:7] + "..."
                plt.annotate(mem_key, (mem_emb[i,0] + 0.15, mem_emb[i,1] + 0.15))
            actr.model_output("-"*10)
            actr.model_output("Displaying a graph of memory vectors. Close graph window to continue.")
            plt.show()
        except Exception as e:
            actr.print_warning(f"Error graphing HDM memory: \n {e}")
        return

actr.add_command('dm',dm,'Print chunks from Python declarative memory.',True,"dm")


# Replace the original ACT-R sdp command with this simplified version
# which only serves to print the parameters for the indicated DM chunks.

def sdp(*chunks):

    actr.print_warning("Not yet implemented")
    raise Exception("Not yet implemented")
    model = actr.current_model()

    if not(model):
        actr.print_warning('Sdp called with no current model.')
        return(False)

    else:
        module = current_module(model)

        module.lock.acquire()

        current_chunks=module.chunks

        module.lock.release()

        r = []

        if chunks == ():

            for c in current_chunks:
                ct = actr.call_command("chunk-ct",c)
                count = actr.call_command("chunk-count",c)
                actr.command_output("Paramters for chunk %s created: %d current count: %d" % (c,ct,count))
                r.append([c,ct,count])

        else:
            for c in chunks:
                if c in current_chunks:

                    ct = actr.call_command("chunk-ct",c)
                    count = actr.call_command("chunk-count",c)
                    actr.command_output("Paramters for chunk %s created: %d current count: %d" % (c,ct,count))
                    r.append([c,ct,count])

        return (r)

actr.add_command('sdp',sdp,'Print chunk parameters for chunks in Python declarative memory.',True,"sdp")

class Finst:
  def __init__(self,parent,size=4,time=3.0):
    self.parent=parent
    self.size=size
    self.time=time
    self.obj=[]
  def contains(self,o):
    return o in self.obj
  def add(self,o):
    if self.size==0: return
    self.obj.append(o)
    if len(self.obj)>self.size:
      self.remove(self.obj[0])
    # self.parent.sch.add(self.remove,args=[o],delay=self.time)
  def remove(self,o):
    if o in self.obj: self.obj.remove(o)
