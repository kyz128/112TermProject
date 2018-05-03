# User interface
# referenced: http://www.tutorialspoint.com/python/python_gui_programming.htm
#images from 
#https://www.listchallenges.com/movies-that-you-cant-live-life-without-seeing
#https://www.pinterest.com/pin/414683078161007928/
#https://www.123rf.com/photo_3985403_tv-channel-movie-guide-on-abstract-background.html
#http://www.pixempire.com/icon/square-with-star-icon.html
#https://br.freepik.com/icones-gratis/pagina-web-pagina-inicial_768343.htm
#https://www.walmart.com/ip/UTZ-Halloween-Pretzels-Treats-Bags-70ct-35oz/116882017

from tkinter import *
import time
from recommend import *
from PIL import ImageTk, Image  
import MovieScout.MovieScout.run 


class UI(Tk):
    
    @staticmethod
    def readFavorites():
        # read favorited movies from a file
        favorites=[line.rstrip() for line in open("favorites.txt")]
        return favorites
    
    def __init__(self):
        Tk.__init__(self)
        self.width= 900
        self.height= 500
        self.canvas = Canvas(self, width = self.width, height = \
        self.height)
        self.canvas.pack()
        # initalize favorites list
        self.favoriteLst= UI.readFavorites()
        # keeps track of current recommendation method and screen
        self.currentScreen= None
        self.currentListing= None
        self.searchImage= PhotoImage(file="./images/searchScreen.png")
        self.home= PhotoImage(file="./images/home.png")
        self.coverScreen()
        # when window closed, save current favorites list
        self.protocol("WM_DELETE_WINDOW", self.writeFavorites) 
    
    def writeFavorites(self):
        # save the favorited movies to txt file
        self.destroy()
        f= open("favorites.txt", "w+")
        if len(self.favoriteLst)==0:
            f.write("")
        else:
            for i in self.favoriteLst:
                f.write(str(i)+"\n")
        f.close()
    
    def coverScreen(self):
        # very first screen: has title and a start button
        self.canvas.delete('all')
        self.start = Image.open('./images/cover.png')
        self.startImg = ImageTk.PhotoImage(self.start)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.startImg)
        self.canvas.create_text(self.width/2, self.height/3, \
        text="MovieScout", fill="white", font=("ms serif", 48, "bold"))
        self.startButton = Button(self, text="Start", \
        command=self.langScreen, width= 10)
        self.startButton.config(font=('ms serif', 12))
        self.canvas.create_window(self.width/2, self.height/5*4, \
        window=self.startButton)
    
    def langScreen(self):
        # language selection screen
        self.canvas.delete('all')
        self.lang = Image.open('./images/lang.png')
        self.langImg = ImageTk.PhotoImage(self.lang)
        self.canvas.create_image(self.width/2, self.height/2, \
        image=self.langImg)
        self.canvas.create_text(self.width/2, self.height/3, \
        text="Select the movie language", fill="white", \
        font=("ms serif", 25, "bold"))
        # list of available languages
        self.langLst= ["English(en)", "Spanish(es)", "French(fr)", \
        "German(de)", "Italian(it)","Japanese(ja)", "Russian(ru)"]
        self.langVar = StringVar(self)
        # default value is English
        self.langVar.set("English(en)") 
        # initalize drop-down menu for languages
        self.langOption = OptionMenu(self, self.langVar, *self.langLst)
        self.langOption.config(width=30, font=('ms serif', 12))
        self.canvas.create_window(self.width/2, self.height/4*3, \
        window=self.langOption)
        # proceed to main screen 
        self.langButton = Button(self, text="Next", \
        command=self.welcomeScreen, width= 10)
        self.langButton.config(font=('ms serif', 12))
        # go back to initial screen 
        self.backButton= Button(self, text="Back", width=10, \
        bg= "white", fg="black", command=self.coverScreen)
        self.canvas.create_window(self.width/12, self.height/12, \
        window= self.backButton )
        self.canvas.create_window(self.width/4*3, self.height/4*3, \
        window=self.langButton)

    
    def welcomeScreen(self):
        self.canvas.delete('all')
        # save the language selected into self.val
        self.val= self.langVar.get()
        # strip out the language code 
        self.langSelected=self.val[-3:-1]
        self.startImage= PhotoImage(file= "./images/startImage.png")
        self.canvas.create_image(self.width/2,self.height/2, \
            image= self.startImage)
        # different recommendation options
        self.gButton= Button(self, text="Genre Recommendations", \
        width= len("Genre Recommendations"), command=self.genreScreen )
        self.gButton.config(font=("ms serif", 12))
        self.canvas.create_window(self.width/3, self.height/3, \
        window=self.gButton)
        self.fButton= Button(self, text="Favorite Recommendations", \
        width= len("Favorite Recommendations"), command=self.favoriteMovies )
        self.fButton.config(font=("ms serif", 12))
        self.canvas.create_window(self.width/3, self.height/2, \
        window=self.fButton)
        self.tButton= Button(self, text="Title Recommendations", \
        width= len("Title Recommendations"), command=self.titleScreen)
        self.tButton.config(font=("ms serif", 12))
        self.canvas.create_window(self.width/3, self.height/3*2, \
        window=self.tButton)
        # nav buttons
        self.backButton= Button(self, text="Back", width=10, bg= "white", \
        fg="black", command=self.langScreen)
        self.canvas.create_window(self.width/12, self.height/12, \
        window= self.backButton )
    
    def genreScreen(self):
        self.canvas.delete('all')
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.canvas.create_text(self.width/2+20, self.height/6, \
        text= "Genres", fill= "black", font= ("ms serif", 18, "bold"))
        # nav buttons
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)
        # button to see favorites list
        self.favListButton= Button(self, text= "See Favorites", \
        width=len("See Favorites"), bg= "black", fg= "white", \
        command= self.showFavList)
        self.canvas.create_window(self.width/6*5, self.height/12, \
        window=self.favListButton)
        # list of available genres
        self.genreList= ['Action', 'Adventure', 'Animation', 'Comedy', \
        'Crime', 'Drama', 'Documentary', 'Family', 'Fantasy', 'Horror', \
        'Music', 'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War']
        self.longestLine= max([len(i) for i in self.genreList])
        for i in range(len(self.genreList)):
            self.b= Button(self, width= self.longestLine, \
            text=self.genreList[i], bg= "black", fg= "white", \
            command=lambda i=i:self.topGenreScreen(self.genreList[i]))
            # genre listing in 2 columns
            if i> (len(self.genreList)-1)//2:
                self.canvas.create_window(self.width/2+self.longestLine*10, \
                self.height/4+ i%(len(self.genreList)//2)*self.longestLine*3, \
                window= self.b, anchor= NE)
            else:
                self.canvas.create_window(self.width/2, \
                self.height/4+ i*self.longestLine*3, window= self.b, anchor= NE)
        
    def topGenreScreen(self, genre):
        # display listing of top 10 movies given a genre
        self.canvas.delete('all')
        self.currentScreen= "moviesGenreLst"
        self.currentListing= "genres"
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        self.canvas.create_text(self.width/2+20, self.height/6, \
        text= genre, fill= "black", font= ("ms serif", 18, "bold"))
        # nav buttons: home, favorites list
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)
        self.favListButton= Button(self, text= "See Favorites", \
        width=len("See Favorites"), bg= "black", fg= "white", \
        command= self.showFavList)
        self.canvas.create_window(self.width/6*5, self.height/12, \
        window=self.favListButton)
        # back button returns to the genre listing
        self.backButton= Button(self, text="Back", width=10, bg= "black", \
        fg="white", command=self.previousListing)
        self.canvas.create_window(self.width/12, self.height/12, \
        window= self.backButton )
        # save current genre selected to return to that genre listing page 
        # if needed
        self.genreSelected= genre
        # get top movies by genre list given movie language and genre
        self.topGenreLst= getGenreRec(genre, self.langSelected)
        for i in range(len(self.topGenreLst)):
            self.genreButton= Button(self, text= self.topGenreLst[i], \
            width= max([len(i) for i in self.topGenreLst]), bg= "black", \
            fg= "white", \
            # pass in current i for the corresponding button selected
            command=lambda i=i:self.movieScreen(self.topGenreLst[i]))
            self.canvas.create_window(self.width/2+20, self.height/3+i*20, \
            window=self.genreButton)
            
    def titleScreen(self, val=""):
        # movie recs by title here
        self.canvas.delete('all')
        self.currentScreen= "moviesTitleLst"
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)  
        # enter movie title in text entry box
        self.inputBox = Entry(self.canvas, font= ("ms serif", 18, "bold"))
        self.canvas.create_text(self.width/2, self.height/5, \
        text= "Enter a movie title here", fill= "black", \
        font= ("ms serif", 18, "bold"))
        self.canvas.create_window(self.width/2, self.height/3, \
        window=self.inputBox)
        self.recButton= Button(self, text= "Get Recs", width= 10, \
        bg= "black", fg= "white", command= self.showMovies) 
        self.canvas.create_window(self.width/4*3, self.height/3, \
        window=self.recButton)
        # nav buttons
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)    
        
    def showMovies(self, title=""):
        # display top 10 title recs
        # delete previous title recs output
        self.canvas.delete("msg", "movieLst")
        # save input text/results of search for when back button pressed
        self.inputText= self.inputBox.get()
        # if title not misspelled, pass inputText into ML function 
        if title=="":
            self.msg, self.titleLst= \
            getTitleRecs(str(self.inputText), self.langSelected)
        else: 
            self.msg, self.titleLst= getTitleRecs(str(title), self.langSelected)
        self.canvas.create_text(self.width/2, self.height/20*9, \
        text=self.msg, fill= "blue", font= ("ms serif", 12, "bold"), tags="msg")
        for i in range(len(self.titleLst)):
             # if misspelled title input call title recs again but pass 
            # in suggested title for recommendation
            if self.msg=='Movie not found. Did you mean this:':
                self.titleButton= Button(self, text= self.titleLst[i], \
                width= max([len(i) for i in self.titleLst]), bg= "black", \
                fg= "white", \
                command=lambda i=i:self.showMovies(self.titleLst[i]))
            else: 
                self.titleButton= Button(self, text= self.titleLst[i], \
                width= max([len(i) for i in self.titleLst]), bg= "black", \
                fg= "white", \
                command=lambda i=i:self.movieScreen(self.titleLst[i]))
            self.canvas.create_window(self.width/2, self.height/2+i*20, \
            window=self.titleButton, tags="movieLst")
    
    def previousSearch(self):
        # when back button pressed on the movie description screen
        self.canvas.delete("all")
        # if currently doing title recs, display previous search output
        if self.currentScreen=="moviesTitleLst":
            self.titleScreen()
            self.showMovies(self.inputText)
        # if genre recs, return to the given genre page with movie listing
        elif self.currentScreen=="moviesGenreLst":
            self.topGenreScreen(self.genreSelected)
        # if fav recs, return to listing of favorite recs
        elif self.currentScreen=="moviesFavLst":
            self.favoriteMovies()
    
    def previousListing(self):
        # when back button pressed on the listing pages
        # if on specific genre page, return to listing of all genres
        if self.currentListing=="genres":
            self.genreScreen()
        # if on favorite recs page, return to list of favorite movies
        elif self.currentListing=="favs":
            self.showFavList()
    
    def movieScreen(self, title):
        # displays movie info (e.g. plot, year, name, etc.) given title
        # pass in the movie title to the urls.txt for image scraping
        f= open("urls.txt", "w+")
        # format it so that it can be recognized by the IMDB search site
        self.titleSplit= title.split()
        self.url= "+".join(self.titleSplit)
        f.write(self.url)
        f.close()
        # get movie data
        self.mGenre, self.mDate, self.mRate, self.mPlot= \
        getMovieData(title, self.langSelected)
        self.canvas.delete('all')
        # nav buttons
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)
        self.favListButton= Button(self, text= "See Favorites", \
        width=len("See Favorites"), bg= "black", fg= "white", \
        command= self.showFavList)
        self.canvas.create_window(self.width/6*5, self.height/12, \
        window=self.favListButton)
        self.backButton= Button(self, text="Back", width=10, bg= "black", \
        fg="white", command=self.previousSearch)
        self.canvas.create_window(self.width/12, self.height/12, \
        window= self.backButton )
        #run spider to scrape images
        MovieScout.MovieScout.run.runSpider()
        self.movieBg= PhotoImage(file="./images/movieScreen.png")
        self.canvas.create_image(self.width/2, self.height/2, \
        image= self.movieBg)
        self.canvas.create_text(self.width/3, self.height/6, \
        text= title, font= ("ms serif", 18, "bold"), anchor= NW)
        self.canvas.create_text(self.width/3, self.height/4, \
        text= "Genres: %s" % str(self.mGenre), anchor= NW, font=("ms serif",12))
        self.canvas.create_text(self.width/3, self.height/4+20,\
        text= "Released Date: %s" % str(self.mDate), anchor= NW, \
        font= ("ms serif", 12))
        # round rating to 2 decimal places
        self.canvas.create_text(self.width/3, self.height/4+40, \
        text= "Rating: %0.2f" % float(self.mRate), anchor= NW, \
        font= ("ms serif", 12))
        # ensure filename valid 
        if ":" in self.url:
            self.url= str(self.url).replace(":", "")
        else: self.imgTitle= str(self.url)
        # wait for images to be downloaded so they can be called
        time.sleep(5)
        try:
            self.img = Image.open('C:/Users/kimbe/Documents/15112/TermProject/images/full/%s.jpg' % self.imgTitle)
        except:
            # draw placeholder image if movie poster not found
            self.img = Image.open('./images/placeholder.jpeg')
        self.movieimg = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.width/5,self.height/5*2, image= self.movieimg)
        self.text= UI.reformatPlot(self.mPlot)
        self.canvas.create_text(self.width/3, self.height/20*9, \
        text= self.text, anchor= NW)
        # control display of the favorite button when revisitng a movie
        if title not in self.favoriteLst:
            self.removeFavorite(title)
        else:
            self.addFavorite(title)
    
    def showFavList(self):
        # list of favorited movies on screen
        self.canvas.delete('all')
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)
        self.canvas.create_text(self.width/2+20, self.height/6, \
        text= "Favorites", fill= "black", font= ("ms serif", 18, "bold"))
        # nav buttons
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)
        self.favRecsButton= Button(self, text= "Get Fav Recs", \
        width=len("Get Fav Recs"), bg= "black", fg= "white", \
        command=self.favoriteMovies)
        self.canvas.create_window(self.width/6*5, self.height/12, \
        window=self.favRecsButton)
        # when fav list empty
        if len(self.favoriteLst)==0:
            self.canvas.create_text(self.width/2, self.height/3, \
            text="Nothing in Favorites!", fill= "blue", \
            font=("ms serif", 14, "bold"))
        else: 
            for i in range(len(self.favoriteLst)):
                self.favMovieButton= Button(self, text= self.favoriteLst[i], \
                width= max([len(i) for i in self.favoriteLst]), bg= "black",\
                 fg= "white", \
                 command=lambda i=i:self.movieScreen(self.favoriteLst[i]))
                self.canvas.create_window(self.width/2+20, self.height/3+i*20,\
                window=self.favMovieButton)
    
    def favoriteMovies(self):
        # rec screen based on favorites list
        self.canvas.delete("all")
        self.currentScreen= "moviesFavLst"
        self.currentListing="favs"
        self.canvas.create_image(self.width/2, self.height/2, \
         image= self.searchImage)
        # nav buttons
        self.homeButton= Button(self, bg= "black", fg= "white", \
        command= self.welcomeScreen)
        self.homeButton.config(image= self.home, compound= CENTER)
        self.canvas.create_window(self.width/12, self.height/12*11, \
        window=self.homeButton)
        self.backButton= Button(self, text="Back", width=10, bg= "black", \
        fg="white", command=self.previousListing)
        self.canvas.create_window(self.width/12, self.height/12, \
        window= self.backButton )
        self.canvas.create_text(self.width/2, self.height/5, \
        text= "Favorites Recommendation", fill= "black", \
        font= ("ms serif", 18, "bold"))
        # display recommendations
        self.favMsg, self.favTitles= \
        getFavorites(self.favoriteLst, self.langSelected)
        self.canvas.create_text(self.width/2, self.height/3, \
        text= self.favMsg, fill= "blue", font= ("ms serif", 12, "bold"))
        for i in range(len(self.favTitles)):
            self.favMovie= Button(self, text= self.favTitles[i], \
            width= max([len(i) for i in self.favTitles]), bg= "black", \
            fg= "white", command=lambda i=i:self.movieScreen(self.favTitles[i]))
            self.canvas.create_window(self.width/2, self.height/20*9+i*20, \
            window=self.favMovie)
        
    def addFavorite(self, title):
        # what happens when you favorite a movie
        self.canvas.delete("unfav")
        self.favorite= PhotoImage(file= "./images/favorite.png")
        # when favorite button pressed again, movie unfavorited
        self.favButton= Button(self, text="Unfavorite  ", \
        command= lambda:self.removeFavorite(title))
        self.favButton.config(image= self.favorite, compound= LEFT)
        self.canvas.create_window(self.width/3, self.height/4+70, \
        window= self.favButton, anchor= NW, tags= "fav")
        # only add to favorites list if not already in it
        if title not in self.favoriteLst:
            self.favoriteLst.append(title)
    
    def removeFavorite(self, title):
        # when you unfavorite a movie
        self.canvas.delete('fav')
        self.unfavorite= PhotoImage(file= "./images/unfavorite.png")
        self.favButton= Button(self, text="Favorite  ", \
        command= lambda: self.addFavorite(title))
        self.favButton.config(image= self.unfavorite, compound= LEFT)
        self.canvas.create_window(self.width/3, self.height/4+70, \
        window= self.favButton, anchor= NW, tags= "unfav")
        # only legal to remove when len of list >0 and movie in list
        if len(self.favoriteLst) > 0 and title in self.favoriteLst:
            self.favoriteLst.remove(title)
    
    @staticmethod
    def reformatPlot(text):
        # reformat the plot to make it look nice
        sText= str(text).split()
        plotlst= []
        for i in sText:
            if len(plotlst)%12==0:
                plotlst.append("\n")
            plotlst.append(i)
        return " ".join(plotlst)

recUI = UI()
recUI.mainloop()