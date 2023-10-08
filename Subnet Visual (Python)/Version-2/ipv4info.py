from enum import IntEnum, unique
import socket
import struct
from dataclasses import dataclass

@unique
class ErrorMsg(IntEnum):
    SUCCESS = 0
    NO_INPUT = 1
    INVALID_IP = 2
    IS_IPV6 = 3
    INVALID_CIDR = 4
    CIDR_RANGE = 5
    INVALID_MASK = 6
    EMPTY_MASK_OR_PREFIX = 7
    MASK_TYPE_MISMATCH = 8

    @classmethod
    def message(cls, member):
        return {
            ErrorMsg.SUCCESS: "",
            ErrorMsg.NO_INPUT: "No IP address entered.",
            ErrorMsg.INVALID_IP: "Invalid IPv4 address.",
            ErrorMsg.IS_IPV6: "Invalid IPv4 address. This program only accepts IPv4 addresses and not IPv6 addresses.",
            ErrorMsg.INVALID_CIDR: "Invalid CIDR Prefix. A valid CIDR Prefix is between 0 and 32 inclusive.",
            ErrorMsg.CIDR_RANGE: "CIDR Prefix out of range. Enter a value between 0 and 32 inclusive.",
            ErrorMsg.INVALID_MASK: "Invalid Netmask or Wildcard Mask.",
            ErrorMsg.EMPTY_MASK_OR_PREFIX: "Missing Netmask, Wildcard Mask, or CIDR Prefix.",
            ErrorMsg.MASK_TYPE_MISMATCH: "The given mask does not match the selected input type."
        }.get(member, "Unknown error type.")


class MaskType(IntEnum):
    CIDR = 1
    NETMASK = 2
    WILDCARD = 3


class IPv4Address:
    def __init__(self, packed_ip):
        self.packed = packed_ip
        self.ip_address = '.'.join(map(str, self.packed))
        self.long = struct.unpack('!I', self.packed)[0]
        self.binary_quad = '.'.join(bin(byte)[2:].zfill(8) for byte in self.packed)
        self.binary_bits = tuple(b for b in ''.join(bin(byte)[2:].zfill(8) for byte in self.packed))
        self.decimal_octets = tuple(str(int(byte)) for byte in self.packed)
        self.hex_octets = tuple((hex(byte)[2:].zfill(2)).upper() for byte in self.packed)

        # https://en.wikipedia.org/wiki/Classful_network
        self.ip_class = 'A' if self.binary_quad[0] == '0' else \
                        'B' if self.binary_quad[0:2] == '10' else \
                        'C' if self.binary_quad[0:3] == '110' else\
                        'D' if self.binary_quad[0:4] == '1110' else\
                        'E' if self.binary_quad[0:4] == '1111' else \
                        'Unknown'
        
        # 10.0.0.0/8 or 172.16.0.0/12 or 192.168.0.0/16
        # https://www.arin.net/reference/research/statistics/address_filters/
        self.is_private = (self.long & 4278190080) == 167772160 or \
                          (self.long & 4293918720) == 2886729728 or \
                          (self.long & 4294901760) == 3232235520

        self.subnets = None
    
    
