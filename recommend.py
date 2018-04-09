# import the necessary modules
import pandas as pd
import numpy as np
import copy 
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
nMetadata= copy.deepcopy(metadata)
metadataLen= len(metadata['id'])
for i in range(metadataLen):
    for j in metadata['id'][i]:
        if j not in string.digits:
            nMetadata=nMetadata.drop(nMetadata.index[i])



