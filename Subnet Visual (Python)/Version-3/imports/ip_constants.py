from dataclasses import dataclass
from functools import cached_property

@dataclass
class IPv4MaskFormat:
    numeric: int

    @cached_property
    def _be_bytes(self):
        return self.numeric.to_bytes(4, 'big')
    
    @cached_property
    def dotted_decimal(self):
        return '.'.join(map(str, self._be_bytes))
    
    @cached_property
    def decimal_list(self):
        return list(map(int, self.numeric.to_bytes(4, 'big')))
    
    @cached_property
    def dotted_hex(self):
        return '.'.join([hex(value)[2:].zfill(2).upper() for value in self._be_bytes])
    
    @cached_property
    def hex_list(self):
        return [hex(value)[2:].zfill(2).upper() for value in self._be_bytes]
    
    @cached_property
    def dotted_binary(self):
        return '.'.join([bin(value)[2:].zfill(8) for value in self._be_bytes])
    
    @cached_property
    def binary_list(self):
        return [int((self.numeric >> (31 - index)) & 1) for index in range(32)]
    
    @cached_property
    def dotted_octal(self):
        return '.'.join([oct(value)[2:] for value in self._be_bytes])
    
    @cached_property
    def octal_list(self):
        return [oct(value)[2:] for value in self._be_bytes]


@dataclass
class IPv4CIDRInfo:
    network_bits: int

    @cached_property
    def host_bits(self):
        return 32 - self.network_bits
    
    @cached_property
    def network_host_bitmap(self):
        return 'N' * self.network_bits + 'H' * self.host_bits
    
    @cached_property
    def num_addresses(self):
        return 1 << (self.host_bits)
    
    @cached_property
    def num_hosts(self):
        return self.num_addresses - 2 if self.num_addresses > 2 else 0
    
    @cached_property
    def netmask(self):
        return IPv4MaskFormat((0xFFFFFFFF << self.host_bits) & 0xFFFFFFFF)
    
    @cached_property
    def wildcard(self):
        return IPv4MaskFormat(0xFFFFFFFF - self.netmask.numeric)



