#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use python3 as it supports many encoding as copared to
# python2

# Using hashed value of all the sentences and storing them
# in a set and then checking if that alread exist.
# This saves memory as well as speeds up our processing.
# Useful especially when dealing with noisy data for 
# NLP tasks like NMT and many more where you have huge
# data like in Millions of line.

import uuid
import hashlib

hashSet = set()

def hash_sent(sent):
    # uuid is used to generate a random number
    return hashlib.md5(sent).hexdigest()

# input.txt is the original data file with duplicate lines
with open('dataset1.csv') as f:
    for line in f:
        sent = line.strip("\n")
        # print(sent)
        hashValue = hash_sent(sent.encode('utf-8')) # encoding for cases of special chars in sentence.
        # print(hashValue)
        if hashValue in hashSet:
            continue
        else:
            print(line.strip('\n'))
            hashSet.add(hashValue)

#  I used print only, If you wnat to write in a new file 
# change the code accordingly else just use `python3 deleteDuplicate.py > output.txt`