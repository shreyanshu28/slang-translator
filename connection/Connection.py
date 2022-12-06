import elasticsearch
from elasticsearch import Elasticsearch
import os

# Set environment variables
os.environ['ES_USER'] = 'elastic'
os.environ['ES_PASSWORD'] = '1234'
index = 'slang_104'
client = Elasticsearch (
    hosts = ["http://localhost:9200"],
    http_auth = (
        os.environ.get('ES_USER'),
        os.environ.get('ES_PASSWORD')
    )
)
print(client)