class IPv4Utility:
    '''
    Construct a constant list to eliminate redundant calculations for finite IPv4 masks
    '''
    _CIDR_INFO = tuple([IPv4CIDRInfo(i) for i in range(33)])

    '''
    Divided by CIDR blocks. Information from:
    https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
    '''
    _SPECIAL_IANA_IPS = {
        32: {
            0: ('0.0.0.0/32', '"This host on this network"', [('[RFC1122], Section 3.2.1.3', 'https://www.rfc-editor.org/rfc/rfc1122.html#page-29')]), # 0.0.0.0/32
            3221225480: ('192.0.0.8/32', 'IPv4 dummy address', [('[RFC7600]', 'https://www.rfc-editor.org/rfc/rfc7600.html')]), # 192.0.0.8/32
            3221225481: ('192.0.0.9/32', 'Port Control Protocol Anycast', [('[RFC7723]', 'https://www.rfc-editor.org/rfc/rfc7723.html')]), # 192.0.0.9/32
            3221225482: ('192.0.0.10/32', 'Traversal Using Relays around NAT Anycast', [('[RFC8155]', 'https://www.rfc-editor.org/rfc/rfc8155.html')]), # 192.0.0.10/32
            3221225642: ('192.0.0.170/32, 192.0.0.171/32', 'NAT64/DNS64 Discovery', [('[RFC8880]', 'https://www.rfc-editor.org/rfc/rfc8880.html'), ('[RFC7050], Section 2.2', 'https://www.rfc-editor.org/rfc/rfc7050.html#section-2.2')]), # 192.0.0.170/32
            3221225643: ('192.0.0.170/32, 192.0.0.171/32', 'NAT64/DNS64 Discovery', [('[RFC8880]', 'https://www.rfc-editor.org/rfc/rfc8880.html'), ('[RFC7050], Section 2.2', 'https://www.rfc-editor.org/rfc/rfc7050.html#section-2.2')]), # 192.0.0.171/32
            4294967295: ('255.255.255.255/32', 'Limited Broadcast', [('[RFC8190]', 'https://www.rfc-editor.org/rfc/rfc8190.html'), ('[RFC919], Section 7', 'https://www.rfc-editor.org/rfc/rfc919.html#section-7')]) # 255.255.255.255/32
        },
        29: { # 4294967288
            3221225472: ('192.0.0.0/29', 'IPv4 Service Continuity Prefix', [('[RFC7335]', 'https://www.rfc-editor.org/rfc/rfc7335.html')]) # 192.0.0.0/29
        },
        24: { # 4294967040
            3221225472: ('192.0.0.0/24', 'IETF Protocol Assignments', [('[RFC6890], Section 2.1', 'https://www.rfc-editor.org/rfc/rfc6890.html#section-2.1')]), # 192.0.0.0/24
            3221225984: ('192.0.2.0/24', 'Documentation (TEST-NET-1)', [('[RFC5737]', 'https://www.rfc-editor.org/rfc/rfc5737.html')]), # 192.0.2.0/24
            3223307264: ('192.31.196.0/24', 'AS112-v4', [('[RFC7535]', 'https://www.rfc-editor.org/rfc/rfc7535.html')]), # 192.31.196.0/24
            3224682752: ('192.52.193.0/24', 'AMT', [('[RFC7450]', 'https://www.rfc-editor.org/rfc/rfc7450.html')]), # 192.52.193.0/24
            3232706560: ('192.175.48.0/24', 'Direct Delegation AS112 Service', [('[RFC7534]', 'https://www.rfc-editor.org/rfc/rfc7534.html')]), # 192.175.48.0/24
            3325256704: ('198.51.100.0/24', 'Documentation (TEST-NET-2)', [('[RFC5737]', 'https://www.rfc-editor.org/rfc/rfc5737.html')]), # 198.51.100.0/24
            3405803776: ('203.0.113.0/24', 'Documentation (TEST-NET-3)', [('[RFC5737]', 'https://www.rfc-editor.org/rfc/rfc5737.html')]), # 203.0.113.0/24
        },
        16: { # 4294901760
            2851995648: ('169.254.0.0/16', 'Link Local', [('[RFC3927]', 'https://www.rfc-editor.org/rfc/rfc3927.html')]), # 169.254.0.0/16
            3232235520: ('192.168.0.0/16', '172.16.0.0/12', 'Private-Use', [('[RFC1918]', 'https://www.rfc-editor.org/rfc/rfc1918.html')]) # 192.168.0.0/16
        },
        15: { # 4294836224
            3323068416: ('198.18.0.0/15', 'Benchmarking', [('[RFC2544]', 'https://www.rfc-editor.org/rfc/rfc2544.html')]) # 198.18.0.0/15
        },
        12: { # 4293918720
            2886729728: ('172.16.0.0/12', 'Private-Use', [('[RFC1918]', 'https://www.rfc-editor.org/rfc/rfc1918.html')]) # 172.16.0.0/12
        },
        10: { # 4290772992
            1681915904: ('100.64.0.0/10', 'Shared Address Space', [('[RFC6598]', 'https://www.rfc-editor.org/rfc/rfc6598.html')]) # 100.64.0.0/10
        },
        8: { # 4278190080
            0: ('0.0.0.0/8', '"This network"', [('[RFC791], Section 3.2', 'https://www.rfc-editor.org/rfc/rfc791.html#section-3.2')]), # 0.0.0.0/8
            167772160: ('10.0.0.0/8', 'Private-Use', [('[RFC1918]', 'https://www.rfc-editor.org/rfc/rfc1918.html')]), # 10.0.0.0/8
            2130706432: ('127.0.0.0/8', 'Loopback', [('[RFC1122], Section 3.2.1.3', 'https://www.rfc-editor.org/rfc/rfc1122.html#page-29')]) # 127.0.0.0/8
        },
        4: { # 4026531840
            4026531840: ('240.0.0.0/4', 'Reserved', [('[RFC1112], Section 4', 'https://www.rfc-editor.org/rfc/rfc1112.html#section-4')]) # 240.0.0.0/4
        }
    }

    @classmethod
    def _get_bit_by_index(cls, ip_addr: int, index: int) -> int:
        '''
        Internal function

        Returns the bit of an IPv4 address at the specified index
        '''
        return int((ip_addr >> (31 - index)) & 1)


    @classmethod
    def _get_octet_by_index(cls, ip_addr: int, index: int) -> int:
        '''
        Internal function

        Returns the octet of an IPv4 address at the specified index (0 indexed)
        '''
        return int((ip_addr >> (24 - (index * 8))) & 0xFF)
    

    @classmethod
    def _get_ip_class(cls, ip_addr: int) -> (str, str, int):
        '''
        Internal function

        Returns the IP Class, the first octet range of the class, 
        and the bit index which distinguishes the class
        '''
        if IPv4Utility._get_bit_by_index(ip_addr, 0) == 0:
            return ('A', '0 - 127', 0)
        elif IPv4Utility._get_bit_by_index(ip_addr, 1) == 0:
            return ('B', '128 - 191', 1)
        elif IPv4Utility._get_bit_by_index(ip_addr, 2) == 0:
            return ('C', '192 - 223', 2)
        elif IPv4Utility._get_bit_by_index(ip_addr, 3) == 0:
            return ('D', '224 - 239', 3)
        else:
            return ('E', '240 - 255', 3)
    

    @classmethod
    def _get_special_iana_ip_notes(cls, ip_addr: int) -> list:
        '''
        Internal function

        Checks to see which special ranges the ip address is a part of and returns a list of the special blocks the ip is a part of
        Ranges and information based on: https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
        '''
        special = []
        for block in IPv4Utility._SPECIAL_IANA_IPS.keys():
            try:
                special.append(IPv4Utility._SPECIAL_IANA_IPS[block][ip_addr & IPv4Utility._CIDR_INFO[block].netmask.numeric])
            except KeyError:
                continue
        
        return special
    

    @classmethod
    def _is_power_of_two(cls, n: int) -> bool:
        '''
        Internal function

        Returns True if n is a power of 2
        '''
        return n > 0 and (n & (n - 1)) == 0
    

    @classmethod
    def _get_closest_power_of_two(cls, n: int) -> int:
        '''
        Internal function

        Returns the closest power 2 of n such that 2^power >= n
        '''
        assert(n > 0)
        power = n.bit_length() - 1

        if IPv4Utility._is_power_of_two(n):
            return power
        else:
            return power if (1 << power) > n else power + 1
        

    @classmethod
    def _get_blocks_from_ip_range(cls, start_ip: int, end_ip: int) -> list:
        '''
        Internal function

        Returns a list of CIDR blocks which covers the range of ips between start_ip and end_ip (inclusive)
        '''
        assert(start_ip <= end_ip)
        blocks = []
        while start_ip <= end_ip:
            if start_ip == end_ip:
                blocks.append(f"{IPv4Utility._numeric_ip_to_dotted_decimal(start_ip)}/32")
                break
            prefix_len = 32 - IPv4Utility._get_closest_power_of_two(end_ip - start_ip + 1)
            for i in range(prefix_len, 33):
                network = IPv4Utility._get_network_ip(start_ip, i)
                broadcast = IPv4Utility._get_broadcast_ip(start_ip, i)
                if network == start_ip and broadcast <= end_ip:
                    blocks.append(f"{IPv4Utility._numeric_ip_to_dotted_decimal(start_ip)}/{i}")
                    start_ip = broadcast + 1
                    break
        return blocks
    

    @classmethod
    def _numeric_ip_to_dotted_decimal(cls, ip: int) -> str:
        '''
        Internal function

        Converts a numeric IPv4 address into dotted decimal notation
        '''
        return '.'.join(map(str, ip.to_bytes(4, 'big')))
    

    @classmethod
    def _get_network_ip(cls, numeric_ip: int, prefix_len: int) -> int:
        '''
        Internal function

        Returns the network address of the <numeric_ip>/<prefix_len> block
        '''
        assert(0 <= prefix_len <= 32)
        return numeric_ip & IPv4Utility._CIDR_INFO[prefix_len].netmask.numeric
    

    @classmethod
    def _get_broadcast_ip(cls, numeric_ip: int, prefix_len: int) -> int:
        '''
        Internal function

        Returns the broadcast address of the <numeric_ip>/<prefix_len> block
        '''
        assert(0 <= prefix_len <= 32)
        return numeric_ip | IPv4Utility._CIDR_INFO[prefix_len].wildcard.numeric




