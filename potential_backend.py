# -*- coding: utf-8 -*-
"""cs338_demo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eusbAJroHzr3vip4iSTqcIubaUVz3l9-
"""

pip install -U sentence-transformers

# Importing libraries

import math
import http.client
import json
from sentence_transformers import SentenceTransformer, util

"""Part 1: Matching our sentences to available categories and retrieving n-quotes"""

# Downloading the model
# pre vectorization to speed shit up
model = SentenceTransformer('all-mpnet-base-v2')

# Establishing connection with RapidAPI and getting the list of quote categories

conn = http.client.HTTPSConnection("famous-quotes4.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "12362c4f69mshf3bc1981e616ac1p1939abjsnde94f542c73e",
    'X-RapidAPI-Host': "famous-quotes4.p.rapidapi.com"
    }

conn.request("GET", "/", headers=headers)

res = conn.getresponse()
data = res.read()
categories = json.loads(data)

print(categories)

# import http.client

# conn = http.client.HTTPSConnection("famous-quotes4.p.rapidapi.com")

# headers = {
#     'X-RapidAPI-Key': "12362c4f69mshf3bc1981e616ac1p1939abjsnde94f542c73e",
#     'X-RapidAPI-Host': "famous-quotes4.p.rapidapi.com"
#     }

# conn.request("GET", "/random?category=all&count=100000", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# The sentences we'd like to encode
# It's a hard-coded example for the sake of having a quick demo. 
# Later on, this will be replaced directly by the user input.
ourSentences = ["I am so sorry you are going through a hard time. I wish I could be there for you. But don't worry, it will get better!"]

# Get embeddings of sentences
catEmbeddings = model.encode(categories)
sentEmbeddings = model.encode(ourSentences)

# Compute similarities
res = [0]*len(catEmbeddings)
maxSim = -math.inf

# for each category
for i in range(len(catEmbeddings)):
  # calculate the cosine similarity between our sentence embedding 
  # and the given category
  currSim = util.cos_sim(sentEmbeddings, catEmbeddings[i]).item()
  # store the result in a results array
  res[i] = currSim
  # update the maxSim so it stores the highest similarity score
  maxSim = max(maxSim, currSim)


# print("{0:.4f}".format(sim.tolist()[0][0])) 
maxSim

# Now, find the index of the maximum cosine similarity score and retrieve 
# the name of the category
targetCat = categories[res.index(maxSim)]
targetCat

# Establishing connection for GET request
conn = http.client.HTTPSConnection("famous-quotes4.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "12362c4f69mshf3bc1981e616ac1p1939abjsnde94f542c73e",
    'X-RapidAPI-Host': "famous-quotes4.p.rapidapi.com"
    }

# Retrieve 100 quotes with our target category
conn.request("GET", "/random?category={}&count=1000".format(targetCat), headers=headers)

# Retrieving quotes
res = conn.getresponse()
data = res.read()

jsonFormat = json.loads(data)
quotesList = [0]*len(jsonFormat)
for i in range(len(quotesList)):
  quotesList[i] = jsonFormat[i]["text"]

quotesList[0]

"""Part 2: After we got our quotes, we have to repeat the cosine similarity for our sentences and the actual quotes that we retrieved."""

quotesEmbeddings = model.encode(quotesList)

quoteRes = [0]*len(quotesEmbeddings)
maxSimRes = -math.inf

# for each category
for i in range(len(quotesEmbeddings)):
  # calculate the cosine similarity between our sentence embedding 
  # and the quote embedding
  currSimRes = util.cos_sim(sentEmbeddings, quotesEmbeddings[i]).item()
  # store the result in a results array
  quoteRes[i] = currSimRes
  # update the maxSimRes so it stores the highest similarity score
  maxSimRes = max(maxSimRes, currSimRes)


# print("{0:.4f}".format(sim.tolist()[0][0])) 
maxSimRes

# Retrieve the quote with the highest similarity score
targetQuote = quotesList[quoteRes.index(maxSimRes)]
targetQuote

"""Next steps:
1. Figuring out how to retrieve all quotes with a given category tags
2. Amending the code slights to allow for retrieving top-n best matching quotes (linked to "Give me another quote" button)
3. Tuning the model/checking out other pre-defined models OR build/train our own model
4. Exploring other approaches and libraries such as nltk, spacy, etc.
"""

