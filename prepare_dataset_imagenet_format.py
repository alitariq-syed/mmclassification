# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:31:21 2023

@author: Ali
"""
import os
import numpy as np
import json

target_data_path = "E:/SwipBox/Dataset/"
subset='test'
path = target_data_path+subset
print(os.listdir(path))

file_list=[]
class_mapping = {'good':1,'bad':0}
for dirpath, dnames, fnames in os.walk(path):
    for f in fnames:
        if f.lower().endswith(".jpeg"):
            # print (f)
            img_class = dirpath.split('\\')[-1]
            targed_string = img_class+'/' + f + ' ' + str(class_mapping[img_class])
            file_list.append(targed_string)
            

np.savetxt(fname = target_data_path+subset+'_list.txt',X = file_list,fmt='%s')
