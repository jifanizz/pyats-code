#!/usr/bin/env python

import pprint
from tabulate import tabulate


# Load testbed and connect to device
from genie.testbed import load

testbed = load('tb.yml')
uut = testbed.devices['abr']

# Connect to device
uut.connect(log_stdout=False)

# parse bgp beighbors
bgp_nbr=uut.parse('show bgp neighbors')

# filter neighbor values
nbr_ip=bgp_nbr['instance']['all']['vrf']['default']['neighbor']

# filter output
nbr_cnt=0
tr=[]
for nbr, vals in nbr_ip.items():
    state=vals['session_state']
    as_nbr=vals['remote_as']
    #print(nbr, state)
    tr.append((nbr,as_nbr,state))


    if state.lower()=='established':
        nbr_cnt += 1
    else:
        continue

# Print out
print(tabulate(tr, headers=['BGP Neibhbor', 'BGP AS', 'BGP State']))
print('\n')
print(f"Number of BGP established neighbors is {nbr_cnt}")


