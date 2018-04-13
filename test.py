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

S1 = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0] 
S2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
print(cosine_similarity([S1, S2],[S1, S2])

