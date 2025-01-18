#!/bin/bash 

if [ `uname` == "Linux" ];then
    python3_path="$PWD/lib/python3/bin/python3"
    $python3_path main.py -c config.yaml
elif [ `uname` == "Darwin" ];then 
    python3 main.py -c config.yaml 
fi
