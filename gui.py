from tkinter import *
from recommend import * 
def showTerminal():
    canvas.delete('msg', 'movie')
    inputText= str(e1.get())
    msg, lst= getTitleRecs(inputText)
    canvas.create_text(450, 185, text=msg, fill= "white", font= "Helvetica 12", tags= 'msg')
    for i in range(len(lst)):
        canvas.create_text(450, 205+i*20, text= lst[i], fill= "white", font= "Helvetica 12", tags= 'movie')
root = Tk()
canvas = Canvas(root, width = 900, height = 500)
canvas.pack()
canvas.create_rectangle(0,0,960, 540, fill= "black")
e1 = Entry(canvas)
canvas.create_text(450, 100, text= "Enter a movie title here", fill= "white", font= "Helvetica 18")
canvas.create_window(400, 150, window=e1)
b= Button(root, text= "Get Recs", width= 10, command= showTerminal)
canvas.create_window(530, 150, window=b)
root.mainloop()


