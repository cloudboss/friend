import random

import ipaddress


def random_ipv4(cidr='10.0.0.0/8'):
    """
    Return a random IPv4 address from the given CIDR block.

    :key str cidr: CIDR block
    :returns: An IPv4 address from the given CIDR block
    :rtype: ipaddress.IPv4Address
    """
    network = ipaddress.ip_network(unicode(cidr))
    start = int(network.network_address) + 1
    end = int(network.broadcast_address)
    randint = random.randrange(start, end)
    return ipaddress.ip_address(randint)