class Masks:
    NETMASKS = tuple(socket.inet_ntoa(struct.pack('!I', (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF)) for prefix_length in range(33))
    WILDCARDS = tuple(socket.inet_ntoa(struct.pack('!I', ~(0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF)) for prefix_length in range(33))
    MASK_BITS = tuple(range(33))
    HOST_BITS = tuple(32 - bits for bits in range(33))
    BITMAPS = tuple(['N'] * prefix_length + ['H'] * (32 - prefix_length) for prefix_length in range(33))


class Subnets:
    TOTAL = tuple(1 << (32 - prefix_length) for prefix_length in range(33))
    USABLE_HOSTS = tuple(t - 2 if t > 2 else 0 for t in TOTAL)


@dataclass(frozen=True)
class IPv4Subnet:
    subnet: str
    prefix_length: int
    network_ip: str
    broadcast_ip: str
    start_ip: str
    end_ip: str


@dataclass(frozen=True)
class IPv4SummaryAddress:
    dotted_quad: str
    binary_quad: str
    long: int
    binary_bits: tuple
    decimal_octets: tuple
    hex_octets: tuple


@dataclass(frozen=True)
class IPv4Summary:
    ip: IPv4SummaryAddress
    netmask: IPv4SummaryAddress
    wildcard: IPv4SummaryAddress
    network: IPv4SummaryAddress
    broadcast: IPv4SummaryAddress
    start_ip: IPv4SummaryAddress
    end_ip: IPv4SummaryAddress
    ip_class: str
    is_private: bool
    subnet: str
    bits: int
    total_ips: int
    usable_ips: int


class IPv4Info:
    def __init__(self):
        self.ip_addresses = {}
        self.subnets = {}

        for cidr in range(33):
            n = Masks.NETMASKS[cidr]
            w = Masks.WILDCARDS[cidr]
            self.ip_addresses[n] = IPv4Address(socket.inet_pton(socket.AF_INET, n))

            # Avoid constructing an object for duplicative addresses
            if w not in ['0.0.0.0', '255.255.255.255']:
                self.ip_addresses[w] = IPv4Address(socket.inet_pton(socket.AF_INET, w))

    @classmethod
    def strip_ip_quad_leading_zeros(cls, ip_quad: str):
        return '.'.join([str(int(i)) for i in ip_quad.strip().split('.')])

    def _check_ip(self, ip_address: str):
        ip_address = ip_address.strip()
        if not ip_address:
            return ErrorMsg.NO_INPUT, None
        if ip_address not in self.ip_addresses:
            try:
                ip = IPv4Address(socket.inet_pton(socket.AF_INET, ip_address))
                ip_address = ip.ip_address
                if ip_address not in self.ip_addresses:
                    self.ip_addresses[ip_address] = ip
            except socket.error:
                try:
                    socket.inet_pton(socket.AF_INET6, ip_address)
                    return ErrorMsg.IS_IPV6, None
                except socket.error:
                    return ErrorMsg.INVALID_IP, None
        return ErrorMsg.SUCCESS, ip_address
    

    # TODO: Fix ambguity from determining if /0 and /32 masks are wildcard or netmask
    def _check_mask(self, mask: str, mask_type: MaskType):
        mask = mask.strip()
        if not mask:
            return ErrorMsg.EMPTY_MASK_OR_PREFIX, None
        
        # Very loose here with validation since this is restricted by the dropdown. Needs testing to make sure field input never specifies a mask type
        if mask_type:
            if mask_type == MaskType.CIDR:
                return ErrorMsg.SUCCESS, int(mask)
            elif mask_type == MaskType.NETMASK:
                return ErrorMsg.SUCCESS, Masks.NETMASKS.index(mask)
            else:
                return ErrorMsg.SUCCESS, Masks.WILDCARDS.index(mask)
                    

        # CIDR Prefix
        if len(mask) < 3:
            try:
                mask = int(mask)
                if 0 <= mask <= 32:
                    return ErrorMsg.SUCCESS, mask
                return ErrorMsg.CIDR_RANGE, None
            except ValueError:
                return ErrorMsg.INVALID_CIDR, None
        try:
            mask = IPv4Info.strip_ip_quad_leading_zeros(mask)
            # Check if Netmask
            if mask in Masks.NETMASKS:
                return ErrorMsg.SUCCESS, Masks.NETMASKS.index(mask)
            # Check if Wildcard mask
            return ErrorMsg.SUCCESS, Masks.WILDCARDS.index(mask)
        except ValueError:
            return ErrorMsg.INVALID_MASK, None
    

    def validate_input(self, ip_address: str, mask: str, mask_type: MaskType):
        ip_err, ip_address = self._check_ip(ip_address)
        mask_err, bits = self._check_mask(mask, mask_type)
        info = None

        if ip_err == ErrorMsg.SUCCESS and mask_err == ErrorMsg.SUCCESS:
            self._populate_subnet_info(ip_address)
            # populate dataclass to return
            info = self._generate_ip_info(ip_address, bits)

        return ip_err, mask_err, info
            
    def _populate_subnet_info(self, ip_address: str):
        if not self.ip_addresses[ip_address].subnets:
            long = self.ip_addresses[ip_address].long
            subnets = []
            for bits in range(33):
                network = long & self.ip_addresses[Masks.NETMASKS[bits]].long
                network_quad = socket.inet_ntoa(struct.pack('!I', network))
                s = network_quad + '/' + str(bits)

                if s not in self.subnets:
                    broadcast = long | self.ip_addresses[Masks.WILDCARDS[bits]].long
                    start_ip = None if Subnets.USABLE_HOSTS[bits] == 0 else (network + 1)
                    end_ip = None if Subnets.USABLE_HOSTS[bits] == 0 else (broadcast - 1)

                    broadcast_quad = socket.inet_ntoa(struct.pack('!I', broadcast))
                    start_ip_quad = None if not start_ip else socket.inet_ntoa(struct.pack('!I', start_ip))
                    end_ip_quad = None if not end_ip else socket.inet_ntoa(struct.pack('!I', end_ip))

                    subnet = IPv4Subnet(s, bits, network_quad, broadcast_quad, start_ip_quad, end_ip_quad)

                    self.subnets[s] = subnet

                    if network_quad not in self.ip_addresses:
                        self.ip_addresses[network_quad] = IPv4Address(struct.pack('!I', network))

                    if broadcast_quad not in self.ip_addresses:
                        self.ip_addresses[broadcast_quad] = IPv4Address(struct.pack('!I', broadcast))

                    if start_ip_quad and start_ip_quad not in self.ip_addresses:
                        self.ip_addresses[start_ip_quad] = IPv4Address(struct.pack('!I', start_ip))

                    if end_ip_quad and end_ip_quad not in self.ip_addresses:
                        self.ip_addresses[end_ip_quad] = IPv4Address(struct.pack('!I', end_ip))

                subnets.append(s)

            self.ip_addresses[ip_address].subnets = tuple(subnets)


    def _generate_ip_info(self, ip_address: str, bits: int):
        ip = self.ip_addresses[ip_address]
        netmask = self.ip_addresses[Masks.NETMASKS[bits]]
        wildcard = self.ip_addresses[Masks.WILDCARDS[bits]]
        subnet = self.subnets[ip.subnets[bits]]
        start = None if not subnet.start_ip else self.ip_addresses[subnet.start_ip]
        end = None if not subnet.end_ip else self.ip_addresses[subnet.end_ip]
        network = self.ip_addresses[subnet.network_ip]
        broadcast = self.ip_addresses[subnet.broadcast_ip]

        return IPv4Summary(
            IPv4SummaryAddress(ip.ip_address, ip.binary_quad, ip.long, ip.binary_bits, ip.decimal_octets, ip.hex_octets),
            IPv4SummaryAddress(netmask.ip_address, netmask.binary_quad, netmask.long, netmask.binary_bits, netmask.decimal_octets, netmask.hex_octets),
            IPv4SummaryAddress(wildcard.ip_address, wildcard.binary_quad, wildcard.long, wildcard.binary_bits, wildcard.decimal_octets, wildcard.hex_octets),
            IPv4SummaryAddress(network.ip_address, network.binary_quad, network.long, network.binary_bits, network.decimal_octets, network.hex_octets),
            IPv4SummaryAddress(broadcast.ip_address, broadcast.binary_quad, broadcast.long, broadcast.binary_bits, broadcast.decimal_octets, broadcast.hex_octets),
            None if not start else IPv4SummaryAddress(start.ip_address, start.binary_quad, start.long, start.binary_bits, start.decimal_octets, start.hex_octets),
            None if not end else IPv4SummaryAddress(end.ip_address, end.binary_quad, end.long, end.binary_bits, end.decimal_octets, end.hex_octets),
            ip.ip_class,
            ip.is_private,
            subnet.subnet,
            bits,
            Subnets.TOTAL[bits],
            Subnets.USABLE_HOSTS[bits],
        )