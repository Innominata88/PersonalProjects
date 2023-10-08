import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

from imports.widgets import *
from imports.ip_fields_dataclasses import *
from imports.input_handler import *
from imports.ip_constants import *

_BACKGROUND = "#212121"
_TEXT = "#FFFFFF"
_ROOT_GEOMETRY = "900x750"

class CIDRVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CIDR Visualizer")
        self.geometry(_ROOT_GEOMETRY)

        self.fields = IPv4SummaryFields(
            ip=self._init_ip_fields(),
            netmask=self._init_ip_fields(),
            wildcard=self._init_ip_fields(),
            network=self._init_ip_fields(),
            broadcast=self._init_ip_fields(),
            start_ip=self._init_ip_fields(),
            end_ip=self._init_ip_fields(),
            next_subnet=self._init_ip_fields(),

            ip_notes=IPv4SummaryNotesFields(ip_class=tk.StringVar(), 
                                            ip_class_range=tk.StringVar(), 
                                            special_notes=[]
                                            ),

            block=IPv4SummaryBlockFields(cidr_notation=tk.StringVar(),
                                         network_bits=tk.IntVar(),
                                         host_bits=tk.IntVar(value=32),
                                         total_addresses=tk.IntVar(),
                                         usable_hosts=tk.IntVar(),
                                         mask_map=[tk.StringVar(value='H') for _ in range(32)]
                                         ),

            subnet=IPv4SubnetFields(prefix_length=tk.StringVar(),
                                    addresses_per_subnet=tk.IntVar(),
                                    subnet_bits=tk.StringVar(),
                                    remaining_host_bits=tk.IntVar(),
                                    number_of_subnets=tk.IntVar(),
                                    subnet_map=[tk.StringVar(value='H') for _ in range(32)]
                                    )
        )
        self.input_frame = InputHandler(self)
        self.input_frame.grid(row=0, column=0, sticky="NSEW")
        
        # self.update()
        # print(self.winfo_width())
        # print(self.input_frame.winfo_width())


        self.mainloop()
        

    def _init_ip_fields(self):
        return IPv4SummaryAddressFields(
            dotted_decimal=tk.StringVar(value='0.0.0.0'),
            dotted_binary=tk.StringVar(value='00000000.00000000.00000000.00000000'),
            dotted_hex=tk.StringVar(value='00.00.00.00'),
            numeric=tk.StringVar(value=0),
            binary_bits=[tk.StringVar(value=0) for _ in range(32)],
            decimal_octets=[tk.StringVar(value=0) for _ in range(4)],
            hex_octets=[tk.StringVar(value='00') for _ in range(4)]
        )

if __name__ == "__main__":
    root = CIDRVisualizer()