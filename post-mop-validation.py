#!/usr/bin/env python3

# To get a logger for the script
import logging

# Import of PyATS library
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handle errors with connections to devices
from unicon.core import errors

import argparse
from pyats.topology import loader

from genie.testbed import load
from tabulate import tabulate



# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################


class common_setup(aetest.CommonSetup):
    """
    Connect to the devices listed in the testbed.
    """
    @aetest.subsection
    def establish_connections(self, testbed):
        # Load testbed file which is passed as command-line argument
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        # Load all devices from testbed file and try to connect to them
        for device in genie_testbed.devices.values():
            log.info(banner(f"Connect to device '{device.name}'"))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish "
                            f"connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################


class Verify_Interface(aetest.Testcase):

    @aetest.test
    def interface_operational_status(self):
        """
        Validate that interface is 'up'.
        """

        for dev in self.parent.parameters['dev']:
            intfs = dev.parse('show interfaces GigabitEthernet0/0/0/0')
            int_stat=intfs['GigabitEthernet0/0/0/0']['oper_status']

            if int_stat != 'up':
                self.failed("Interface GigabitEthernet0/0/0/0 is down")
            else:
                pass

    
    @aetest.test
    def interface_CRC_errors(self):
        """
        Report on the number of CRS errors on interface
        """

        for dev in self.parent.parameters['dev']:
            intfs = dev.parse('show interfaces GigabitEthernet0/0/0/0')
            in_crc=intfs['GigabitEthernet0/0/0/0']['counters']['in_crc_errors']

            if in_crc > 0:
                self.failed("CRC Errors found")
            else:
                pass
    
    @aetest.test
    def interface_drop_errors(self):
        """
        Report on the number of interface drops
        """

        for dev in self.parent.parameters['dev']:
            intfs = dev.parse('show interfaces GigabitEthernet0/0/0/0')
            in_drops=intfs['GigabitEthernet0/0/0/0']['counters']['in_total_drops']
            out_drops=intfs['GigabitEthernet0/0/0/0']['counters']['out_total_drops']

            if in_drops > 0 or out_drops > 0:
                self.failed("Interface Drops")
            else:
                self.passed("No Interface Errors")
                pass
            
class Verify_IGP(aetest.Testcase):
    
   
    @aetest.test
    def OSPF_Status(self):
        """
        Validate OSPF neighbor is up and correct configuration
        """

        for dev in self.parent.parameters['dev']:
            ospf_nbr = dev.parse('show ospf vrf all-inclusive neighbor detail')
            nbr_state = ospf_nbr['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']['GigabitEthernet0/0/0/0']['neighbors']['10.0.0.6']['state']
            ospf_int = dev.parse('show ospf vrf all-inclusive interface GigabitEthernet0/0/0/0')
            ospf_int_cost=ospf_int['vrf']['']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']['GigabitEthernet0/0/0/0']['cost']
            ospf_line_proto=ospf_int['vrf']['']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']['GigabitEthernet0/0/0/0']['line_protocol']
            if nbr_state == 'full' and ospf_int_cost == 1 and ospf_line_proto == True: 
                self.passed("OSPF Neigbor Up")
                pass
            else:
                self.failed("OSPF Neighbor Down")



class Verify_BGP_Neighbor_Status(aetest.Testcase):
    """ This is validaate that BGP are established """

    @ aetest.test
    def BGP_All_Established(self):

        
        for dev in self.parent.parameters['dev']:
            nbr_cnt=0
            tr=[]
            bgp_nbr=dev.parse('show bgp neighbors')
            nbr_ip=bgp_nbr['instance']['all']['vrf']['default']['neighbor']
            for nbr,vals in nbr_ip.items():
                state=vals['session_state']
                as_nbr=vals['remote_as']
                if state.lower() != 'established':
                    nbr_cnt += 1
                tr.append((nbr,as_nbr,state))
        

        if nbr_cnt > 0:
            print('\n')
            print(tabulate(tr, headers=['BGP Neibhbor', 'BGP AS', 'BGP State']))
            print('\n')
            self.failed("BGP Neighbors Down")
        else:
            self.passed("All BGP Neighbors Established")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
