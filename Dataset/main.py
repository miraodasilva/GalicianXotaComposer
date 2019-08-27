#!/usr/bin/env python
# -*- coding: utf-8 -*-

from download_midis import download_dataset
from separate_tracks import separate_tracks
from magenta_conversion import create_tf_record,create_sequence_examples
from split_train_test import split_train_test
from augment_data import augment_data
import codecs
import pickle
midis_dir = "./midis/"
mono_midis_dir = "./mono_midis/"
mono_midis_train = "./mono_midis_train/"
mono_midis_train_aug = "./mono_midis_train_aug/"
mono_midis_test = "./mono_midis_test/"
tf_record_train = "./tfrecord_train/"
tf_record_test = "./tfrecord_test/"
sequence_examples_train = "./sequence_example_train/"
sequence_examples_test = "./sequence_example_test/"



#Download MIDI files
"""
meta = download_dataset(midis_dir)
print(meta)
#Separate tracks into monophonic MIDI files
meta = separate_tracks(midis_dir,mono_midis_dir,meta)
print(meta)

f = codecs.open("./data_meta_info.txt","w",encoding="utf-8")

#Filter bad files
meta = [i for i in meta if len(i)==5]

for name,link,file,tracks,length in meta:
	f.write("Name: %s , Link: %s , File: %s, Tracks: %s, Length: %s \n" % (name,link,file,tracks,length))
f.close()


split_train_test(mono_midis_dir,mono_midis_train,mono_midis_test)

#augment training data
augment_data(mono_midis_train,mono_midis_train_aug)
"""
mono_midis_train = mono_midis_train_aug
#Create tfrecord which compiles all monophonic MIDI files

create_tf_record(mono_midis_train,tf_record_train)
create_tf_record(mono_midis_test,tf_record_test)
#create sequence examples based on the tf record
create_sequence_examples(tf_record_train+"dataset.tfrecord",sequence_examples_train)
create_sequence_examples(tf_record_test+"dataset.tfrecord",sequence_examples_test)





