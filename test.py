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



#images from 
#https://www.listchallenges.com/movies-that-you-cant-live-life-without-seeing
#https://www.pinterest.com/pin/414683078161007928/
#https://www.123rf.com/photo_3985403_tv-channel-movie-guide-on-abstract-background.html
#http://www.pixempire.com/icon/square-with-star-icon.html


from tkinter import *
from recommend import *

class UI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.width= 900
        self.height= 500
        self.canvas = Canvas(self, width = self.width, height = \
        self.height)
        self.canvas.pack()
        self.favoriteLst= []
        self.titleLst2= ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        self.searchImage= PhotoImage(file="./images/searchScreen.png")
        self.welcomeScreen()
    
    def welcomeScreen(self):
        # first screen that displays
        self.canvas.delete('all')
        self.startImage= PhotoImage(file= "./images/startImage.png")
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.startImage)
        self.canvas.create_text(self.width/3, self.height/3, text= "MovieScout", font= "Helvetica 48 bold", fill= "black")
        self.var = StringVar(self)
        self.var.set('Getting Started')
        self.options = OptionMenu(self, self.var, \
        'Title Recommendations', command=self.titleScreen)
        self.options.config(bg= "black", fg= "white",font= "Helvetica 15")
        self.options['menu'].config(bg= "black", fg= "white", font= "Helvetica 12")
        self.options['menu'].add_command(label='Genre Recommendations', command=self.genreScreen)
        self.options['menu'].add_command(label='Mood Recommendations', command= "")
        self.canvas.create_window(self.width/3, self.height/4*3, window=self.options)

    def genreScreen(self):
        # genre buttons 2 columns
        self.canvas.delete('all')
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.canvas.create_text(self.width/2+20, self.height/6, text= "Genres", fill= "black", font= "Helvetica 18 bold")
        self.homeButton= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton)
        self.genreList= ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Documentary', 'Family', 'Fantasy', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War']
        self.longestLine= max([len(i) for i in self.genreList])
        for i in range(len(self.genreList)):
            self.b= Button(self, width= self.longestLine, text=self.genreList[i], bg= "black", fg= "white", command=lambda i=i:self.topGenreScreen(self.genreList[i]))
            if i> (len(self.genreList)-1)//2:
                self.canvas.create_window(self.width/2+self.longestLine*10, self.height/4+ i%(len(self.genreList)//2)*self.longestLine*3, window= self.b, anchor= NE)
            else:
                self.canvas.create_window(self.width/2, self.height/4+ i*self.longestLine*3, window= self.b, anchor= NE)
        
    def topGenreScreen(self, genre):
        # display listing of top movies by genre
        self.canvas.delete('all')
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.canvas.create_text(self.width/2+20, self.height/6, text= genre, fill= "black", font= "Helvetica 18 bold")
        self.homeButton= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton)
        for i in range(10):
            self.genreButton= Button(self, text= self.titleLst2[i], width= max([len(i) for i in self.genreList]), bg= "black", fg= "white", command=lambda i=i:self.movieScreen(self.titleLst2[i]))
            self.canvas.create_window(self.width/2+20, self.height/3+i*20, window=self.genreButton)
            
    
    def titleScreen(self, val=""):
        # movie recs by title here
        self.canvas.delete('all')
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.inputBox = Entry(self.canvas, font= "Helvetica 18")
        self.canvas.create_text(self.width/2, self.height/5, text= "Enter a movie title here", fill= "black", font= "Helvetica 18 bold")
        self.canvas.create_window(self.width/2, self.height/3, window=self.inputBox)
        self.recButton= Button(self, text= "Get Recs", width= 10, bg= "black", fg= "white", command= self.showMovies) 
        self.canvas.create_window(self.width/4*3, self.height/3, window=self.recButton)
        self.homeButton= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton)
    
    def callAgain(self, title):
        self.titleScreen(self)
        self.againMsg, self.againTitles= getTitleRecs(str(title))
        return self.againMsg, self.againTitles
        
    def showMovies(self, title=""):
        self.canvas.delete("msg")
        # display top 10 title recs
        if title=="":
            self.msg, self.titleLst= getTitleRecs(str(self.inputBox.get()))
        else: 
            self.msg, self.titleLst= getTitleRecs(str(title))
        self.canvas.create_text(self.width/2, self.height/20*9, text=self.msg, fill= "blue", font= "Helvetica 12 bold", tags= "msg")
        for i in range(len(self.titleLst)):
            if self.msg=='Movie not found. Did you mean this:':
                self.titleButton= Button(self, text= self.titleLst[i], width= max([len(i) for i in self.titleLst]), bg= "black", fg= "white", command=lambda i=i:self.showMovies(self.titleLst[i]))
            else: 
                self.titleButton= Button(self, text= self.titleLst[i], width= max([len(i) for i in self.titleLst]), bg= "black", fg= "white", command=lambda i=i:self.movieScreen(self.titleLst[i]))
            self.canvas.create_window(self.width/2, self.height/2+i*20, window=self.titleButton)
    
    def movieScreen(self, title):
        # displays movie info (e.g. plot, year, name, etc.)
        self.mGenre, self.mDate, self.mRate, self.mPlot= getMovieData(title)
        self.canvas.delete('all')
        self.homeButton2= Button(self, text= "Home", width= 10, bg= "black", fg= "white", command= self.welcomeScreen)
        self.canvas.create_window(self.width/12, self.height/12, window=self.homeButton2)
        self.movieBg= PhotoImage(file="./images/movieScreen.png")
        self.canvas.create_image(self.width/2, self.height/2, image= self.movieBg)
        self.canvas.create_text(self.width/3, self.height/6, text= title, font= "Helvetica 18 bold", anchor= NW)
        self.canvas.create_text(self.width/3, self.height/4, text= "Genres: %s" % str(self.mGenre), anchor= NW, font= "Helvetica 12")
        self.canvas.create_text(self.width/3, self.height/4+20, text= "Released Date: %s" % str(self.mDate), anchor= NW, font= "Helvetica 12")
        self.canvas.create_text(self.width/3, self.height/4+40, text= "Rating: %s" % str(self.mRate), anchor= NW, font= "Helvetica 12")
        self.photo= PhotoImage(file= './images/photo.png')
        self.canvas.create_image(self.width/5,self.height/3, image= self.photo)
        self.text= self.reformatPlot(self.mPlot)
        self.canvas.create_text(self.width/3, self.height/20*9, text= self.text, anchor= NW)
        if title not in self.favoriteLst:
            self.removeFavorite(title)
        else:
            self.addFavorite(title)
    
    def addFavorite(self, title):
        # what happens when you favorite a movie
        self.canvas.delete("unfav")
        self.favorite= PhotoImage(file= "./images/favorite.png")
        self.favButton= Button(self, text="Unfavorite  ", command= lambda: self.removeFavorite(title))
        self.favButton.config(image= self.favorite, compound= LEFT)
        self.canvas.create_window(self.width/3, self.height/4+70, window= self.favButton, anchor= NW, tags= "fav")
        if title not in self.favoriteLst:
            self.favoriteLst.append(title)
        print(self.favoriteLst)
    
    def removeFavorite(self, title):
        # when you unfavorite a movie
        self.canvas.delete('fav')
        self.unfavorite= PhotoImage(file= "./images/unfavorite.png")
        self.favButton= Button(self, text="Favorite  ", command= lambda: self.addFavorite(title))
        self.favButton.config(image= self.unfavorite, compound= LEFT)
        self.canvas.create_window(self.width/3, self.height/4+70, window= self.favButton, anchor= NW, tags= "unfav")
        if len(self.favoriteLst) > 0 and title in self.favoriteLst:
            self.favoriteLst.remove(title)
        print(self.favoriteLst)
    
    def reformatPlot(self, text):
        # reformat the plot to make it look nice
        sText= text.split()
        plotlst= []
        for i in sText:
            if len(plotlst)%10==0:
                plotlst.append("\n")
            plotlst.append(i)
        return " ".join(plotlst)
        
        

recUI = UI()
recUI.mainloop()








