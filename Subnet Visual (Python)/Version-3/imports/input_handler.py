import tkinter as tk
from dataclasses import dataclass


from imports.widgets import *
from imports.ip_fields_dataclasses import *
from imports.ip_constants import *

_PINK_ON = '#FF89B2'
_PINK_OFF = '#99556F'

_BLUE_ON = '#00FFE0'
_BLUE_OFF = '#009983'

_YELLOW_ON = '#FFC655'
_YELLOW_OFF = '#997733'

_PURPLE_ON = '#BD86FF'
_PURPLE_OFF = '#6F5299'

_GREEN_ON = '#00FF93'
_GREEN_OFF = '#009953'

_BACKGROUND = '#212121'
_DARKER_ACCENT = '#131313'
_LIGHTER_ACCENT = '#383838'
_LIGHTEST_ACCENT = '#A5A5A5'
_TEXT = '#FFFFFF'

_FONT = ('TkFixedFont', 10)
_LABEL_FONT = ('TkFixedFont', 8)
_HEADING_FONT = ('TkFixedFont', 12, 'bold')
_TINY_FONT = ('TkFixedFont', 8, 'bold')
_LARGE_FONT = ('TkFixedFont', 25)
_VERY_LARGE_FONT = ('TkFixedFont', 35)
_HUGE_FONT = ('TkFixedFont', 60)

_BINARY_BUTTON_WIDTH = 15

_FONT_STYLES = WidgetFonts(heading=_HEADING_FONT, label=_LABEL_FONT, entry=_FONT, tiny=_TINY_FONT)
_BORDER_WIDTHS = BorderWidths(left=1, right=1, top=1, bottom=1)


_PINK_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PINK_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PINK_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PINK_ON),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_BLUE_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_BLUE_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_BLUE_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_BLUE_ON),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_YELLOW_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_YELLOW_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_YELLOW_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_YELLOW_ON),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_PURPLE_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PURPLE_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PURPLE_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PURPLE_ON),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)


_GREEN_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_GREEN_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_GREEN_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_GREEN_ON),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)


_OCTET_COLORS = (('First', _PINK_STYLE), ('Second', _BLUE_STYLE), ('Third', _YELLOW_STYLE), ('Fourth', _PURPLE_STYLE), ('Extra', _GREEN_STYLE))

class _InputMode(IntEnum):
    BLOCK_TO_IP_RANGE = 0
    IP_RANGE_TO_BLOCK = 1
    PRACTICE = 2

class _MaskType(IntEnum):
    PREFIX_LENGTH = 0
    NETMASK = 1
    WILDCARD = 2

class _InputBase(IntEnum):
    DECIMAL = 10
    OCTAL = 8
    HEX = 16

