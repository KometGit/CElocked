import tkinter as tk
from parser_1 import *

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redd(self):
        self.redraw()
        self.after(theme['editor.render-time'], self.redd)

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = '  ' + str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", fill=theme['editor.linenumbesr-color'], text=linenum, font=theme['editor.font'])
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = 'customtext' + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")):
            self.event_generate("<<Change>>", when="tail")
        return result