# --------- Testing -----------    

# tests = [
#     "0.0.0.0",
#     "0.0.0.1",
#     "10.0.0.0",
#     "100.64.0.0",
#     "127.0.0.0",
#     "169.254.0.0",
#     "172.16.0.0",
#     "192.0.0.0",
#     "192.0.0.8",
#     "192.0.0.9",
#     "192.0.0.10",
#     "192.0.0.170",
#     "192.0.0.171",
#     "192.0.2.0",
#     "192.31.196.0",
#     "192.52.193.0",
#     "192.88.99.0",
#     "192.168.0.0",
#     "192.175.48.0",
#     "198.18.0.0",
#     "198.51.100.0",
#     "203.0.113.0",
#     "240.0.0.0",
#     "255.255.255.255"
# ]

# import socket
# import struct

# # for t in tests:
# #     print(t)
# #     t = struct.unpack("!I", socket.inet_aton(t))[0]
# #     print(t)
# #     print(IPv4Utility._get_ip_class(t))
# #     print(IPv4Utility._get_special_iana_ip_notes(t))
# #     print()

# # for i in range(33):
# #     print(IPv4Utility._CIDR_INFO[i].network_bits, IPv4Utility._CIDR_INFO[i].host_bits, IPv4Utility._CIDR_INFO[i].num_addresses)

# ip0 = struct.unpack("!I", socket.inet_aton('255.255.255.255'))[0]
# ip1 = struct.unpack("!I", socket.inet_aton('255.255.255.255'))[0]

# x = IPv4Utility._get_blocks_from_ip_range(ip0, ip1)
# print(x)
# print(len(x))
