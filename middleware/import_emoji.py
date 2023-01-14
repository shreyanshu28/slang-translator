import json 
import sys
 
sys.path.insert(1, '/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/slang-translator/Connection')

from elastic_con import client 
from elasticsearch import Elasticsearch, helpers
import os     
index_name = "emo31"
with open("/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/emojilib-main/dist/emoji-en-US.json") as fi:
    
    #reader = json.DictReader(fi, fieldnames=columns, delimiter=",", quotechar='"')

    reader = json.loads(fi.read().encode('UTF-16'))

#     # This skips the first row which is the header of the CSV file.
#     # next(reader)
    
    actions = []
#         # print(json.dumps(reader, indent=4))
    for index in range(len(reader)):
        action = {"index": {"_index": index_name}}
        doc = {
                 "id": int(index),
                 "emoji": tuple(reader.items())[index][0],
                 "meaning": tuple(reader.items())[index][1]
             }
        actions.append(json.dumps(action))
        actions.append(json.dumps(doc))



#     #with open("/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/slang/slang.csv", "w") as fo:
#         #fo.write("\n".join(actions))

try:
    # make the bulk call, and get a response
    response = helpers.bulk(client, actions,index =index_name,doc_type = 'emojis')

    #response = helpers.bulk(elastic, actions, index='employees', doc_type='people')
    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)
 
  
index_name = "emo31"
request = '''{"query": {"match_all": {}}}'''
results = client.search(index=index_name, body=request,size = 100)['hits']['hits']
print(results)