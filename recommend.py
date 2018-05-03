# perform the machine learning on data
# import the necessary modules
# referenced sklearn documentation; see following links 
#http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# pandas syntax: referenced course notes; took online class "Python for Data Science" by University of California San Diego

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
fields= ['id', 'genres', 'original_title', 'release_date', 'vote_average', \
'vote_count', 'overview', "original_language"]
metadata= pd.read_csv('./the-movies-dataset/movies_metadata.csv', sep= ',', \
low_memory= False, usecols= fields)

###############################################################################
# Data Cleaning 
###############################################################################
# merge keywords, credits, and metadata for analysis
# see TP Data Exploration.pdf for more info
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
# feature dictionaries enclosed by strings; literal_eval gets rid of them
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

# weighted rating formula adapted from 
#https://math.stackexchange.com/questions/942738/
#algorithm-to-calculate-rating-based-on-multiple-reviews-using-both-review-score

allFeatures["weighted_rating"]= 5*allFeatures["vote_average"]/10 + \
 5*(1-math.e**(-allFeatures["vote_count"]/10)).round(2)

def toString(lst):
    return " ".join(lst)

#join the elements to form aggregate search criteria
def searchString(movie):
    return ' '.join(movie['keywords']) + ' ' + ' '.join(movie['cast']) + ' ' \
    + ' '.join(movie['genres'])

allFeatures['search'] = allFeatures.apply(searchString, axis='columns')
# to evaluate if movie is part of a certain genre 
allFeatures["genresStr"]= allFeatures['genres'].apply(toString)

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

# select a subset of allFeatures; specifically only rows where 
# the original_language is what is selected in the ui
def langData(lang):
    allFeaturesCopy= \
    allFeatures[allFeatures["original_language"]==lang].copy(deep=True)
    # create a new lookup table for the slice
    allFeaturesCopy.reset_index(drop=True, inplace=True)
    indicesCopy = \
    pd.Series(allFeaturesCopy.index, index=allFeaturesCopy['newTitle'])
    return allFeaturesCopy, indicesCopy
    
# get cosine similarity scores for all movies given a movie title and lang
def showCos(title, lang):
    data, index= langData(lang)
    # get movie id
    i= index[title]
    # find corresponding search string and use it as criteria to evaluate
    # similarity 
    vocab= (data['search'][i]).split(" ")
    countVector = CountVectorizer(stop_words='english', vocabulary= vocab)
    countData = countVector.transform(data['search'])
    # compare the how similar a given movie is to all other movies 
    cosScore = cosine_similarity(countData[i], countData)
    return cosScore

# compute cosine similarity for typed in word and all movies in database
def similarTitle(word, lang):
    data, index= langData(lang)
    countVector = CountVectorizer(stop_words='english')
    # vocabulary is created from all movie titles 
    c = countVector.fit(data['original_title'])
    # evaluate word input 
    cosScore = \
    cosine_similarity(c.transform([word]), c.transform(data['original_title']))
    return cosScore

def getSpellingSuggestion(word, lang):
    data, index= langData(lang)
    suggestionLst=[]
    simTitle= similarTitle(word, lang)
    # assign each score their corresponding movie id
    sim= list(enumerate(simTitle[0]))
    # most similar titles show up first
    sim.sort(key= lambda x: x[1], reverse= True)
    # get top 3 suggestions
    for j, val in sim[0:3]:
        if sim[0][1] < 0.2:
            return 'No movie exist with that name. Check your spelling.', []
        cautionText= 'Movie not found. Did you mean this:'
        suggestionLst.append(data['original_title'][j])
    return cautionText, suggestionLst
    

def getTitleRecs(inputTitle, lang):
    titlesLst=[]
    try:
        title= inputTitle
        # convert title input into all lowercase and no space
        normTitle= normalizeTitle(title)
        scores= showCos(normTitle, lang)
        data, index= langData(lang)
        scoresLst= list(enumerate(scores[0]))
        scoresLst.sort(key= lambda x: x[1], reverse= True)
        successText= 'You might like these movies:'
        # skip most similar because that is the movie passed in 
        for i, score in scoresLst[1:11]:
            titlesLst.append(data['original_title'][i])
        return successText, titlesLst
    except:
        # if error, try to give spell suggestions
        try:
            return getSpellingSuggestion(inputTitle, lang)
        except: 
            return 'Error!', []


def showFavCos(titleLst, lang):
    # ensure no duplicates in vocab
    allVocab=set()
    data, index= langData(lang)
    for i in titleLst:
        inx= index[i]
        vocab= (data['search'][inx]).split(" ")
        for j in vocab:
            allVocab.add(j)
    # turn final vocab list into string; compatible with search string dtype
    s= " ".join(list(allVocab))
    countVector = CountVectorizer(stop_words='english')
    # use search string as basis for evaluation 
    countData = countVector.fit(data["search"])
    cosScore = cosine_similarity(countVector.transform([s]), countVector.transform(data['search']))
    return cosScore
    
def getFavorites(favList, lang):
    titlesLst=[]
    newFavList=[]
    # skip movies already in the favorites list
    skipNum= len(favList)
    if len(favList)==0:
        return "Nothing in favorites", []
    data, index= langData(lang)
    try:
        # reformat all titles in favorites list and store them in newFavList
        for i in favList:
            j=normalizeTitle(i)
            newFavList.append(j)
        scores= showFavCos(newFavList, lang)
        favScores= list(enumerate(scores[0]))
        favScores.sort(key= lambda x: x[1], reverse= True)
        successText= 'You might like these movies:'
        # get top 10 recommended movies
        for k, score in favScores[skipNum+1:skipNum+11]:
            titlesLst.append(data['original_title'][k])
        return successText, titlesLst
    except:
        return "Error!", []

def getGenreRec(genre, lang):
    # return top 10 movies given genre and lang
    genreNorm= normalizeTitle(genre)
    #filter movies by genre and lang
    sliced= \
    allFeatures[(allFeatures["genresStr"].str.contains(genreNorm)) & (allFeatures["original_language"]==lang)].copy(deep=True)
    # sort by rating descending
    sliced.sort_values(by= "weighted_rating", inplace= True, ascending= False)
    # reset index to account for excluded movies
    sliced.reset_index(drop=True, inplace= True)
    return sliced["original_title"][0:10]

def getMovieData(title, lang):
    # return genre, released date, rating, and plot 
    data, index= langData(lang)
    normTitle= normalizeTitle(title)
    i= index[normTitle]
    return data["genres"][i], data["release_date"][i], \
    data["weighted_rating"][i], data["overview"][i]



    
