# for testing/practicing purposes 
# source: https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# 
# from sklearn.feature_extraction.text import CountVectorizer
# # list of text documents
# text = ["The quick brown fox jumped over the lazy dog."]
# # create the transform
# vectorizer = CountVectorizer()
# # tokenize and build vocab
# vectorizer.fit(text)
# # summarize
# print(vectorizer.vocabulary_)
# # encode document
# vector = vectorizer.transform(text)
# # summarize encoded vector
# print(vector.shape)
# print(type(vector))
# print(vector.toarray())



#image from 
#https://www.listchallenges.com/movies-that-you-cant-live-life-without-seeing
#https://www.pinterest.com/pin/414683078161007928/
#https://www.123rf.com/photo_3985403_tv-channel-movie-guide-on-abstract-background.html

from PIL import ImageTk
from tkinter import *

class UI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.width= 900
        self.height= 500
        self.canvas = Canvas(self, width = self.width, height = \
        self.height)
        self.canvas.pack()
        self.welcomeScreen()
    
    def welcomeScreen(self):
        self.canvas.delete('all')
        self.image= ImageTk.PhotoImage(file= \
         "./images/startImage.png")
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.image)
        self.canvas.create_text(self.width/3, self.height/3, text= "MovieScout", font= "Helvetica 48 bold", fill= "black")
        self.var = StringVar(self)
        self.var.set('Getting Started')
        self.options = OptionMenu(self, self.var, \
        'Title Recommendations', command=self.titleScreen)
        self.options.config(bg= "black", fg= "white",font= "Helvetica 15")
        self.options['menu'].config(bg= "black", fg= "white", font= "Helvetica 12")
        self.options['menu'].add_command(label='Genre Recommendations', command="")
        self.options['menu'].add_command(label='Mood Recommendations', command= "")
        self.canvas.create_window(self.width/3, self.height/4*3, window=self.options)

    def titleScreen(self, val=""):
        self.canvas.delete('all')
        self.searchImage= ImageTk.PhotoImage(file= \
         "./images/searchScreen.png")
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.inputBox = Entry(self.canvas, font= "Helvetica 18")
        self.canvas.create_text(self.width/2, self.height/5, text= "Enter a movie title here", fill= "black", font= "Helvetica 18 bold")
        self.canvas.create_window(self.width/2, self.height/3, window=self.inputBox)
        self.recButton= Button(self, text= "Get Recs", width= 10, bg= "black", fg= "white", command= self.showTerminal) 
        self.canvas.create_window(self.width/4*3, self.height/3, window=self.recButton)
        self.homeButton= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton)
        
    def showTerminal(self):
        self.canvas.delete('movie')
        inputText= str(self.inputBox.get())
        for i in range(10):
            self.titleButton= Button(self, text= inputText + str(i), width= self.inputBox['width'], bg= "black", fg= "white", command=self.newScreen)
            self.canvas.create_window(self.width/2, self.height/2+i*20, window=self.titleButton)
    
    def newScreen(self):
        self.canvas.delete('all')
        self.homeButton2= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton2)
        self.movieBg= ImageTk.PhotoImage(file= \
            "./images/movieScreen.png")
        self.canvas.create_image(self.width/2, self.height/2, \
            image= self.movieBg)

recUI = UI()
recUI.mainloop()








