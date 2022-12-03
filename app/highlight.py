import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
from parser_1 import *

class HighLight():
    def __init__(self, textwidget) -> None:
        self.textwidget = textwidget
        self.textwidget.tag_configure("current_line", background=theme['editor.subground'])
    def _highlight_current_line(self, interval=theme['editor.render-time']):
            self.textwidget.tag_remove("current_line", 1.0, "end")
            self.textwidget.tag_add("current_line", "insert linestart", "insert lineend+1c")
            self.textwidget.after(interval, self._highlight_current_line)
    
    def highlight(self):
        cdg = ic.ColorDelegator()
        cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        cdg.tagdefs['MYGROUP'] = theme['editor.MYGROUP']
        cdg.tagdefs['COMMENT'] = theme['editor.COMMENT']
        cdg.tagdefs['KEYWORD'] = theme['editor.KEYWORD']
        cdg.tagdefs['BUILTIN'] = theme['editor.BUILTIN']
        cdg.tagdefs['STRING'] = theme['editor.STRING']
        cdg.tagdefs['DEFINITION'] = theme['editor.DEFINITION']
        ip.Percolator(self.textwidget).insertfilter(cdg)