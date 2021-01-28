    #!/usr/bin/env python

# To get a logger for the script
import logging
import json
# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie
from genie.abstract import Lookup
from genie.testbed import load
from genie.utils import Dq


# import the genie libs
from genie.libs import ops # noqa

rr_nbr = ['10.111.111.2']

# Get your logger for your script
log = logging.getLogger(__name__)

testbed = load('./xr-tb-1.yaml')
xr1=testbed.devices['xr1']
xr1.connect(log_stdout=False)

bgp_session=xr1.parse('show bgp neighbors')

nbr_ip=Dq(bgp_session).contains('established').get_values('neighbor')

for nbr in rr_nbr:
    if nbr not in nbr_ip:
        print(f'BGP Session with {rr_nbr} not establised')
    else:
        print(f'BGP Session with {rr_nbr} established')