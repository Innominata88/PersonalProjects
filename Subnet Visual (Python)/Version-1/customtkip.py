import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
from dataclasses import dataclass
from customtk import *

class DottedQuadBinaryComb(tk.Frame):
    def __init__(self, 
                  container = None,
                  varslist: list[tk.Variable] = None,
                  bordercolor: str = "systemTextColor",
                  outerborderwidths: BorderWidths = BorderWidths(2, 2, 2, 2),
                  innerborderwidth: int = 1,
                  width: str | float = 15, 
                  height: str | float = 15,
                  font=('TkFixedFont', 10),
                  dotfont=('TkFixedFont', 14, 'bold'),
                  **kwargs):
        tk.Frame.__init__(self, container)
        self.octet_frames = []

        idx = 0

        for i in range(0, 32, 8):
            octet = CombFrame(self, 
                              varslist=varslist[i:i+8], 
                              bordercolor=bordercolor, 
                              outerborderwidths=outerborderwidths, 
                              innerborderwidth=innerborderwidth, 
                              width=width, 
                              height=height, 
                              font=font, 
                              **kwargs)
            octet.grid(row=0, column=idx, sticky="W")
            idx += 1
            
            if idx < 6:
                tk.Label(self, text=".", font=dotfont).grid(row=0, column=idx)
                idx += 1
            
            self.octet_frames.append(octet)


class WidgetCombFrame(tk.Frame):
     def __init__(self, 
                  container = None,
                  varslist: list[tk.Variable] = None,
                  textlist: list[str] = None,
                  bordercolor: str = None,
                  outerborderwidths: BorderWidths = BorderWidths(0, 0, 0, 0),
                  innerborderwidth: int = 1,
                  width: str | float = 1,
                  widget: tk.Widget = tk.Entry,
                  **kwargs):
        tk.Frame.__init__(self, container)
        self.cells = []
        
        # Outer container frame with the outside borders
        self.outer = BorderedFrame(self, bordercolor=bordercolor, borderwidths=outerborderwidths)
        self.outer.grid(row=0, column=0, sticky="WENS")

        # Inner container frame to hold the comb
        self.interior = tk.Frame(self.outer)
        self.interior.grid(row=0, column=0, 
                           padx=(outerborderwidths.left, outerborderwidths.right), 
                           pady=(outerborderwidths.top, outerborderwidths.bottom),
                           sticky="WENS")
        
        # Generate labels for the comb and place them
        if varslist:
            number_of_vars = len(varslist)
            for i in range(number_of_vars):
                cell = BorderedFrame(self.interior, 
                                    interior=widget,
                                    bordercolor=bordercolor, 
                                    textvariable=varslist[i], 
                                    borderwidths=BorderWidths(innerborderwidth if i != 0 else 0, 0, 0, 0),
                                    width=width,
                                    **kwargs)
                self.cells.append(cell)
                cell.grid(column = i, row = 0, sticky="WENS")
        else:
            number_of_vars = len(textlist)
            for i in range(number_of_vars):
                cell = BorderedFrame(self.interior, 
                                    interior=widget,
                                    bordercolor=bordercolor, 
                                    text=textlist[i], 
                                    borderwidths=BorderWidths(innerborderwidth if i != 0 else 0, 0, 0, 0),
                                    width=width,
                                    **kwargs)
                self.cells.append(cell)
                cell.grid(column = i, row = 0, sticky="WENS")      


class DottedQuadWidgetComb(tk.Frame):
    def __init__(self, 
                  container = None,
                  varslist: list[tk.Variable] = None,
                  bordercolor: str = "systemTextColor",
                  outerborderwidths: BorderWidths = BorderWidths(2, 2, 2, 2),
                  innerborderwidth: int = 1,
                  font=('TkFixedFont', 10),
                  dotfont=('TkFixedFont', 14, 'bold'),
                  width: str | float = 1,
                  justify=tk.CENTER,
                  spacertxt: str = '.',
                  widget: tk.Widget = tk.Entry,
                  **kwargs):
        tk.Frame.__init__(self, container)
        self.octet_frames = []

        idx = 0
        n = len(varslist)
        step = n // 4

        for i in range(0, n, step):
            octet = WidgetCombFrame(self, 
                              varslist=varslist[i:i+step], 
                              bordercolor=bordercolor, 
                              outerborderwidths=outerborderwidths, 
                              innerborderwidth=innerborderwidth, 
                              width=width,
                              font=font,
                              justify=justify,
                              widget=widget,
                              **kwargs)
            octet.grid(row=0, column=idx, sticky="NSEW")
            idx += 1
            
            if idx < 6:
                tk.Label(self, text=spacertxt, font=dotfont).grid(row=0, column=idx)
                idx += 1
            
            self.octet_frames.append(octet)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x400")

    vals = [tk.StringVar() for _ in range(32)]
    vals2 = [tk.StringVar() for _ in range(4)]
    vals3 = [tk.StringVar() for _ in range(4)]

    num = ['1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '0', '1', '0', '1', '1', '0', '0']
    num2 = ['192', '168', '92', '44']
    num3 = 'C0', 'A8', '5C', '2C'
    for i in range(32):
        vals[i].set(num[i])

    for i in range(4):
        vals2[i].set(num2[i])
        vals3[i].set(num3[i])
    
    #default font color is "systemTextColor"

    b = DottedQuadBinaryComb(root, vals)

    b.grid(row=7, column=0, columnspan=2)


    c = DottedQuadWidgetComb(root, vals)
    c.grid(row=8, column=0, columnspan=2)

    d = DottedQuadWidgetComb(root, vals, font=('TkFixedFont'))
    d.grid(row=9, column=0, columnspan=2)

    e = DottedQuadWidgetComb(root, vals, font=('TkFixedFont', 12), spacertxt=" ")
    e.grid(row=10, column=0, columnspan=2)

    f = DottedQuadWidgetComb(root, vals2, width=3, font=('TkFixedFont', 12))
    f.grid(row=11, column=0, columnspan=2)

    root.mainloop()