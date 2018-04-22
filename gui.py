# user interface for recommendation engine
from tkinter import *
from recommend import * 
def showTerminal():
    # clear screen every time has new input
    canvas.delete('msg', 'movie')
    # user input value 
    inputText= str(e1.get())
    # run recommend function
    msg, lst= getTitleRecs(inputText)
    # output results on canvas
    canvas.create_text(450, 185, text=msg, fill= "white", font= "Helvetica 12", tags= 'msg')
    for i in range(len(lst)):
        canvas.create_text(450, 205+i*20, text= lst[i], fill= "white", font= "Helvetica 12", tags= 'movie')

#initalize tk screen
root = Tk()
canvas = Canvas(root, width = 900, height = 500)
canvas.pack()
canvas.create_rectangle(0,0,960, 540, fill= "black")
# initalize 1-line text input box
e1 = Entry(canvas)
canvas.create_text(450, 100, text= "Enter a movie title here", fill= "white", font= "Helvetica 18")
# bind text input box to a window, placing it on canvas
canvas.create_window(400, 150, window=e1)
# create button; bind to function showTerminal
b= Button(root, text= "Get Recs", width= 10, command= showTerminal)
# place button on canvas
canvas.create_window(530, 150, window=b)
root.mainloop()



