from elasticsearch import Elasticsearch, helpers
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import csv, sys
from pydantic import BaseModel
from zipfile import ZipFile

# unzip the data
# with ZipFile("charts.zip","r") as zip_ref:
#     zip_ref.extractall(".")

# set field size limit to avoid issues with long csv columns
csv.field_size_limit(sys.maxsize)


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
es.options(ignore_status=[400,404]).indices.delete(index='charts')
with open('./charts.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='charts')


@app.get("/health")
def health():
    return {'success': True, 'message': 'healthy :)'}


# endpoint that allows users to search on the frontend :)
@app.post("/search")
def search(search_query: SearchQuery):
    es = Elasticsearch("http://elastic:9200")
    # doc = {
    #     "size" : 10,
    #     "query": {
    #         "match": {
    #             "name": {
    #                 "query": search_query.text,
    #                 "fuzziness": 2
    #             }
    #         }
    #     }
    # }
    doc = {
        "query": {
        "bool": {
          "must": [
            {
              "match": {
                "expansion": search_query.text,
                #"fuzziness":2
                
              }
            }
          ]
        }
      }
}
    res = es.search(index='charts', body=doc, scroll='1m')

    # get results
    data = [x['_source'] for x in res['hits']['hits']]
    print("DATA ", data)


    return {"query": search_query.text, 'success': True, 'results': data}
