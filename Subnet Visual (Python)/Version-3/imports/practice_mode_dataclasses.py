import tkinter as tk
from dataclasses import dataclass

@dataclass
class IPv4PracticeEntryFields:
    decimal_list: list
    binary_list: list
    hex_list: list
    is_correct: tk.BooleanVar
    is_shown: tk.BooleanVar
    is_checked: tk.BooleanVar


@dataclass
class IPv4PracticeFields:
    target_ip: list
    target_cidr: tk.IntVar
    network_ip: list
    min_host: list
    max_host: list
    next_subnet: list
    is_complete: tk.BooleanVar