class InputHandler(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.inner = tk.Frame(self, background=_BACKGROUND, width=900, height=350)
        self.inner.grid(row=0, column=0, sticky="NSEW")
        self.inner.columnconfigure(0, weight=1)
        self.inner.rowconfigure(0, weight=1)

        self.input_fields = InputModeFields(input_mode=tk.IntVar(value=_InputMode.BLOCK_TO_IP_RANGE),
                                            mask_mode=tk.IntVar(value=_MaskType.PREFIX_LENGTH),
                                            base_mode=tk.IntVar(value=_InputBase.DECIMAL))
        self.header = tk.Frame(self.inner, height=25, width=900, background=_BACKGROUND)
        self.header.grid(column=0, row=0, pady=(0, 15), sticky="NWE")

        self.content = tk.Frame(self.inner, height=350, width=900, background=_BACKGROUND)
        self.content.grid(column=0, row=2, sticky="NSEW")

        entry = self._init_block_to_ip_frame()
        entry.grid(row=2, column=0, pady=(5, 15), sticky="NSEW")

        self.footer = tk.Frame(self.inner, height=25, width=900, background=_BACKGROUND)
        self.footer.grid(column=0, row=2, sticky="SEW")

        # TODO
        self.footer.columnconfigure(0, weight=1)
        self.footer.rowconfigure(0, weight=1)

        self._init_base_choice_buttons()
        self.base_button_frame.grid(row=1, column=0, pady=10)

        self.header_buttons = {
            _InputMode.BLOCK_TO_IP_RANGE: self._init_header_button(column=0, name="Block to IP Range", value=_InputMode.BLOCK_TO_IP_RANGE, style=_PINK_STYLE, is_on=True),
            _InputMode.IP_RANGE_TO_BLOCK: self._init_header_button(column=1, name="IP Range to Block", value=_InputMode.IP_RANGE_TO_BLOCK, style=_BLUE_STYLE),
            _InputMode.PRACTICE: self._init_header_button(column=2, name="Subnetting Practice", value=_InputMode.PRACTICE, style=_YELLOW_STYLE)
        }

        # self.entry_frames = {
        #     _InputMode.BLOCK_TO_IP_RANGE: self.__init_block_to_ip_entry_frame()
        # }

        # self.entry = tk.Frame(width=900, background="red", height=100)
        # self.entry.grid(row=1, column=0, sticky="NSEW")

    
    def _init_header_button(self, column, name, value, style: WidgetStyle, is_on=False):
        color = style.enabled.accent if is_on else style.disabled.accent
        
        button = BorderedFrame(self.header, interior=tk.Label, text=name, bordercolor=color, borderwidths=BorderWidths(0, 0, 0, 2), background=style.enabled.background, justify=tk.CENTER, font=('TkFixedFont', 10), foreground=color)
        button.grid(column=column, row=0, sticky="NSEW")
        self.header.columnconfigure(column, weight=1)

        button.interior.bind("<Button-1>", lambda event, mode=value: self._set_mode(event, mode))
        self.input_fields.input_mode.trace("w", lambda *args, button_value=value, off_color=style.disabled.accent, on_color=style.enabled.accent: self._color_header_buttons(*args, button_value=button_value, off_color=off_color, on_color=on_color))

        return button
    

    def _init_block_to_ip_frame(self):
        frame = tk.Frame(self.inner, height=250, width=900, background=_BACKGROUND)
        entry = IPv4EntryFrame(frame, input_base_var=self.input_fields.base_mode)
        entry.grid(row=0, column=0, padx=(15, 0), pady=(0, 10), sticky='NSEW')

        mask = IPv4MaskInputFrame(frame, input_base_var=self.input_fields.base_mode)
        mask.grid(row=1, column=0, padx=(15, 10), columnspan=3, sticky='NSEW')

        #prefix_frame = tk.Frame(frame, background=_BACKGROUND)
        FixedSizeFramedLabel(entry, width=60, height=60, background=_BACKGROUND, text="/", font=_HUGE_FONT, foreground=_OCTET_COLORS[4][1].enabled.accent).grid(row=1, column=1, rowspan=2, sticky="NSEW")

        BorderedFrame(entry, width=45, height=45, interior=FixedSizeFramedLabel, borderwidths=_BORDER_WIDTHS, bordercolor=_OCTET_COLORS[4][1].enabled.accent, background=_DARKER_ACCENT, textvariable=mask.fields.prefix_length, anchor=tk.CENTER, font=_VERY_LARGE_FONT, justify=tk.CENTER, foreground=_OCTET_COLORS[4][1].enabled.accent).grid(row=1, column=2, ipadx=5, ipady=5, padx=80, rowspan=2, sticky="SEW")
        #FixedSizeFramedLabel(prefix_frame, width=80, height=80, background=_DARKER_ACCENT, textvariable=mask.fields.prefix_length, font=_HUGE_FONT, foreground=_OCTET_COLORS[4][1].enabled.accent).grid(row=0, column=1)

        #prefix_frame.grid(row=0, column=1, sticky='NSEW')

        return frame
    

    def _set_mode(self, event, mode):
        # Mode did not change
        if mode == self.input_fields.input_mode.get():
            print("do nothing")
            return
        
        if mode == _InputMode.BLOCK_TO_IP_RANGE:
            print("Block to IP Range")
        elif mode == _InputMode.IP_RANGE_TO_BLOCK:
            print("IP Range to Block")
        else:
            print("Practice")
        
        self.input_fields.input_mode.set(mode)

    def _color_header_buttons(self, *args, button_value, off_color, on_color):
        if button_value == self.input_fields.input_mode.get():
            self.header_buttons[button_value].config(background=on_color)
            self.header_buttons[button_value].interior.config(foreground=on_color)
        else:
            self.header_buttons[button_value].config(background=off_color)
            self.header_buttons[button_value].interior.config(foreground=off_color)

    def _init_base_choice_buttons(self):
        self.base_button_style = SegmentedButtonStyle(
            buttons = [
                ButtonStyle("Octal", value=_InputBase.OCTAL, 
                            selected=WidgetStateColors(background=_GREEN_ON, text=_DARKER_ACCENT, accent=_GREEN_OFF),
                            unselected=WidgetStateColors(background=_DARKER_ACCENT, text=_GREEN_OFF, accent=_GREEN_OFF)),
                ButtonStyle("Decimal", value=_InputBase.DECIMAL, 
                            selected=WidgetStateColors(background=_BLUE_ON, text=_DARKER_ACCENT, accent=_BLUE_OFF),
                            unselected=WidgetStateColors(background=_DARKER_ACCENT, text=_BLUE_OFF, accent=_BLUE_OFF)),
                ButtonStyle("Hex", value=_InputBase.HEX, 
                            selected=WidgetStateColors(background=_YELLOW_ON, text=_DARKER_ACCENT, accent=_YELLOW_OFF),
                            unselected=WidgetStateColors(background=_DARKER_ACCENT, text=_YELLOW_OFF, accent=_YELLOW_OFF))
            ],
            fonts=_FONT_STYLES,
            borderwidths=_BORDER_WIDTHS,
            background=_BACKGROUND
        )

        self.base_button_frame = tk.Frame(self.footer, background=_BACKGROUND)

        self.base_button = SegmentedButtonFrame(self.base_button_frame, self.input_fields.base_mode, button_styles=self.base_button_style)
        self.base_button.grid(row=0, column=0, sticky="NSEW")

        self.base_button.selected.set(_InputBase.DECIMAL)

        for b in self.base_button.buttons:
            b.interior.grid(ipadx=15)



class IPv4EntryFrame(tk.Frame):
    def __init__(self, parent, input_base_var: tk.IntVar, **kwargs):
        tk.Frame.__init__(self, parent, background=_BACKGROUND)
        self.fields = IPv4EntryFields(numeric=tk.StringVar(), 
                                      binary_bits=[tk.StringVar(value='0') for _ in range(32)],
                                      octets=[tk.StringVar(value='0') for _ in range(4)],
                                      _input_base = input_base_var)
        
        self.fields._input_base.trace("w", lambda *args: self._update_input_type(*args))

        for i in range(32):
            self.fields.binary_bits[i].trace("w", lambda *args, i=i: self._color_binary_button(*args, bit_index=i))

        for i in range(4):
            self.fields.octets[i].trace("w", lambda *args, i=i: self._update_octet(*args, octet=i))

        self.inner = tk.Frame(self, background=_BACKGROUND)
        self.inner.grid(row=1, column=0)

        self.label_pad_x = (1, 1)
        self.label_pad_y = (2, 2)

        self.widgets = {
            'octet': WidgetData(row=1, column=0, label=tk.Label(self.inner, text="Decimal:", font=_FONT, background=_BACKGROUND, foreground=_TEXT), frames=[]),
            'binary': WidgetData(row=2, column=0, label=tk.Label(self.inner, text="Bit Value:", font=_FONT, background=_BACKGROUND, foreground=_TEXT), frames=[])
        }

        idx = 1
        for i in range(0, 32, 8):
            binary_octet_num = i // 8
            binary_octet = CombFrame(self.inner,
                              widget=FixedSizeFramedLabel,
                              varslist=self.fields.binary_bits[i:i+8], 
                              bordercolor=_OCTET_COLORS[binary_octet_num][1].enabled.accent,
                              width=_BINARY_BUTTON_WIDTH, 
                              height=_BINARY_BUTTON_WIDTH, 
                              font=_FONT,
                              foreground=_OCTET_COLORS[binary_octet_num][1].disabled.accent,
                              background=_DARKER_ACCENT,
                              **kwargs)
            binary_octet.grid(row=self.widgets['binary'].row, column=idx, sticky="NSEW", pady=self.label_pad_y, padx=self.label_pad_x)
            idx += 1
            self.widgets['binary'].frames.append(binary_octet)
                        
            if binary_octet_num < 3:
                tk.Label(self.inner, text=" ", font=_HEADING_FONT, background=_BACKGROUND, foreground=_TEXT).grid(row=self.widgets['binary'].row, column=idx)
                idx += 1
            
        for i in range(8):
            self.widgets['binary'].frames[0].cells[i].interior.label.bind("<Button-1>", lambda event, i=i: self._toggle_bit(event, i, 0, 7-i, 31-i))
            self.widgets['binary'].frames[1].cells[i].interior.label.bind("<Button-1>", lambda event, i=i: self._toggle_bit(event, 8+i,1, 7-i, 31-8-i))
            self.widgets['binary'].frames[2].cells[i].interior.label.bind("<Button-1>", lambda event, i=i: self._toggle_bit(event, 16+i, 2, 7-i, 31-16-i))
            self.widgets['binary'].frames[3].cells[i].interior.label.bind("<Button-1>", lambda event, i=i: self._toggle_bit(event, 24+i, 3, 7-i, 31-24-i))

            Tooltip(self.widgets['binary'].frames[0].cells[i].interior.label, (1 << (7-i)))
            Tooltip(self.widgets['binary'].frames[1].cells[i].interior.label, (1 << (7-i)))
            Tooltip(self.widgets['binary'].frames[2].cells[i].interior.label, (1 << (7-i)))
            Tooltip(self.widgets['binary'].frames[3].cells[i].interior.label, (1 << (7-i)))

        idx = 1
        validate_octet = self.register(self._validate_octet)
        for i in range(4):
            decimal_octet = LabeledEntryFrame(self.inner, label_text=f"{_OCTET_COLORS[i][0]} Octet", textvariable=self.fields.octets[i], width=3, styles=_OCTET_COLORS[i][1], validate="key", validatecommand=(validate_octet, "%P"))
            decimal_octet.grid(row=self.widgets['octet'].row, column=idx, padx=self.label_pad_x, pady=self.label_pad_y, sticky="NSEW")
            self.widgets['octet'].frames.append(decimal_octet)
            
            self.fields.octets[i].trace("w", lambda *args, i=i: self._update_octet(*args, octet=i))
            decimal_octet.bind("<FocusOut>", lambda event, i=i: self._set_default_octet(event, i))
            decimal_octet.bind("<FocusIn>", lambda event, i=i: self._remove_default_octet_focusin(event, i))

            decimal_octet.tooltip = Tooltip(self.widgets['octet'].frames[i], f"{_OCTET_COLORS[i][0]} Octet (Decimal)")

            idx += 1

            if idx < 7:
                tk.Label(self.inner, text=".", font=_HEADING_FONT, background=_BACKGROUND, foreground=_TEXT).grid(row=self.widgets['octet'].row, column=idx, sticky="S")
                idx += 1

        
    def _toggle_bit(self, event, bit_index, octet, bit_position, absolute_bit_position):
        bit = self.fields.binary_bits[bit_index].get()

        octet_value = self._get_octet(octet)
        numeric = self._get_numeric_ip()
        
        if bit == '1':
            self.fields.binary_bits[bit_index].set(0)
            octet_value &= ~(1 << bit_position)
            self.fields.numeric.set((numeric & ~(1 << absolute_bit_position)))
        else:
            self.fields.binary_bits[bit_index].set(1)
            octet_value |= (1 << bit_position)
            self.fields.numeric.set((numeric | (1 << absolute_bit_position)))
        
        base = self.fields._input_base.get()

        if base == _InputBase.HEX:
            self.fields.octets[octet].set(format(octet_value, '02X'))
        elif base == _InputBase.OCTAL:
            self.fields.octets[octet].set(format(octet_value, 'o'))
        else:
            self.fields.octets[octet].set(octet_value)


    def _get_decimal_octet(self, octet):
        try:
            return int(self.fields.octets[octet].get(), 10)
        except ValueError:
            return 0
    

    def _get_hex_octet(self, octet):
        try:
            return int(self.fields.octets[octet].get(), 16)
        except ValueError:
            return 0
        
    def _get_octal_octet(self, octet):
        try:
            return int(self.fields.octets[octet].get(), 8)
        except ValueError:
            return 0
    

    def _get_octet(self, octet):
        base = self.fields._input_base.get()

        if base == _InputBase.HEX:
            return self._get_hex_octet(octet)
        elif base == _InputBase.OCTAL:
            return self._get_octal_octet(octet)
        else:
            return self._get_decimal_octet(octet)
    

    def _get_numeric_ip(self):
        try:
            return int(self.fields.numeric.get(), 10)
        except ValueError:
            return 0

        
    def _validate_decimal_octet(self, P):
        if P.isdigit():
            try:
                return len(P) < 3 or (0 <= int(P, 10) <= 255)
            except ValueError:
                return False
        return not P


    def _validate_hex_octet(self, P):
        try:
            return (0 <= int(P, 16) <= 255)
        except ValueError:
                return not P
        

    def _validate_octal_octet(self, P):
        if P.isdigit():
            try:
                return len(P) < 3 or (0 <= int(P, 8) <= 255)
            except ValueError:
                return False
        return not P
        
    
    def _validate_octet(self, P):
        base = self.fields._input_base.get()

        if base == _InputBase.HEX:
            return self._validate_hex_octet(P)
        elif base == _InputBase.OCTAL:
            return self._validate_octal_octet(P)
        else:
            return self._validate_decimal_octet(P)
        
    
    def _update_octet(self, *args, octet: int):
        value = self._get_octet(octet)

        bits = bin(value)[2:].zfill(8)
        for i in range(8):
            self.fields.binary_bits[(octet * 8) + i].set(bits[i])

        self.fields.numeric.set((self._get_octet(0) << 24) 
                        | (self._get_octet(1)<< 16) 
                        | (self._get_octet(2)<< 8) 
                        | (self._get_octet(3)))        


    def _set_default_octet(self, event, octet):
        if self.fields._input_base.get() == _InputBase.HEX:
            self.fields.octets[octet].set(format(self._get_octet(octet), '02X'))
        else:
            self.fields.octets[octet].set(self._get_octet(octet))


    def _remove_default_octet_focusin(self, event, octet):
        if self._get_octet(octet) == 0:
            self.fields.octets[octet].set("")
        elif self.fields._input_base.get() == _InputBase.HEX:
            self.fields.octets[octet].set(format(self._get_octet(octet), 'X'))


    def _color_binary_button(self, *args, bit_index):
        octet = bit_index // 8
        bit = bit_index % 8
        if self.fields.binary_bits[bit_index].get() == '1':
            self.widgets['binary'].frames[octet].cells[bit].interior.label.config(foreground=_OCTET_COLORS[octet][1].enabled.text)
        else:
            self.widgets['binary'].frames[octet].cells[bit].interior.label.config(foreground=_OCTET_COLORS[octet][1].disabled.accent)


    def _update_input_type(self, *args):
        base = self.fields._input_base.get()
        
        octets = self._get_numeric_ip().to_bytes(4, 'big')

        if base == _InputBase.HEX:
            self.widgets['octet'].label.config(text="Hex:")
            for i in range(4):
                self.fields.octets[i].set(format(octets[i], '02X'))
                self.widgets['octet'].frames[i].tooltip.change_text(text=f"{_OCTET_COLORS[i][0]} Octet (Hex)")
        elif base == _InputBase.OCTAL:
            self.widgets['octet'].label.config(text="Octal:")
            for i in range(4):
                self.fields.octets[i].set(format(octets[i], 'o'))
                self.widgets['octet'].frames[i].tooltip.change_text(text=f"{_OCTET_COLORS[i][0]} Octet (Octal)")
        else:
            self.widgets['octet'].label.config(text="Decimal:")
            for i in range(4):
                self.fields.octets[i].set(octets[i])
                self.widgets['octet'].frames[i].tooltip.change_text(text=f"{_OCTET_COLORS[i][0]} Octet (Decimal)")
        


class IPv4MaskInputFrame(tk.Frame):
    def __init__(self, parent, input_base_var: tk.IntVar, **kwargs):
        tk.Frame.__init__(self, parent, background=_BACKGROUND)

        slider_colors = PrefixLenSliderColors(background=_BACKGROUND,
                                            slider_color=_DARKER_ACCENT,
                                            on_colors=(_OCTET_COLORS[0][1].enabled.accent, _OCTET_COLORS[1][1].enabled.accent, _OCTET_COLORS[2][1].enabled.accent, _OCTET_COLORS[3][1].enabled.accent, _OCTET_COLORS[4][1].enabled.accent),
                                            off_colors=(_OCTET_COLORS[0][1].disabled.accent, _OCTET_COLORS[1][1].disabled.accent, _OCTET_COLORS[2][1].disabled.accent, _OCTET_COLORS[3][1].disabled.accent, _OCTET_COLORS[4][1].disabled.accent))
        
        self.inner = tk.Frame(self, background=_BACKGROUND)
        self.inner.grid(row=0, column=0)

        self.slider = PrefixLengthSlider(self.inner, colors=slider_colors)
        self.slider.grid(row=0, column=2)

        self._input_base = input_base_var

        self.netmask_visual = IPv4EntryFrame(self.inner, input_base_var=self._input_base)
        self.netmask_visual.grid(row=1, column=0, pady=(5, 0))
        self.wildcard_visual = IPv4EntryFrame(self.inner, input_base_var=self._input_base)
        self.wildcard_visual.grid(row=2, column=0)

        self.fields = IPv4MaskEntryFields(prefix_length=self.slider.slider_pos,
                                          netmask=self.netmask_visual.fields,
                                          wildcard=self.wildcard_visual.fields)
        

        # Unbinding what I do not need, but should make another class or add an option that does what I want
        for i in range(4):
            for j in range(8):
                self.netmask_visual.widgets['binary'].frames[i].cells[j].interior.label.unbind("<Button-1>")
                self.wildcard_visual.widgets['binary'].frames[i].cells[j].interior.label.unbind("<Button-1>")

            self.netmask_visual.widgets['octet'].frames[i].unbind("<FocusOut>")
            self.netmask_visual.widgets['octet'].frames[i].unbind("<FocusIn>")
            self.netmask_visual.widgets['octet'].frames[i].readonly_entry()
            

            self.wildcard_visual.widgets['octet'].frames[i].unbind("<FocusOut>")
            self.wildcard_visual.widgets['octet'].frames[i].unbind("<FocusIn>")
            self.wildcard_visual.widgets['octet'].frames[i].readonly_entry()
        
        self.netmask_dropdown = LabeledMaskComboboxFrame(self.inner, label_text="Netmask", styles=_OCTET_COLORS[1][1], value=self.fields.prefix_length, input_base_var=self._input_base, display_field="netmask")
        self.wildcard_dropdown = LabeledMaskComboboxFrame(self.inner, label_text="Wildcard", styles=_OCTET_COLORS[2][1], value=self.fields.prefix_length, input_base_var=self._input_base, display_field="wildcard")

        self.netmask_dropdown.grid(row=1, column=2, sticky="NSEW")
        self.wildcard_dropdown.grid(row=2, column=2, sticky="NSEW")
        
        self.arrow_frames = [
            FixedSizeFramedLabel(self.inner, text="\u21E6", font=_LARGE_FONT, foreground=_OCTET_COLORS[1][1].enabled.accent, background=_BACKGROUND, justify=tk.CENTER),
            FixedSizeFramedLabel(self.inner, text="\u21E6", font=_LARGE_FONT, foreground=_OCTET_COLORS[2][1].enabled.accent, background=_BACKGROUND)
        ]

        self.arrow_frames[0].grid(row=1, column=1, padx=10, sticky="NSEW")
        self.arrow_frames[1].grid(row=2, column=1, padx=10, sticky="NSEW")

        self.fields.prefix_length.trace("w", lambda *args: self._update_masks(*args))

        self.fields.prefix_length.set(0)


    def _update_masks(self, *args):
        prefix_len = self.fields.prefix_length.get()
        mask_info = IPv4Utility._CIDR_INFO[prefix_len]

        if self.fields.netmask.numeric.get() == mask_info.netmask.numeric:
            return
        
        self.fields.netmask.numeric.set(mask_info.netmask.numeric)
        self.fields.wildcard.numeric.set(mask_info.wildcard.numeric)

        # Trigger the update method for the IPv4EntryFrames by updating the base with the same value
        self._input_base.set(self._input_base.get())
        


class LabeledMaskComboboxFrame(tk.Frame):
    def __init__(self, 
                 parent=None, 
                 label_text="Label", 
                 styles: WidgetStyle = None, 
                 value: tk.Variable = None,
                 input_base_var: tk.IntVar = None,
                 display_field: str = None,
                 **kwargs):
        super().__init__(parent, background=styles.background)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.style = styles
        self.value = value
        self.choice = tk.StringVar()
        self.label_text = tk.StringVar(value=label_text)
        self._input_base = input_base_var

        self.inner = BorderedFrame(self, bordercolor=self.style.enabled.accent, borderwidths=self.style.borderwidths)
        self.inner.grid(row=1, column=0, sticky="EW", padx=0, pady=0, columnspan=2)

        self.inner.interior.config(background=self.style.enabled.background)
        self.inner.rowconfigure(0, weight=1)
        self.inner.columnconfigure(0, weight=1)
        
        self.entry = tk.Entry(self.inner.interior, 
                              background=self.style.enabled.background, 
                              foreground=self.style.enabled.text,
                              disabledbackground=self.style.disabled.background,
                              disabledforeground=self.style.disabled.text,
                              readonlybackground=self.style.readonly.background,
                              highlightbackground=self.style.enabled.background,
                              textvariable=self.choice,
                              state="readonly",
                              highlightthickness=0, bd=0, **kwargs)
        self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5, columnspan=2)
        self.inner.interior.rowconfigure(0, weight=1)
        self.inner.interior.columnconfigure(0, weight=1)

        self.label = tk.Label(self, textvariable=self.label_text, font=self.style.fonts.label, foreground=self.style.enabled.accent, background=self.style.background)
        self.label.grid(row=0, column=0, columnspan=2, padx=0, sticky="SW")

        self.base_label = tk.Label(self, text="(Decimal)", font=self.style.fonts.tiny, foreground=self.style.enabled.accent, background=self.style.background)
        self.base_label.grid(row=2, column=0, columnspan=2, padx=0, sticky="NE")


        self.dropdown_button = tk.Label(self.inner.interior, background=self.style.enabled.background, text="▼", font=self.style.fonts.tiny, foreground=self.style.enabled.accent)
        self.dropdown_button.grid(row=0, column=3, padx=2, pady=2)

        self.dropdown_button.bind("<Button-1>", self._toggle_dropdown)

        self.options = IPv4Utility._CIDR_INFO
        self.dropdown_visible = False
        self.display_field = display_field
        self.display_format_field = "dotted_decimal" # dotted_decimal, decimal_list, dotted_hex, hex_list, dotted_binary, binary_list, dotted_octal, octal_list

        self._input_base.trace("w", lambda *args: self._update_input_type(*args))
        self.value.trace("w", lambda *args: self._update_choice(*args))


    def _get_display_text(self, option):
        display_text = getattr(option, self.display_field, str(option))
        if isinstance(display_text, IPv4MaskFormat):
            display_text = getattr(display_text, self.display_format_field, str(display_text))
        
        return display_text


    def _toggle_dropdown(self, event):
        if self.dropdown_visible:
            self._hide_dropdown()
        else:
            self._show_dropdown()


    def _show_dropdown(self):
        if not self.dropdown_visible:
            self.dropdown_visible = True
            self.dropdown_menu = tk.Menu(self.entry)
            for option in self.options:
                display_text = self._get_display_text(option)
                self.dropdown_menu.add_command(label=display_text, command=lambda option=option: self._select_option(option))
            self.dropdown_menu.post(self.winfo_x(), self.winfo_y() + self.winfo_height())


    def _hide_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_visible = False
            self.dropdown_menu.unpost()


    def _select_option(self, option):
        display_text = self._get_display_text(option)
        self.choice.set(display_text)
        self.value.set(getattr(option, "network_bits", str(option)))
        self._hide_dropdown()


    def disable_combobox(self):
        '''
        Sets the state of the combobox widget to "disabled" and sets appropriate colors
        '''
        self.entry.config(state="disabled")
        self.label.config(foreground=self.style.disabled.accent)
        self.base_label.config(foreground=self.style.disabled.accent)
        self.inner.config(background=self.style.disabled.accent)
        self.dropdown_button.config(foreground=self.style.disabled.accent, background=self.style.disabled.background)
        self.dropdown_button.unbind("<Button-1>")


    def readonly_combobox(self):
        '''
        Sets the state of the combobox widget to "readonly" and sets appropriate colors
        '''
        self.entry.config(state="readonly", foreground=self.style.readonly.text)
        self.label.config(foreground=self.style.readonly.accent)
        self.base_label.config(foreground=self.style.readonly.accent)
        self.inner.config(background=self.style.readonly.accent)
        self.dropdown_button.config(foreground=self.style.readonly.accent, background=self.style.readonly.background)
        self.dropdown_button.unbind("<Button-1>")


    def enable_combobox(self):
        '''
        Sets the state of the combobox widget to "normal" and sets appropriate colors
        '''
        self.entry.config(state="normal", foreground=self.style.enabled.text)
        self.label.config(foreground=self.style.enabled.accent)
        self.base_label.config(foreground=self.style.enabled.accent)
        self.inner.config(background=self.style.enabled.accent)
        self.dropdown_button.config(foreground=self.style.enabled.accent, background=self.style.enabled.background)
        self.dropdown_button.bind("<Button-1>", self.toggle_dropdown)


    def set_label_text(self, label_text):
        '''
        Sets the label text of the widget
        '''
        self.label_text.set(label_text)
    
    
    def _update_input_type(self, *args):
        base = self._input_base.get()

        if base == _InputBase.HEX:
            self.display_format_field = "dotted_hex"
            self.base_label.config(text="(Hex)")
        elif base == _InputBase.OCTAL:
            self.display_format_field = "dotted_octal"
            self.base_label.config(text="(Octal)")
        else:
            self.display_format_field = "dotted_decimal"
            self.base_label.config(text="(Decimal)")
        
        display_text = self._get_display_text(self.options[self.value.get()])
        self.choice.set(display_text)

    
    def _update_choice(self, *args):
        display_text = self._get_display_text(self.options[self.value.get()])
        if display_text != self.choice.get():
            self.choice.set(display_text)