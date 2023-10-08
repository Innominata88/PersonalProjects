import tkinter as tk
from dataclasses import dataclass
from enum import IntEnum

@dataclass
class IPv4SummaryAddressFields:
    dotted_decimal: tk.StringVar
    dotted_binary: tk.StringVar
    dotted_hex: tk.StringVar
    numeric: tk.StringVar
    binary_bits: list
    decimal_octets: list
    hex_octets: list


@dataclass
class IPv4SubnetFields:
    prefix_length: tk.StringVar
    addresses_per_subnet: tk.IntVar
    subnet_bits: tk.StringVar
    remaining_host_bits: tk.IntVar
    number_of_subnets: tk.IntVar
    subnet_map: list


@dataclass
class IPv4SummaryNotesFields:
    ip_class: tk.StringVar
    ip_class_range: tk.StringVar
    special_notes: list


@dataclass
class IPv4SummaryBlockFields:
    cidr_notation: tk.StringVar
    network_bits: tk.IntVar
    host_bits: tk.IntVar
    total_addresses: tk.IntVar
    usable_hosts: tk.IntVar
    mask_map: list


@dataclass
class IPv4SummaryFields:
    ip: IPv4SummaryAddressFields
    netmask: IPv4SummaryAddressFields
    wildcard: IPv4SummaryAddressFields
    network: IPv4SummaryAddressFields
    broadcast: IPv4SummaryAddressFields
    start_ip: IPv4SummaryAddressFields
    end_ip: IPv4SummaryAddressFields
    next_subnet: IPv4SummaryAddressFields

    ip_notes: IPv4SummaryNotesFields
    block: IPv4SummaryBlockFields

    subnet: IPv4SubnetFields


@dataclass
class InputModeFields:
    input_mode: tk.IntVar
    mask_mode: tk.IntVar
    base_mode: tk.IntVar


@dataclass
class IPv4EntryFields:
    numeric: tk.StringVar
    binary_bits: list
    octets: list
    _input_base: tk.IntVar


@dataclass
class IPv4MaskEntryFields:
    prefix_length: tk.IntVar
    netmask: IPv4EntryFields
    wildcard: IPv4EntryFields


@dataclass
class WidgetData:
    row: int
    column: int
    label: tk.Label
    frames: list
