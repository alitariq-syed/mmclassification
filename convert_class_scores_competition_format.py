#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 16:13:51 2021

@author: ali
"""


import numpy as np
import json


base_dir = './tutorial_exps_C1/'

f = open(base_dir+'output_results.json')
results_dict = json.load(f)

formatted_results = []
for i in results_dict['class_scores']:
    print(i)
    formatted_results.append(str(i[0])+" "+ str(i[1])+" "+str(i[2]))
 
# Closing file
f.close()

formatted_results = np.asarray(formatted_results)
np.savetxt(fname=base_dir+'output_results_formatted.txt',X=formatted_results, fmt='%s')