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

txt = CustomText(window, selectbackground=theme['editor.selectbackground'], foreground=theme['editor.MYGROUP']['foreground'], selectforeground=theme['editor.selectforeground'], padx=10, pady=10, spacing1=1, highlightthickness=theme['editor.highlightthickness'], spacing2=1, spacing3=1, font=theme['editor.font'], background=theme['editor.background'])
txt.place(relx=0.05, rely=0, relheight=1, relwidth=0.95)
txt.bind('<KeyPress>', textchange)
font = tkfont.Font(font=theme['editor.font'])
linenumbers = TextLineNumbers(window, background=theme['editor.background'], highlightthickness=theme['editor.highlightthickness'])
linenumbers.attach(txt)
linenumbers.place(relx=0, rely=0, relheight=1, relwidth=0.05)
tab_size = font.measure(theme['editor.tabsize'])
txt.config(tabs=tab_size)
linenumbers.redd()
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

lighting = HighLight(txt)
lighting._highlight_current_line()
lighting.highlight()

txt.bind('<">', lambda string: addBind('"'))
txt.bind("<'>", lambda string: addBind("'"))
def addBind(what : str):
    txt.insert(INSERT, what)

menu = Menu(window)
fileDropdown = Menu(menu, tearoff=False)

fileDropdown.add_command(label='New File', command=lambda: fileDropDownHandeler("New"), accelerator="Command+N")
window.bind(keys['editor.k1'], lambda string: fileDropDownHandeler("New"))
fileDropdown.add_command(label='Open File', command=lambda: fileDropDownHandeler("Open"), accelerator="Command+O")
window.bind(keys['editor.k2'], lambda string: fileDropDownHandeler("Open"))
fileDropdown.add_command(label='Save File', command=lambda: fileDropDownHandeler("Save"), accelerator="Command+S")
window.bind(keys['editor.k3'], lambda string: fileDropDownHandeler("Save"))
fileDropdown.add_command(label='Save As', command=lambda: fileDropDownHandeler("SaveAs"), accelerator="Command+Shift+S")
window.bind(keys['editor.k4'], lambda string: fileDropDownHandeler("SaveAs"))
fileDropdown.add_separator()
fileDropdown.add_command(label='Close File', command=lambda: fileDropDownHandeler("CFile"), accelerator="Command+Shift+F")
window.bind(keys['editor.k5'], lambda string: fileDropDownHandeler("CFile"))
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




