from shutil import copyfile
import os
from random import shuffle
from math import floor



def split_train_test(data_dir,train_dir,test_dir,split=0.8):
    all_files = [os.path.join(data_dir,f) for f in os.listdir(data_dir)]
    file_list = list(filter(lambda file: file.endswith('.mid'), all_files))
    file_list = sorted(file_list)
    shuffle(file_list)
    full_size = sum(os.path.getsize(os.path.join(data_dir,f)) for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir,f)))
    split_size = full_size * split
    os.mkdir(train_dir)
    total_size = 0
    i = 0
    while total_size < split_size:
        f = file_list[i]
        total_size += os.path.getsize(f)
        name = os.path.basename(f)
        copyfile(f,os.path.join(train_dir,name))
        i+=1
    os.mkdir(test_dir)
    for f in file_list[i:]:
    	name = os.path.basename(f)
    	copyfile(f,os.path.join(test_dir,name))
