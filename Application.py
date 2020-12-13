from tkinter import *
from PIL import Image,ImageTk
from tkinter import font
import cv2
from tkinter  import filedialog
import main

def Handle_File():
    global display_area,imgtk,text
    filedir = filedialog.askopenfilename()
    if filedir != '' :
        img = cv2.imread(filedir)
        img = cv2.resize(img,(400,200))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image = Image.fromarray(img))
        display_area.create_image(0,0,image=imgtk, anchor = NW)
        predict_result = main.recognize.recog(filedir)
        text.set(predict_result)


windows = Tk()
windows.title("Number reader")
windows.geometry('800x200')
windows.resizable(width=False, height= False)
win_font = font.Font(size = 20)

#------------------------------------------
filemenu = Menu(windows)
m1 = Menu(filemenu,tearoff=0)
m1.add_command(label = 'Open File',command =Handle_File)
m1.add_command(label = 'Exit', command =quit)
filemenu.add_cascade(label = 'File', menu = m1)
#------------------------------------------
display_area = Canvas(windows,width =400, height = 200, bg = 'white')
display_area.grid(column = 0, row = 0)
imgtk = None
# display_area.pack(side = TOP)

#------------------------------------------
label = Label(windows, text='Predict result: ')
label['font'] =win_font
label.grid(column = 1, row = 0)

#------------------------------------------

text= StringVar()
text.set('')
entry = Entry(windows,textvariable = text)
entry['font'] = win_font
entry.grid(column = 2, row = 0)

windows.config(menu= filemenu)
windows.mainloop()