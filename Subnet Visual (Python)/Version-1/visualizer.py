from enum import IntEnum
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

import customtk
from ipv4info import *

class NetworkVisualizer(tk.Tk):
    SMALL_FONT = ('Helvetica', 10)
    EMPTY_BIN_FILL = [''] * 32
    EMPTY_OCTET_FILL = [''] * 4

    class InputToggle(IntEnum):
        DROPDOWNS = 1
        SINGLE_FIELD = 2

        @classmethod
        def message(cls, member):
            return {
                NetworkVisualizer.InputToggle.DROPDOWNS: "Input the IPv4 address in the entry field and use the dropdown to select the mask or prefix.",
                NetworkVisualizer.InputToggle.SINGLE_FIELD: "Input the IPv4 address followed by a '/' and mask or CIDR prefix in the entry field."
            }.get(member, "Unknown toggle type.")


    def create_input_frame(self, container):
        frame = ttk.Frame(container)

        self.ip_err = tk.StringVar()
        self.ip_err.set(ErrorMsg.message(ErrorMsg.SUCCESS))
        self.mask_err = tk.StringVar()
        self.mask_err.set(ErrorMsg.message(ErrorMsg.SUCCESS))

        input_toggle_frame = ttk.Frame(frame)

        self.input_frame_dropdowns = ttk.Frame(frame)
        self.input_frame_entry = ttk.Frame(frame)

        self.style.configure("Small.TRadiobutton", font=('Helvetica', 10))

        self.ip_input = tk.StringVar()

        self.prior_input_toggle = NetworkVisualizer.InputToggle.DROPDOWNS
        self.input_toggle_var = tk.IntVar()
        self.input_toggle_dropdown = ttk.Radiobutton(input_toggle_frame, text = "Mask Dropdown Entry", variable = self.input_toggle_var, value = self.InputToggle.DROPDOWNS, command = self.toggle_input_frame, style="Small.TRadiobutton")
        self.input_toggle_entry = ttk.Radiobutton(input_toggle_frame, text = "Combined Entry Field", variable = self.input_toggle_var, value = self.InputToggle.SINGLE_FIELD, command = self.toggle_input_frame, style="Small.TRadiobutton")
        self.input_toggle_dropdown.grid(column = 0, row = 0, sticky = tk.W)
        self.input_toggle_entry.grid(column = 1, row = 0, sticky = tk.W)

        input_label_frame = ttk.Frame(frame)

        self.input_label = ttk.Label(input_label_frame, 
                                     text = NetworkVisualizer.InputToggle.message(NetworkVisualizer.InputToggle.DROPDOWNS),
                                     font=('Helvetica', 10))
        self.input_label.grid(column = 0, row = 1, sticky = tk.W)
        
        # Input Field - Toggle Option 1 (Dropdowns)
        ttk.Label(self.input_frame_dropdowns, text="IP Address:").grid(column = 0, row = 0, sticky = tk.W)
        ip_input_dd = ttk.Entry(self.input_frame_dropdowns, textvariable = self.ip_input, width = 20)
        ip_input_dd.focus()
        ip_input_dd.grid(column = 1, row = 0, sticky = tk.W)
        
        ttk.Label(self.input_frame_dropdowns, text="/").grid(column = 2, row = 0, sticky = tk.W)
        self.mask_input = ttk.Combobox(self.input_frame_dropdowns, values = list(range(33)), width = 2, state="readonly")
        self.mask_input.grid(column = 3, row = 0, sticky = tk.W)

        self.prior_mask_toggle = MaskType.CIDR
        self.mask_toggle_var = tk.IntVar()
        self.mask_toggle_cidr = ttk.Radiobutton(self.input_frame_dropdowns, text = "CIDR Prefix", variable = self.mask_toggle_var, value = MaskType.CIDR, command = self.toggle_mask_dropdown, style="Small.TRadiobutton")
        self.mask_toggle_netmask = ttk.Radiobutton(self.input_frame_dropdowns, text = "Netmask", variable = self.mask_toggle_var, value = MaskType.NETMASK, command = self.toggle_mask_dropdown, style="Small.TRadiobutton")
        self.mask_toggle_wildcard = ttk.Radiobutton(self.input_frame_dropdowns, text = "Wildcard Mask", variable = self.mask_toggle_var, value = MaskType.WILDCARD, command = self.toggle_mask_dropdown, style="Small.TRadiobutton")
        self.mask_toggle_cidr.grid(column = 3, row = 1, sticky = tk.W)
        self.mask_toggle_netmask.grid(column = 3, row = 2, sticky = tk.W)
        self.mask_toggle_wildcard.grid(column = 3, row = 3, sticky = tk.W)


        # Input Field - Toggle Option 2 (Entry Field)
        ttk.Label(self.input_frame_entry, text="IP Address/Mask:").grid(column=0, row=0, sticky=tk.W)
        ip_input_single = ttk.Entry(self.input_frame_entry, textvariable = self.ip_input, width = 35)
        ip_input_single.focus()
        ip_input_single.grid(column = 1, row = 0, sticky = tk.W)

        error_frame = ttk.Frame(frame)
        ip_err_label = ttk.Label(error_frame, textvariable = self.ip_err, foreground = 'red', font=('Helvetica', 10))
        ip_err_label.grid(column = 0, row = 0, sticky = tk.W)
        mask_err_label = ttk.Label(error_frame, textvariable = self.mask_err, foreground = 'red', font=('Helvetica', 10))
        mask_err_label.grid(column = 0, row = 1, sticky = tk.W)


        button_frame = ttk.Frame(frame)
        submit_button = ttk.Button(button_frame, text = "Submit", command = self.get_input)
        clear_button = ttk.Button(button_frame, text = "Clear", command = self.clear)
        submit_button.grid(column = 0, row = 0, sticky = tk.W)
        clear_button.grid(column = 1, row = 0, sticky = tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx = 5, pady = 0)

        self.input_toggle_var.set(NetworkVisualizer.InputToggle.DROPDOWNS)
        self.mask_toggle_var.set(MaskType.CIDR)
        
        input_toggle_frame.grid(column = 0, row = 0)
        input_label_frame.grid(column = 0, row = 1)
        self.input_frame_dropdowns.grid(column = 0, row = 2)
        error_frame.grid(column = 0, row = 3)
        button_frame.grid(column = 0, row = 4)

        self.input_frame_entry.grid_remove() # Hide input frame to default dropdown

        return frame
    

    def create_footer_frame(self, container):
        frame = ttk.Frame(container)

        ttk.Label(frame, text='Power of 2:').grid(column=0, row=0)
        ttk.Label(frame, text='Exponent:').grid(column=0, row=1)
        for i in range(9):
            ttk.Label(frame, text=2**i).grid(column=i+1, row=0)
            ttk.Label(frame, text=i).grid(column=i+1, row=1)
        for widget in frame.winfo_children():
            widget.grid(padx = 5, pady = 0)
        return frame
    

    def create_summary_frame(self, container):
        frame = ttk.Frame(container, style = "Summary.TFrame")
        f1 = self._binary_comb_and_octets(frame, "ip")

        f1.grid(column = 0, row = 0)
        
        return frame
    

    def _binary_comb_frame(self, container, ip_field, style):
        frame = ttk.Frame(container)

        f1 = ttk.Frame(frame, borderwidth = style["border_width_outer"], relief = style["outer_border_relief"])
        f2 = ttk.Frame(frame, borderwidth = style["border_width_outer"], relief = style["outer_border_relief"])
        f3 = ttk.Frame(frame, borderwidth = style["border_width_outer"], relief = style["outer_border_relief"])
        f4 = ttk.Frame(frame, borderwidth = style["border_width_outer"], relief = style["outer_border_relief"])

        for i in range(8):
            tk.Label(f1, textvariable = self.fields[ip_field]["binary_bits"][i], image = self.spacer, borderwidth = style["border_width_inner"], relief = style["inner_border_relief"], height = style["height"], width = style["bit_width"], background = style["bit_bg_color"], foreground = style["bit_text_color"], compound = tk.CENTER, font = style["font"]).grid(column = i, row = 0)
            tk.Label(f2, textvariable = self.fields[ip_field]["binary_bits"][i + 8], image = self.spacer, borderwidth = style["border_width_inner"], relief = style["inner_border_relief"], height = style["height"], width = style["bit_width"], background = style["bit_bg_color"], foreground = style["bit_text_color"], compound = tk.CENTER, font = style["font"]).grid(column = i, row = 0)
            tk.Label(f3, textvariable = self.fields[ip_field]["binary_bits"][i + 16], image = self.spacer, borderwidth = style["border_width_inner"], relief = style["inner_border_relief"], height = style["height"], width = style["bit_width"], background = style["bit_bg_color"], foreground = style["bit_text_color"], compound = tk.CENTER, font = style["font"]).grid(column = i, row = 0)
            tk.Label(f4, textvariable = self.fields[ip_field]["binary_bits"][i + 24], image = self.spacer, borderwidth = style["border_width_inner"], relief = style["inner_border_relief"], height = style["height"], width = style["bit_width"], background = style["bit_bg_color"], foreground = style["bit_text_color"], compound = tk.CENTER, font = style["font"]).grid(column = i, row = 0)
        
        f1.grid(column=0, row=0, sticky='WENS')
        f2.grid(column=1, row=0, sticky='WENS')
        f3.grid(column=2, row=0, sticky='WENS')
        f4.grid(column=3, row=0, sticky='WENS')

        return frame
    

    def _octet_comb_frame(self, container, ip_field, field_name, style):
        frame = ttk.Frame(container)
    
        for i in range(4):
            tk.Label(frame, textvariable = self.fields[ip_field][field_name][i], image = self.spacer, borderwidth = style["octet_border_width_outer"], relief = style["outer_border_relief"], height = style["height"], width = style["octet_width"], background = style["octet_bg_color"], foreground = style["octet_text_color"], compound=tk.CENTER, font = style["font"]).grid(column = i, row = 0, sticky = tk.W+tk.E)

        return frame
    
    

    def _binary_comb_and_octets(self, container, ip_field, is_tiny = True, has_octet_background = True):
        frame = ttk.Frame(container)

        style = {
            "height": 20 if not is_tiny else 15,
            "octet_width": 176 if not is_tiny else 135,
            "bit_width": 20 if not is_tiny else 15,
            "font": self.default_font if not is_tiny else ('Helvetica', 10),
            "octet_bg_color": "white" if has_octet_background else None,
            "bit_bg_color": "white",
            "bit_text_color": "black",
            "octet_text_color": "black" if has_octet_background else "white",
            "space_width": 20 if not is_tiny else 15,
            "border_width_inner": 1,
            "border_width_outer": 1,
            "octet_border_width_outer": 2,
            "inner_border_relief": "solid",
            "outer_border_relief": "solid",
            "row_label_text_color": "white",
            "row_label_background_color": None
        }

        octet_frame = ttk.Frame(frame, borderwidth = 3)
        self._octet_comb_frame(octet_frame, ip_field, "hex_octets", style).grid(column = 0, row = 0, sticky = 'WENS')
        self._octet_comb_frame(octet_frame, ip_field, "decimal_octets", style).grid(column = 0, row = 1, sticky = 'WENS')

        tk.Label(frame, text = "Octet Value:", image = self.spacer, height = style["height"], background = style["row_label_background_color"], foreground = style["row_label_text_color"], compound=tk.CENTER, font = style["font"]).grid(column = 0, row = 0, sticky = tk.E)
        tk.Label(frame, text = "IP Address:", image = self.spacer, height = style["height"], background = style["row_label_background_color"], foreground = style["row_label_text_color"], compound=tk.CENTER, font = style["font"]).grid(column = 0, row = 1, sticky = tk.E)
        tk.Label(frame, text = "Bit Value:", image = self.spacer, height = style["height"], background = style["row_label_background_color"], foreground = style["row_label_text_color"], compound=tk.CENTER, font = style["font"]).grid(column = 0, row = 2, sticky = tk.E)

        octet_frame.grid(column = 1, row = 0, rowspan = 3, sticky = 'WENS')
        self._binary_comb_frame(frame, ip_field, style).grid(column = 1, row = 2, sticky = 'WENS')

        return frame
    

    def create_visual_frame(self, container):
        self.style.configure("Visual.TFrame", background="lightgreen")

        frame = ttk.Frame(container, style = "Visual.TFrame")

        ttk.Label(frame, text='Visual').grid(column=0, row=0)
        
        return frame


    def __init__(self):
        #root = tk.Tk()
        super().__init__()

        self.title("Network Visualizer")

        self.style = ttk.Style()
        self.style.theme_use()

        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.ip_dict_keys = set(["ip", "netmask", "wildcard", "network", "broadcast", "start_ip", "end_ip"])

        self.fields = {
            "ip": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "netmask": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "wildcard": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "network": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "broadcast": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "start_ip": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "end_ip": {
                    "dotted_quad": tk.StringVar(),
                    "binary_quad": tk.StringVar(), 
                    "long": tk.IntVar(),
                    "binary_bits": [tk.StringVar() for _ in range(32)],
                    "decimal_octets": [tk.StringVar() for _ in range(4)], 
                    "hex_octets": [tk.StringVar() for _ in range(4)]
            },
            "ip_class": tk.StringVar(),
            "is_private": tk.StringVar(),
            "subnet": tk.StringVar(),
            "bits": tk.IntVar(),
            "total_ips": tk.IntVar(),
            "usable_ips": tk.IntVar()
        }

        # layout the root window
        self.rowconfigure(0, minsize = 200, weight=4)
        self.rowconfigure(1, minsize = 200, weight=1)
        
        self.columnconfigure(0, minsize = 200, weight = 2)
        self.columnconfigure(1, minsize = 200, weight = 1)

        self.ip_info = IPv4Info()
        self.prior_summary = (None, None)
        self.prior_submit = (None, None, None)
        self.is_clear = False

        self.spacer = tk.PhotoImage(width=1, height=1)
        self.ip_summary = None

        input_frame = self.create_input_frame(self)
        summary_frame = self.create_summary_frame(self)
        visual_frame = self.create_visual_frame(self)

        input_frame.grid(column = 0, row = 0)
        summary_frame.grid(column = 0, row = 1)
        visual_frame.grid(column = 1, row = 0, rowspan = 2)
        
        #footer_frame = create_footer_frame(root)
        #footer_frame.grid(column = 0, row = 0)
        
        self.mainloop()


    def get_input(self):
        toggle_val = self.input_toggle_var.get()
        ip = None
        mask = None
        mask_type = None
        if toggle_val == NetworkVisualizer.InputToggle.DROPDOWNS:
            ip = self.ip_input.get().strip()
            mask = self.mask_input.get()
            mask_type = self.mask_toggle_var.get()
        else:
            entry = self.ip_input.get().strip().split('/')
            ip = entry[0].strip()
            mask = "" if len(entry) < 2 else entry[1].strip()

        if self.prior_submit == (ip, mask, mask_type):
            return
        
        ip_err, mask_err, self.ip_summary = self.ip_info.validate_input(ip, mask, mask_type)
        self.ip_err.set(ErrorMsg.message(ip_err))
        self.mask_err.set(ErrorMsg.message(mask_err))
        self.prior_submit = (ip, mask, mask_type)

        # populate the fields if everything is fine!
        if self.ip_summary and self.prior_summary != (self.ip_summary.ip.dotted_quad, self.ip_summary.bits):
            self.prior_summary = (self.ip_summary.ip.dotted_quad, self.ip_summary.bits)
            self.set_output_fields()
    

    def _set_ip_fields(self, ip: IPv4SummaryAddress, ip_field):
        if not ip:
            self._clear_ip_fields(ip_field)
            return
        
        self.fields[ip_field]["dotted_quad"].set(ip.dotted_quad)
        self.fields[ip_field]["binary_quad"].set(ip.binary_quad)
        self.fields[ip_field]["long"].set(ip.long)
        for i in range(32):
            self.fields[ip_field]["binary_bits"][i].set(ip.binary_bits[i])
        for i in range(4):
            self.fields[ip_field]["decimal_octets"][i].set(ip.decimal_octets[i])
            self.fields[ip_field]["hex_octets"][i].set(ip.hex_octets[i])
    

    def _clear_ip_fields(self, ip_field):
        self.fields[ip_field]["dotted_quad"].set("")
        self.fields[ip_field]["binary_quad"].set("")
        self.fields[ip_field]["long"].set(None)
        for i in range(32):
            self.fields[ip_field]["binary_bits"][i].set("")
        for i in range(4):
            self.fields[ip_field]["decimal_octets"][i].set("")
            self.fields[ip_field]["hex_octets"][i].set("")

        
    def set_output_fields(self):
        if not self.ip_summary and not self.is_clear:
            self.fields["ip_class"].set("")
            self.fields["is_private"].set("")
            self.fields["subnet"].set("")
            self.fields["bits"].set(None)
            self.fields["total_ips"].set(None)
            self.fields["usable_ips"].set(None)
            
            for ip in self.ip_dict_keys:
                self._clear_ip_fields(ip)
            
            self.is_clear = True
            return
        
        self.fields["ip_class"].set(self.ip_summary.ip_class)
        self.fields["is_private"].set("Private" if self.ip_summary.is_private else "Public")
        self.fields["subnet"].set(self.ip_summary.subnet)
        self.fields["bits"].set(self.ip_summary.bits)
        self.fields["total_ips"].set(self.ip_summary.total_ips)
        self.fields["usable_ips"].set(self.ip_summary.usable_ips)

        for ip in self.ip_dict_keys:
            self._set_ip_fields(getattr(self.ip_summary, ip), ip)   

        self.is_clear = False 
 


    def toggle_mask_dropdown(self):
        toggle_val = self.mask_toggle_var.get()
        idx = self.mask_input.current()

        if toggle_val == self.prior_mask_toggle:
            return
        
        if toggle_val == MaskType.CIDR:
            self.mask_input.config(values = list(range(33)), width = 2)
        elif toggle_val == MaskType.NETMASK:
            self.mask_input.config(values = Masks.NETMASKS, width = 15)
        else:
            self.mask_input.config(values = Masks.WILDCARDS, width = 15)

        if idx >= 0:
            self.mask_input.current(idx)
        
        self.prior_mask_toggle = toggle_val


    def toggle_input_frame(self):
        toggle_val = self.input_toggle_var.get()
        input_val = self.ip_input.get().strip()
        self.input_label.config(text = NetworkVisualizer.InputToggle.message(toggle_val))

        if toggle_val == self.prior_input_toggle:
            return

        if toggle_val == NetworkVisualizer.InputToggle.DROPDOWNS:
            if input_val:
                input_val = input_val.split('/')
                mask = None if len(input_val) < 2 else input_val[1].strip()
                if mask:
                    try:
                        idx = Masks.NETMASKS.index(mask)
                        self.mask_toggle_var.set(MaskType.NETMASK)
                        self.mask_input.current(idx)
                        self.toggle_mask_dropdown()
                    except ValueError:
                        try:
                            idx = Masks.WILDCARDS.index(mask)
                            self.mask_toggle_var.set(MaskType.WILDCARD)
                            self.mask_input.current(idx)
                            self.toggle_mask_dropdown()
                        except ValueError:
                            self.mask_toggle_var.set(MaskType.CIDR)
                            try:
                                cidr = int(mask)
                                if 0 < cidr <= 32:
                                    self.mask_input.current(cidr)
                                    self.toggle_mask_dropdown()
                                else:
                                    self.mask_input.set("")
                            except ValueError:
                                self.mask_input.set("")

                self.ip_input.set(input_val[0].strip())
            else:
                self.mask_input.set("")

            self.input_frame_entry.grid_remove()  # Hide the entry frame
            self.input_frame_dropdowns.grid(column = 0, row = 2)
        else:
            ip = self.ip_input.get().strip().split('/')
            mask = self.mask_input.get()
            ip = '' if len(ip) < 1 else ip[0]
            self.mask_input.set("")

            if ip or mask:
                self.ip_input.set(ip + '/' + mask)
            else:
                self.ip_input.set("")
            self.input_frame_dropdowns.grid_remove()  # Hide the dropdown frame
            self.input_frame_entry.grid(column = 0, row = 2)
        
        self.prior_input_toggle = toggle_val


    def clear(self):
        # Reset input fields
        self.ip_input.set("")
        self.mask_input.set("")

        # Reset errors
        self.ip_err.set(ErrorMsg.message(ErrorMsg.SUCCESS))
        self.mask_err.set(ErrorMsg.message(ErrorMsg.SUCCESS))

        # Reset output fields
        self.prior_summary = (None, None)
        self.prior_submit = (None, None, None)
        self.ip_summary = None
        self.set_output_fields()



if __name__ == "__main__":
    NetworkVisualizer()