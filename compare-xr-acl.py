#!/usr/bin/env python
from genie.testbed import load
from genie.utils.diff import Diff
import ast
import json
import argparse


parser = argparse.ArgumentParser()

#parser.add_argument('--acl_id', dest='acl_id', type=str)
parser.add_argument('--acl_id', type=str)
acl_id = parser.parse_args()
#print(acl_id.acl_id)


# Load the different testbeds for base router and comparing routers
testbed_2 = load('xr-tb-2.yaml')

#Connect to xe1 and extract ACLs
#xr1=testbed_1.devices['xr1']
#xr1.connect(log_stdout=False)
#acl_list = xr1.parse('show access-list afi-all')

base_acl=open('100-base-acl.json','r')

contents=base_acl.read()
orig_acl=ast.literal_eval(contents)
#print(type(orig_acl))

#with open('100-base-acl.json', 'r') as base_acl:
#acl_id = '100'

for name,dev in testbed_2.devices.items():
    dev.connect(log_stdout=False)
    all_acl=dev.parse('show access-list afi-all')
    compare_acl=(all_acl[acl_id.acl_id])
    diff = Diff(orig_acl, compare_acl)
    diff.findDiff()
    if str(diff):
        print(f'ACL {acl_id.acl_id} on router {name} is not compliant')
    else:
        print(f'ACL {acl_id.acl_id} on router {name} is compliant')
