from tkinter import *
from PIL import ImageTk, Image  
master = Tk()
canvas = Canvas(master, width=900, height = 500)
canvas.pack()
canvas.create_rectangle(0,0, 900, 500, fill="black")
# img = Image.open('C:/Users/kimbe/Documents/15112/Term Project/images/full/%s.jpg' % 'The+Godfather')
imgTitle= "Piper"
img = Image.open('C:/Users/kimbe/Documents/15112/Term Project/images/full/%s.jpg' % imgTitle)
movieimg = ImageTk.PhotoImage(img)
canvas.create_image(900/5,500/5*2, image= movieimg)

mainloop()
# import MovieScout.MovieScout.run 
# MovieScout.MovieScout.run.runSpider()