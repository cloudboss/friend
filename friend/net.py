# Copyright 2017 Joseph Wright <joseph@cloudboss.co>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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
