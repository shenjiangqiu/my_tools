#!/usr/bin/python3
import sys
import os
import re

import argparse
parser=argparse.ArgumentParser(description="get the data from result file")
parser.add_argument("-k","--keys",dest="keys",required=True,help="which key to collect")
parser.add_argument("-n","--num",dest="num",type=int,default=0,help="how many result you want to keep,0=keep\
    all result")
parser.add_argument("result_files",nargs="*")
#parser.add_argument("-o","--output",dest="output",default="out.txt")
parser.add_argument("--norm",dest="norm",action="store_true",default=False,help="true: print normalized data instead of real one")

arg_result=parser.parse_args()

keys=arg_result.keys.split()

patterns=[key+"  *(.*)" for key in keys ]
is_norm=arg_result.norm
num=int(arg_result.num)
result=dict()
progs=[re.compile(pattern) for pattern in patterns]

for file in arg_result.result_files:
    with open(file) as f:
        result[file]=dict()
        content=f.read()
        for i,(k,prog) in enumerate(zip(keys,progs)):
            result[file][k]=prog.findall(content)
            result[file][k]=[int(v) for v in result[file][k]]
    # print out
    print(file)
    for key in keys:
        print(key,end=" ")
        if result[file][key]==None or len(result[file][key])==0:
            print("")
            continue
        max_num=1
        if is_norm:
            max_num=max(result[file][key])
        else:
            max_num=1
        if num!=0:
            for number in result[file][key][-num:]:
                print(number/max_num,end=" ")
        else:
            for number in result[file][key]:
                print(number/max_num,end=" ")
        print("")