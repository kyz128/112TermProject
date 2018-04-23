# get title-based recommendations 
# import the necessary modules
import pandas as pd
import numpy as np
import string
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

# read the data files
credits= pd.read_csv('./the-movies-dataset/credits.csv', sep= ',')
keywords= pd.read_csv('./the-movies-dataset/keywords.csv', sep= ',')
# ratings= pd.read_csv('./the-movies-dataset/ratings.csv', sep= ',')
fields= ['id', 'genres', 'original_title', 'release_date', 'vote_average', \
'vote_count']
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
# sort rows by newest release date
allFeatures.sort_values(by="release_date", ascending= False, inplace= True)
# drop duplicate names; keep the newest movie
allFeatures.drop_duplicates(subset= "original_title", keep="first", \
inplace= True)
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
allFeatures['original_title']= allFeatures['original_title'].apply(str)
allFeatures['newTitle']= allFeatures['original_title'].apply(normalizeTitle)
# reset index to account for dropped rows
allFeatures.reset_index(drop=True, inplace=True)
indices = pd.Series(allFeatures.index, index=allFeatures['newTitle'])

# get cosine similarity scores for all movies given a movie title
def showCos(title):
    # find the index of the movie title input 
    i= indices[title]
    # get corresponding search string
    vocab= (allFeatures['search'][i]).split(" ")
    countVector = CountVectorizer(stop_words='english', vocabulary= vocab)
    countData = countVector.transform(allFeatures['search'])
    cosScore = cosine_similarity(countData[i], countData)
    return cosScore

def similarTitle(word):
    # return similarity scores between movie title input & titles in data
    countVector = CountVectorizer(stop_words='english')
    # vocabulary from all titles
    c = countVector.fit(allFeatures['original_title'])
    # matrix of scores 
    cosScore = cosine_similarity(c.transform([word]), c.transform(allFeatures['original_title']))
    return cosScore

def getSpellingSuggestion(word):
    suggestionLst=[]
    simTitle= similarTitle(word)
    sim= list(enumerate(simTitle[0]))
    sim.sort(key= lambda x: x[1], reverse= True)
    # get top 3 suggestions
    for j, val in sim[0:3]:
        if sim[0][1] < 0.2:
            return 'No movie exist with that name. Check your spelling.'
        cautionText= 'Movie not found. Did you mean this:'
        suggestionLst.append(allFeatures['original_title'][j])
    return cautionText, suggestionLst
    

def getTitleRecs(inputTitle):
    titlesLst=[]
    try:
        title= inputTitle
        # normalize input
        normTitle= normalizeTitle(title)
        scores= showCos(normTitle)
        # convert into tuples of movie id and score
        scoresLst= list(enumerate(scores[0]))
        # sort the tuples by the score
        scoresLst.sort(key= lambda x: x[1], reverse= True)
        # get top 10 movie recs
        successText= 'You might like these movies:'
        for i, score in scoresLst[1:11]:
            titlesLst.append(allFeatures['original_title'][i])
        return successText, titlesLst
    except:
        try:
            return getSpellingSuggestion(inputTitle)
        except: 
            return 'Error!', []

def showFavCos(titleLst):
    # suppress duplicate recommendation criteria
    allVocab=set()
    for i in titleLst:
        inx= indices[i]
        vocab= (allFeatures['search'][inx]).split(" ")
        for j in vocab:
            allVocab.add(j)
    # same format as the data in search column of dataframe
    aggregateSearch= " ".join(list(allVocab))
    countVector = CountVectorizer(stop_words='english')
    countData = countVector.fit(allFeatures["search"])
    cosScore = cosine_similarity(countVector.transform([aggregateSearch]), countVector.transform(allFeatures['search']))
    return cosScore
    
def getFavorites(favList):
    if len(favList)==0:
        return "Nothing in favorites", []
    titlesLst=[]
    newFavList=[]
    #don't return any of the titles inputed as recommendations
    skipNum= len(favList) 
    try:
        for i in favList:
            j=normalizeTitle(i)
            newFavList.append(j)
        #normalize all titles in favorites
        scores= showFavCos(newFavList)
        favScores= list(enumerate(scores[0]))
        favScores.sort(key= lambda x: x[1], reverse= True)
        successText= 'You might like these movies:'
        for k, score in favScores[skipNum+1:skipNum+11]:
            titlesLst.append(allFeatures['original_title'][k])
        return successText, titlesLst
    except:
        return "Error!", []
    
allFeatures["weighted_rating"]= 5*allFeatures["vote_average"]/10 + 5*(1-math.e**(-allFeatures["vote_count"]/10)).round(2)

def getGenreRec(genre):
    genreNorm= normalizeTitle(genre)
    slice= allFeatures[allFeatures["genres_test"].str.contains(genreNorm)]
    slice.sort_values(by= "weighted_rating", inplace= True, ascending= False)
    return slice[0:10]



    
