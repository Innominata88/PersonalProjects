import tkinter as tk
import tkinter.font as tkfont
from dataclasses import dataclass

@dataclass
class BorderWidths:
    left: str | float
    right: str | float
    top: str | float
    bottom: str | float


class FixedSizeFramedLabel(tk.Frame):
    def __init__(self, 
                 container, 
                 width: str | float = 24, 
                 height: str | float = 24, 
                 **kwargs):
        # Create outer frame and prevent resizing
        tk.Frame.__init__(self, container, width=width, height=height)
        self.grid_propagate(0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create the label in the outer frame
        self.label = tk.Label(self, **kwargs)
        self.label.config(anchor="center", justify="center")
        
        # Adjust bottom padding to fix vertical text centering in cell
        self.label.grid(row=0, column=0, sticky="WENS", padx=0, 
                        pady=self._get_vertical_padding(), 
                        ipadx=0, ipady=0)

        # Color the background of the outer frame to account for label padding
        super().configure(bg=self.label.cget("bg"))


    def configure(self, cnf=None, **kwargs):
        if not cnf:
            cnf = {}
        cnf.update(**kwargs)

        bg = None

        if "bg" in cnf:
            bg = cnf.pop("bg")
        if "background" in cnf:
            bg = cnf.pop("background")

        if bg:
            super().configure(bg=bg)
            self.label.configure(bg=bg)

        if "height" in cnf:
            super().configure(height=cnf.pop("height"))
        if "width" in cnf:
            super().configure(width=cnf.pop("width"))
        if "font" in cnf:
            self.label.configure(font=cnf.pop("font"))
            self.label.grid(pady=self._get_vertical_padding())

        self.label.configure(cnf)


    def config(self, cnf=None, **kwargs):
        self.configure(cnf, **kwargs)


    def _get_vertical_padding(self):
        try:
            pady_bottom = (int(self.cget("height")) - int(self.label.cget("font").split()[-1])) / 2
        except ValueError as v:
            pady_bottom = (int(self.cget("height")) - int(tkfont.nametofont("TkDefaultFont").actual("size"))) / 2

        return (0, pady_bottom if pady_bottom > 0 else 0)
            


# Adapted from https://code.activestate.com/recipes/580798-tkinter-frame-with-different-border-sizes/?in=user-4189907
class BorderedFrame(tk.Frame):
    def __init__(self, 
                 container, 
                 bordercolor: str = None, 
                 borderwidths: BorderWidths = BorderWidths(0, 0, 0, 0), 
                 interior: tk.Widget = tk.Frame,
                 **kwargs):
        tk.Frame.__init__(self, container, background=bordercolor)
        self.interior = interior(self, **kwargs)
        self.interior.grid(row=0, column=0, 
                           padx=(borderwidths.left, borderwidths.right), 
                           pady=(borderwidths.top, borderwidths.bottom),
                           sticky="NSEW")
        self.grid_columnconfigure(0, weight=1)


class CombFrame(tk.Frame):
     def __init__(self, 
                  container = None,
                  varslist: list[tk.Variable] = None,
                  textlist: list[str] = None,
                  bordercolor: str = None,
                  outerborderwidths: BorderWidths = BorderWidths(0, 0, 0, 0),
                  innerborderwidth: int = 1,
                  width: str | float = 20, 
                  height: str | float = 20,
                  justify = tk.CENTER,
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
                                    interior=FixedSizeFramedLabel,
                                    bordercolor=bordercolor,
                                    borderwidths=BorderWidths(innerborderwidth if i != 0 else 0, 0, 0, 0),
                                    textvariable=varslist[i],
                                    height=height, 
                                    width=width,
                                    justify=justify,
                                    **kwargs)
                self.cells.append(cell)
                cell.grid(column = i, row = 0, sticky="WENS")
        else:
            number_of_vars = len(textlist)
            for i in range(number_of_vars):
                cell = BorderedFrame(self.interior, 
                                    interior=FixedSizeFramedLabel,
                                    bordercolor=bordercolor,
                                    borderwidths=BorderWidths(innerborderwidth if i != 0 else 0, 0, 0, 0),
                                    text=textlist[i],
                                    height=height, 
                                    width=width,
                                    justify=justify,
                                    **kwargs)
                self.cells.append(cell)
                cell.grid(column = i, row = 0, sticky="WENS")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x400")

    vals = [tk.StringVar() for _ in range(32)]
    vals2 = [tk.StringVar() for _ in range(4)]
    vals3 = [tk.StringVar() for _ in range(4)]
    binary_comb_frame = tk.Frame(root)
    decimal_comb_frame = tk.Frame(root)
    hex_comb_frame = tk.Frame(root)

    binary_comb = CombFrame(root, vals, bordercolor="systemTextColor", 
                  outerborderwidths=BorderWidths(left=2, right=2, top=2, bottom=2), 
                  innerborderwidth=1, 
                  width=15, height=15, font=('TkFixedFont', 10))

    decimal_comb = CombFrame(root, vals2, bordercolor="systemTextColor",
                  outerborderwidths=BorderWidths(left=0, right=0, top=0, bottom=0),
                  innerborderwidth=1, width=127, height=15, font=('Helvetica', 10))
    hex_comb = CombFrame(root, vals3, bordercolor="systemTextColor",
                  outerborderwidths=BorderWidths(left=0, right=0, top=0, bottom=0),
                  innerborderwidth=1, width=127, height=15, font=('Helvetica', 10))
    
    decimal_comb.cells[0].interior.configure(width=130)
    decimal_comb.cells[-1].interior.configure(width=130)

    hex_comb.cells[0].interior.configure(width=130)
    hex_comb.cells[-1].interior.configure(width=130)

    num = ['1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '0', '1', '0', '1', '1', '0', '0']
    num2 = ['192', '168', '92', '44']
    num3 = 'C0', 'A8', '5C', '2C'
    for i in range(32):
        vals[i].set(num[i])

    for i in range(4):
        vals2[i].set(num2[i])
        vals3[i].set(num3[i])
    
    #default font color is "systemTextColor"

    BorderedFrame(root, interior=tk.Label, image=tk.PhotoImage(width=1, height=1), text="Octet Value:", height=10, compound=tk.CENTER, font=('Helvetica', 10)).grid(column=0, row=0, sticky=tk.E)
    BorderedFrame(root, interior=tk.Label, image=tk.PhotoImage(width=1, height=1), text="IP Address:", height=10, compound=tk.CENTER, font=('Helvetica', 10)).grid(column=0, row=1, sticky=tk.E)
    BorderedFrame(root, interior=tk.Label, image=tk.PhotoImage(width=1, height=1), text="Bit Value:", height=10, compound=tk.CENTER, font=('Helvetica', 10)).grid(column=0, row=2, sticky=tk.E)
    
    hex_comb.grid(row = 0, column=1, sticky="WENS", padx=0, pady=0)
    decimal_comb.grid(row = 1, column=1, sticky="WENS", padx=0, pady=0)
    binary_comb.grid(row = 2, column=1, sticky="WENS", padx=0, pady=0)


    root.mainloop()