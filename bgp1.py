#!/usr/bin/env python


import pprint


from genie.testbed import load

testbed = load('tb.yml')
uut = testbed.devices['abr']

# connect to it
uut.connect(log_stdout=False)

# let's learn a whole model instead
bgp = uut.learn('bgp')

# now let's look at what we learnt
#pprint.pprint(bgp.info)

# what if we could... track the number of neighbors we have?
num_nbr = 0

for bgp_instance in bgp.routes_per_peer['instance'].values():
    for vrf in bgp_instance['vrf'].values():
        for nbr in vrf['neighbor'].values():
            num_nbr += 1

print("Number of BGP neighbors is " + str(num_nbr))
