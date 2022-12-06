import json 
from Connection.elastic_con import client
import os
index_name = "slang-demo-json"
#columns = ["id", "acronym", "meaning"]
from pathlib import Path
path_to_json = '/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/slang/'

for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
  with open(path_to_json + file_name) as json_file:
        


#with open("/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/slang/slang.json") as fi:
    # reader = json.DictReader(
    #     fi, fieldnames=columns, delimiter=",", quotechar='"'
    # )

        reader = json.loads(json_file.read())

    # This skips the first row which is the header of the CSV file.
    # next(reader)
    
        actions = []
        # print(json.dumps(reader, indent=4))
        for index in range(len(reader)):
            action = {"index": {"_index": index_name, "_id": index}}
            doc = {
                "id": int(index),
                "acronym": tuple(reader.items())[index][0],
                "meaning": tuple(reader.items())[index][1]
            }
            actions.append(json.dumps(action))
            actions.append(json.dumps(doc))



    #with open("/Users/anureddy/Desktop/Sem01/DataScience_for_text_analytics/Project1/slang/slang.csv", "w") as fo:
        #fo.write("\n".join(actions))

        client.bulk("\n".join(actions))