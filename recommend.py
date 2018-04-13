# import the necessary modules
import pandas as pd
import numpy as np
import string
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# read the data files
credits= pd.read_csv('./the-movies-dataset/credits.csv', sep= ',')
keywords= pd.read_csv('./the-movies-dataset/keywords.csv', sep= ',')
# ratings= pd.read_csv('./the-movies-dataset/ratings.csv', sep= ',')
fields= ['id', 'genres', 'title', 'vote_average', 'vote_count']
metadata= pd.read_csv('./the-movies-dataset/movies_metadata.csv', sep= ',', \
low_memory= False, usecols= fields)

###############################################################################
# Data Cleaning 
###############################################################################
# merge keywords, credits, and metadata for analysis
# metadata id column has invalid values; they should be eliminated 
invalid= []
metadataLen= len(metadata['id'])
for i in range(metadataLen):
    for j in metadata['id'][i]:
        if j not in string.digits:
            invalid.append(i)
            break
metadata= metadata.drop(invalid)
# convert ids into int
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
metadata['id'] = metadata['id'].astype('int')
# perform merging 
allFeatures = metadata.merge(credits, on='id')
allFeatures = allFeatures.merge(keywords, on='id')
# look at top 3 actors, plot keywords, and genre for recommendation criteria
measures = ['cast','keywords', 'genres']
for measure in measures:
    allFeatures[measure] = allFeatures[measure].apply(literal_eval)

################################################################################
# Data Selection
################################################################################

#get top 3 of each of the features, if unavailable, return empty list
def getTop3(feature):
    if isinstance(feature, list):
        lst = [i['name'] for i in feature]
        if len(lst) > 3:
            lst = lst[:3]
        return lst
    return []

def lowerStripSpace(feature):
    l=[]
    # strip spaces and convert everything to lowercase
    for i in feature:
        i=i.replace(" ", "")
        l.append(i.lower())
    return l

for measure in measures:
    allFeatures[measure]= allFeatures[measure].apply(getTop3)
    allFeatures[measure]= allFeatures[measure].apply(lowerStripSpace)

def searchString(movie):
    return ' '.join(movie['keywords']) + ' ' + ' '.join(movie['cast']) + ' ' \
    + ' '.join(movie['genres'])

allFeatures['search'] = allFeatures.apply(searchString, axis='columns')

###############################################################################
# Machine Learning
###############################################################################

#convert titles into lower case and strip space 
def normalizeTitle(title):
    t= title.lower()
    words= t.split(' ')
    words= "".join(words)
    return words

# create a reverse lookup table for movie id and normalized movie title
allFeatures['title']= allFeatures['title'].apply(str)
allFeatures['newTitle']= allFeatures['title'].apply(normalizeTitle)
indices = pd.Series(allFeatures.index, index=allFeatures['newTitle'])

# get cosine similarity scores for all movies given a movie title
def showCos(title):
    # find the index of the movie title input 
    i= indices[title]
    # get corresponding search string
    vocab= (allFeatures['search'][i]).split(" ")
    countVector = CountVectorizer(stop_words='english', vocabulary= vocab)
    countData = countVector.fit_transform(allFeatures['search'])
    cosScore = cosine_similarity(countData[i], countData)
    return cosScore


def getTitleRecs():
    title= str(input('Enter a movie title:'))
    # normalize input
    title= normalizeTitle(title)
    scores= showCos(title)
    # convert into tuples of movie id and score
    scoresLst= list(enumerate(scores[0]))
    # sort the tuples by the score
    scoresLst.sort(key= lambda x: x[1], reverse= True)
    # get top 10 movie recs
    for i, score in scoresLst[1:11]:
        print(allFeatures['title'][i])




    
