from tkinter import *
from tkinter import filedialog
import sys
import tkinter.font as tkfont
from custom import *
from highlight import *
from parser_1 import *
from local import *

window = Tk()
currentFilePath = openData()
window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
window.geometry(config['editor.geometry'])
def fileDropDownHandeler(action):
    global currentFilePath
    if action == "Open":
        file = filedialog.askopenfilename()
        window.title(config['editor.name'] + config['editor.states'][0] + file)
        currentFilePath = file
        with open(file, 'r') as f:
            txt.delete(1.0,END)
            txt.insert(INSERT,f.read())
    elif action == "New":
        currentFilePath = config['editor.deafultFileName']
        txt.delete(1.0,END)
        window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
    elif action == "Save" or action == "SaveAs":
        if currentFilePath == config['editor.deafultFileName'] or action=='SaveAs':
            currentFilePath = filedialog.asksaveasfilename()
        with open(currentFilePath, 'w') as f:
            f.write(txt.get('1.0','end'))
        window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
    elif action == "CEditor":
        window.quit()
    elif action == "CFile":
        if currentFilePath == config['editor.deafultFileName'] or action=='SaveAs':
            currentFilePath = filedialog.asksaveasfilename()
        with open(currentFilePath, 'w') as f:
            f.write(txt.get('1.0','end'))
        window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
        currentFilePath = config['editor.deafultFileName']
        txt.delete(1.0,END)
        window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)

def textchange(event):
    window.title(config['editor.name'] + config['editor.states'][1] + currentFilePath)

def autoIndent(event):
    text = event.widget
    line = text.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', line)
    whitespace = match.group(0) if match else ""
    text.insert("insert", f"\n{whitespace}")
    return "break"

def minimap():
    text.delete("1.0","end")
    text.insert(INSERT,txt.get("1.0","end"))
    text.after(theme['editor.render-timeS'], minimap)

font = tkfont.Font(font=theme['editor.font'])
txt = CustomText(window, selectbackground=theme['editor.selectbackground'], foreground=theme['editor.MYGROUP']['foreground'], selectforeground=theme['editor.selectforeground'], padx=10, pady=10, spacing1=1, highlightthickness=theme['editor.highlightthickness'], spacing2=1, spacing3=1, font=font, background=theme['editor.background'])
txt.place(x=30, rely=0, relheight=1, relwidth=1)
txt.bind('<KeyPress>', textchange)
txt.bind("<Return>", autoIndent)
linenumbers = TextLineNumbers(window, background=theme['editor.background'], highlightthickness=theme['editor.highlightthickness'])
linenumbers.attach(txt)
linenumbers.place(relx=0, rely=0, relheight=1, width=30)
tab_size = font.measure(theme['editor.tabsize'])
txt.config(tabs=tab_size)
linenumbers.redd()

if not config['editor.disable-minimap']:
    text=Text(window, font=theme['editor.minifont'], highlightthickness=theme['editor.highlightthickness'], background=theme['editor.background'])
    text.place(relwidth=0.1, relheight=1, relx=0.9)
    minimap()

try:
    with open(currentFilePath, 'r') as f:
        txt.delete(1.0,END)
        txt.insert(INSERT,f.read())
except: 
    currentFilePath = '/Users/mak/Desktop/CElocked/app/app.py'
    window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
    with open(currentFilePath, 'r') as f:
        txt.delete(1.0,END)
        txt.insert(INSERT,f.read())

if config['editor.highlight']:
    lighting = HighLight(txt)
    lighting._highlight_current_line()
    lighting.highlight()

if config['editor.auto-complete']:
    txt.bind('<">', lambda string: addBind('"'))
    txt.bind("<'>", lambda string: addBind("'"))
    def addBind(what : str):
        txt.insert(INSERT, what)

menu = Menu(window)
fileDropdown = Menu(menu, tearoff=False)

fileDropdown.add_command(label='New File', command=lambda: fileDropDownHandeler("New"), accelerator=keys['editor.k1'][1])
window.bind(keys['editor.k1'][0], lambda string: fileDropDownHandeler("New"))
fileDropdown.add_command(label='Open File', command=lambda: fileDropDownHandeler("Open"), accelerator=keys['editor.k2'][1])
window.bind(keys['editor.k2'][0], lambda string: fileDropDownHandeler("Open"))
fileDropdown.add_command(label='Save File', command=lambda: fileDropDownHandeler("Save"), accelerator=keys['editor.k3'][1])
window.bind(keys['editor.k3'][0], lambda string: fileDropDownHandeler("Save"))
fileDropdown.add_command(label='Save As', command=lambda: fileDropDownHandeler("SaveAs"), accelerator=keys['editor.k4'][1])
window.bind(keys['editor.k4'][0], lambda string: fileDropDownHandeler("SaveAs"))
fileDropdown.add_separator()
fileDropdown.add_command(label='Close File', command=lambda: fileDropDownHandeler("CFile"), accelerator=keys['editor.k5'][1])
window.bind(keys['editor.k5'][0], lambda string: fileDropDownHandeler("CFile"))
menu.add_cascade(label='File', menu=fileDropdown)
window.config(menu=menu)

if len(sys.argv) == 2:
    currentFilePath = sys.argv[1]
    window.title(config['editor.name'] + config['editor.states'][0] + currentFilePath)
    with open(currentFilePath, 'r') as f:
        txt.delete(1.0,END)
        txt.insert(INSERT,f.read())
window.protocol("WM_DELETE_WINDOW", lambda: saveData({'current': currentFilePath}, window))
window.mainloop()

