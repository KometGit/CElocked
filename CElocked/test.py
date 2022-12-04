from tkinter import *

root = Tk()
text = Text(root, width = 12, height = 5, wrap = WORD)
text.insert(END, 'This is an example text.')
text.pack()

root.update()

# Note `text.count("0.0", "end", "displaylines")` returns a tuple like this: `(3, )`
result = text.count("0.0", "end", "displaylines")[0]
print(result)

root.mainloop()