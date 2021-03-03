#!/usr/bin/env python
from genie.testbed import load
from genie.utils.diff import Diff
import ast
import json
import argparse
from tabulate import tabulate


# configure the argment extension to the script
parser = argparse.ArgumentParser()
parser.add_argument('--acl_id', type=str)
acl_id = parser.parse_args()


# Load the testbeds for base router and comparing routers
testbed = load('tb-all.yml')


# Load template ACL to compare to
base_acl=open('100-base-acl.json','r')
contents=base_acl.read()
orig_acl=ast.literal_eval(contents)

tr=[]
# Run the diff to compare ACLs from the different routers.
for name,dev in testbed.devices.items():
    dev.connect(log_stdout=False)
    all_acl=dev.parse('show access-list afi-all')
    compare_acl=(all_acl[acl_id.acl_id])
    diff = Diff(orig_acl, compare_acl)
    diff.findDiff()
    if str(diff):
        status='non-compliant'
    else:
        status='compliant'
    tr.append((name,acl_id.acl_id,status))

print('\n')
print(tabulate(tr, headers=['Router', 'ACL-ID', 'Compliance']))
print('\n')