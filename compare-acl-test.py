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


testbed = load('tb.yml')

base_acl=open('100-base-acl.json','r')

contents=base_acl.read()
orig_acl=ast.literal_eval(contents)

print(orig_acl)

for name,dev in testbed.devices.items():
    dev.connect(log_stdout=False)
    all_acl=dev.parse('show access-list afi-all')
    compare_acl=(all_acl[acl_id.acl_id])

print('\n')
print(compare_acl)