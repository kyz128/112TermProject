# source: https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# list of text documents
# text = ["The quick brown fox jumped over the lazy dog."]
# # create the transform
# vectorizer = CountVectorizer()
# # tokenize and build vocab
# vectorizer.fit(text)
# vector = vectorizer.transform(text)

# S1 = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] 
# S2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
# print(cosine_similarity([S1, S2],[S1, S2])



# from tkinter import *
# 
# def showTerminal():
#     canvas.delete('recs', 'recs2')
#     inputText= str(e.get())
#     canvas.create_text(450, 185, text=inputText, fill= "white", font= "Helvetica 12", tags= "recs")
#     canvas.create_text(500, 185, text=inputText, fill= "white", font= "Helvetica 12", tags= "recs2")
# 
# root = Tk()
# canvas = Canvas(root, width = 900, height = 500)
# canvas.pack()
# canvas.create_rectangle(0,0,960, 540, fill= "black")
# e = Entry(canvas)
# canvas.create_text(450, 100, text= "Enter a movie title here", fill= "white", font= "Helvetica 18")
# canvas.create_window(400, 150, window=e)
# b= Button(root, text= "Get Recs", width= 10, command= showTerminal)
# canvas.create_window(530, 150, window=b)
# root.mainloop()


