import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

credits= pd.read_csv('./the-movies-dataset/credits.csv', sep= ',')
print(credits.head(5))