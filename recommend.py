# import the necessary modules
import pandas as pd
import numpy as np
import string
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer

# read the data files
credits= pd.read_csv('./the-movies-dataset/credits.csv', sep= ',')
keywords= pd.read_csv('./the-movies-dataset/keywords.csv', sep= ',')
ratings= pd.read_csv('./the-movies-dataset/ratings.csv', sep= ',')
metadata= pd.read_csv('./the-movies-dataset/movies_metadata.csv', sep= ',', \
low_memory= False)

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



    
