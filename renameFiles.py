# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 22:30:15 2023

@author: 820763897
"""
from os import listdir,rename
from os.path import isfile, join

IMAGE_DIR = r'C:\Users\820763897\Videos\CCC\FlyEmbryoZstack\z_stack_2023-04-27_135417_E2_Z5\\'
#IMAGE_DIR = r'C:\Users\820763897\Videos\CCC\FlyEmbryoZstack\test\\'

files = [f for f in listdir(IMAGE_DIR) if isfile(join(IMAGE_DIR, f))]

for i in range(0,len(files)):
    src=IMAGE_DIR+files[i]
    dst=IMAGE_DIR+str(i)+'.jpg'
    print('old',src)
    print('new',dst)
    print()
    rename(src, dst)
