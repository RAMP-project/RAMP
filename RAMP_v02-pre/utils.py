# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:53:30 2019

@author: FLomb
"""

import pickle

#%%

def save_obj(obj, name ):
    with open('results/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('results/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)