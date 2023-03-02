#!/usr/bin/env python
# coding: utf-8

# In[2]:


from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
from gensim.models import Word2Vec
import pandas as pd
import nltk
import emoji
import spacy


# In[9]:


df = pd.read_csv(r"slang_2020_tweets.csv")
#df.head(10)


# In[148]:


# clean&gather corpus
corpus_text = "n".join(df[:]["text"])


# In[150]:


data_token = []
for i in sent_tokenize(corpus_text):
    temp = []
    lst_temp = word_tokenize(i)
    # tokenize the sentence into words
    for j in range(len(lst_temp)):
        temp_lst = []
        #print(lst_temp[j])
        # to clean data: delete @_ s and hashtags
        if j>0:
            if lst_temp[j-1]!="@" and lst_temp[j-1]!="@" and            lst_temp[j] not in ["@","#","&","\\","/","...",":",".","!","amp",";",","]:           
                temp.append(lst_temp[j].lower())
        else:
            if lst_temp[j] not in ["@","#","&","\\","/","...",":",".","!","amp",";",","]            and lst_temp[j]:         
                temp.append(lst_temp[j].lower())
    temp_update=[]
    for element in temp:
        lst_temp = list(element)
        # in case that the element contains any untokenized emoji
        # store each emoji separately
        for k in range(len(lst_temp)):
            symbol = lst_temp[k]
            #print(symbol)
            if symbol in emoji.EMOJI_DATA:
                temp_update.append(symbol)
                lst_temp[k]=" "
        str_temp = "".join(lst_temp)
        str_temp_lst = str_temp.split(" ")
        for e in str_temp_lst:
            if e:
                temp_update.append(e.strip())
    data_token.append(temp_update)
    #print(temp_update)


# In[151]:


model = gensim.models.Word2Vec(data_token, min_count = 1, vector_size = 200, window = 6, sg = 1)


# In[153]:


model.save('model.bin')

