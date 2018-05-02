from tkinter import *
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
# import MovieScout.MovieScout.run
from PIL import ImageTk, Image  
master = Tk()
canvas = Canvas(master, width=900, height = 500)
canvas.pack()
# process= CrawlerProcess(get_project_settings())
canvas.create_rectangle(0,0, 900, 500, fill="black")
# button= Button(master, text="click me", command=MovieScout.MovieScout.run.runSpider)
imgTitle= 'City+Lights'
img = Image.open('C:/Users/kimbe/Documents/15112/TermProject/images/full/%s.jpg' % imgTitle)
movieimg = ImageTk.PhotoImage(img)
canvas.create_image(900/5,500/5*2, image= movieimg)
# canvas.create_window(450, 250, window= button)

# def runSpider():
#     process.crawl("mimgspider")
#     process.start()

# 
mainloop()
