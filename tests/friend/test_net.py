from itertools import repeat
import unittest

import ipaddress

from friend import net


class NetTests(unittest.TestCase):
    def test_random_ipv4(self):
        rfc_1918 = (u'10.0.0.0/8', u'192.168.0.0/16', u'172.16.0.0/12')
        for cidr in rfc_1918:
            network = ipaddress.ip_network(cidr)
            for random_ip in repeat(lambda: net.random_ipv4(cidr), 100):
                rip = random_ip()
                self.assertTrue(rip > network.network_address)
                self.assertTrue(rip < network.broadcast_address)
