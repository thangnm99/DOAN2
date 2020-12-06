from tkinter import *
from PIL import Image,ImageTk
from tkinter import font
import cv2
from tkinter  import filedialog
import main

def Open_File():
    global display_area,imgtk,kq,v
    filedir = filedialog.askopenfilename()
    if filedir != '' :
        print(filedir)
        img = cv2.imread(filedir)
        img = cv2.resize(img,(400,200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image = Image.fromarray(img))
        display_area.create_image(0,0,image=imgtk, anchor = NW)
        predict_result = main.recognize.recog(filedir)
        v.set(predict_result)


windows = Tk()
windows.title("Number reader")
windows.geometry('800x300')
windows.resizable(width=False, height= False)
win_font = font.Font(size = 20)
# -----------------------------------------
menubar = Frame(windows)
menubar.pack(fill = X)

filebt = Button(menubar, text='File',relief  = 'flat', command = Open_File)
filebt.pack(side=LEFT)
# toolbt = Button(menubar, text='Tool',relief  = 'flat')
# toolbt.pack(side=LEFT)
separateline = Canvas(windows,width=810, height = 1, bg = 'gray')
separateline.pack(side = TOP)
#------------------------------------------
display_area = Canvas(windows,width =400, height = 200, bg = 'white')
imgtk = None
display_area.pack(side = LEFT)

#------------------------------------------
label = Label(windows, text='GIA TRI: ')
label['font'] =win_font
label.pack(side = LEFT)

#------------------------------------------

v= StringVar()
v.set('')
entry = Entry(windows,textvariable = v)
entry['font'] = win_font
entry.pack(side = LEFT)


windows.mainloop()