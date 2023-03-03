from elasticsearch import Elasticsearch, helpers
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import csv, sys
from pydantic import BaseModel
from zipfile import ZipFile
import nltk
import re
import nltk
import spacy
import traceback
import en_core_web_sm
nlp = en_core_web_sm.load()

stop_words = ['a', 'an', 'the','is','iss','but','in','on','to','my']

def remove_stop_words(sentence):
    doc = nlp(sentence)
    filtered_sentence = [token.text for token in doc if not token.is_stop or token.text not in stop_words and not token.is_punct]
    return ' '.join(filtered_sentence)
  
# unzip the data
# with ZipFile("charts.zip","r") as zip_ref:
#     zip_ref.extractall(".")

# set field size limit to avoid issues with long csv columns
csv.field_size_limit(sys.maxsize)

def remove_extra_lengthning(sentence):
    words = sentence.split()
    corrected_words = []
    for word in words:
        i = 3
        while i < len(word):
            if word[i] == word[i-1]:
                word = word[:i] + word[i+1:]
            else:
                i += 1
        corrected_words.append(word)
    return ' '.join(corrected_words)

def convert_words(input_string):
    input_string = input_string.replace("do nt", "do not")
    input_string = input_string.replace("wo nt", "would not")
    input_string = input_string.replace("ca nt", "can not")
    input_string = input_string.replace("sha nt", "shall not")
    input_string = input_string.replace("ai nt", "am not")
    input_string = input_string.replace("ai nt't", "am not")
    input_string = input_string.replace("have nt", "have not")
    input_string = input_string.replace("has nt", "has not")
    input_string = input_string.replace("had nt", "had not")
    input_string = input_string.replace("is nt", "is not")
    input_string = input_string.replace("were nt", "were not")
    input_string = input_string.replace("are nt", "are not")
    #input_string = input_string.replace("'s", "it is")
    return input_string
  
def convert_to_slang(input_string, slang_dict):
    for acronym, meaning in slang_dict.items():
        #print('The input is ',input_string)
        input_string = input_string.replace(meaning, acronym)
    return input_string

def replace_with_emoji(sentence, slang_dict):
  words = sentence.split()
  
  emojified = [next((emoji for emoji, meanings in slang_dict.items() if word in meanings), word) for word in words]
  return " ".join(emojified)

class SearchQuery(BaseModel):
    text: str

app = FastAPI()

origins = [
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# index data into elastic search
es = Elasticsearch("http://elastic:9200")
es.options(ignore_status=[400,404]).indices.delete(index='slang12')
with open('./slang.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='slang12')

index_name = "emo31"
with open("./emoji-en-US.json") as fi:
    

    reader = json.loads(fi.read().encode('UTF-16'))

    
    actions = []
    for index in range(len(reader)):
        action = {"index": {"_index": index_name}}
        doc = {
                 "id": int(index),
                 "emoji": tuple(reader.items())[index][0],
                 "meaning": tuple(reader.items())[index][1]
             }
        actions.append(json.dumps(action))
        actions.append(json.dumps(doc))




try:
    # make the bulk call, and get a response
    response = helpers.bulk(es, actions,index =index_name)

    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)
 
  



@app.get("/health")
def health():
    return {'success': True, 'message': 'healthy :)'}


# endpoint that allows users to search on the frontend :)
@app.post("/search")

def search(search_query: SearchQuery):
    
    sentence = remove_extra_lengthning(search_query.text.lower())
    filtered_sentence = remove_stop_words(sentence)
    converted_string = convert_words(filtered_sentence)
    
    es = Elasticsearch("http://elastic:9200")
    
    doc = {
        "query": {
        "bool": {
          "must": [
            {
              "match": {
                "expansion": converted_string,                
              }
            }
          ]
        }
      }
    }
    
    res = es.search(index='slang12', body=doc, scroll='1m', size=1)['hits']['hits']
    try:
      meaning = []
      acronym  = []
      for d in res:
          meaning.append(d['_source']['expansion'])
          acronym.append(d['_source']['acronym'])
      slang_dict = dict(zip(acronym,meaning))
      slang_sen = convert_to_slang(converted_string,slang_dict)
    
      
    
    
    
      doc = {
          "query": {
          "bool": {
            "must": [
              {
                "match": {
                  "meaning": slang_sen,
                }
              }
            ]
          }
        }
      }
      res = es.search(index='emo31', body=doc, scroll='1m',size=2)['hits']['hits']
      
      meaning = []
      emoji  = []
      for d in res:
          meaning.append(d['_source']['meaning'])
          emoji.append(d['_source']['emoji'])
      emo_dict = dict(zip(emoji,meaning))
      res = replace_with_emoji(slang_sen, emo_dict)
      
    
    except Exception as e:
      print("Exception caught:", e)
      traceback.print_exc()

    return {"query": search_query.text, 'success': True, 'results': res}
  
