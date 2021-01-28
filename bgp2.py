from genie.testbed import load
from tabulate import tabulate
import os
HERE = os.path.dirname(__file__)


if __name__ == '__main__':
    testbed = load(os.path.join(HERE, 'tb.yml'))

    uut = testbed.devices['xr1']
    uut.connect(log_stdout=False)

    uut.connect()
    info = uut.learn('platform')
    bgp = uut.learn('bgp')

    # print useful information
    print('\n' + '-'*80)
    print('Hostname: %s' % uut.name)
    print('Software Version: %s %s\n' % (info.os, info.version))

    nbr_info = []
    for bgp_instance in bgp.routes_per_peer['instance']:
        for vrf in bgp.routes_per_peer['instance'][bgp_instance]['vrf']:
            for nbr in bgp.routes_per_peer['instance'][bgp_instance]['vrf'][vrf]['neighbor']:
                nbr_info.append((bgp_instance, vrf, nbr))

    print(tabulate(nbr_info, headers=['BGP Instance', 'VRF', 'Neighbor']))

    print('\nTotal # of Active Neighbors: %s' % len(nbr_info))
    print('-'*80 + '\n')
