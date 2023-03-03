FROM docker.elastic.co/elasticsearch/elasticsearch:8.1.0

HEALTHCHECK --interval=5s --timeout=3s --retries=50 CMD curl -f -X GET "http://localhost:9200/_cluster/health?" || exit 1