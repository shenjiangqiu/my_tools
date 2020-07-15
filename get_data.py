#!/usr/bin/python3
import sys
import os
import re
import numpy as np
import argparse
parser = argparse.ArgumentParser(description="get the data from result file")
parser.add_argument("-k", "--keys", dest="keys",
                    required=True, help="which key to collect")
parser.add_argument("-n", "--num", dest="num", type=int, default=0, help="how many result you want to keep,0=keep\
    all result")
parser.add_argument("result_files", nargs="*")
# parser.add_argument("-o","--output",dest="output",default="out.txt")
parser.add_argument("--norm", dest="norm", action="store_true",
                    default=False, help="true: print normalized data instead of real one")
parser.add_argument("--print-most", dest="print_most",
                    action="store", default=0,type=int)
arg_result = parser.parse_args()

keys = arg_result.keys.split()

patterns = [key+"  *(.*)" for key in keys]
is_norm = arg_result.norm
num = int(arg_result.num)
result = dict()
progs = [re.compile(pattern) for pattern in patterns]

for file in arg_result.result_files:
    with open(file) as f:
        result[file] = dict()
        content = f.read()
        for i, (k, prog) in enumerate(zip(keys, progs)):
            result[file][k] = prog.findall(content)
            result[file][k] = np.array([int(v) for v in result[file][k]])
    # print out
    if len(result[file][keys[0]]) == 0:
        continue
    if arg_result.print_most>0:

        print(file)
        result[file]["d"] = np.zeros(len(result[file][keys[0]]))
        for k in keys[1:]:
            min_ = min(result[file][k])
            max_ = max(result[file][k])
            normed = (result[file][k]-min_)/(max_-min_)
            average=np.average(normed)
            dist=np.abs(normed-average)
            result[file]["d"]+=dist
        pass
        index=np.argsort(result[file]["d"])
        out_prop=result[file][keys[0]][index[0:arg_result.print_most]]
        print(out_prop)
        

        print(" ")

    else:
        print(file)
        for key in keys:
            print(key, end=" ")
            if result[file][key] == None or len(result[file][key]) == 0:
                print("")
                continue
            max_num = 1
            if is_norm:
                max_num = max(result[file][key])
            else:
                max_num = 1
            if num != 0:
                for number in result[file][key][-num:]:
                    print(number/max_num, end=" ")
            else:
                for number in result[file][key]:
                    print(number/max_num, end=" ")
            print("")
