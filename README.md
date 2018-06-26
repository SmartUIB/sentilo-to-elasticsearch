# sentilo-to-elasticsearch

Utility script to connect Sentilo v1.7.0 with Elasticsearch v6.3.0.

Sentilo v1.7.0 does not match indexes in Elasticsearch v6.3.0. This script does a Man In The Middle approach in order to modify the needed data to work with Elasticsearch.

## How To Use
1. Put Sentilo index template into Elasticsearch. We can do this by sending the next curl to Elasticsearch
```
curl -X PUT "<elasticsearch url>:<elasticsearch port>/_template/sentilo" -H 'Content-Type: application/json' -d @sentilo-index-template.json
```

2. Modify elasticsearch_bulk.py with Elasticsearch url and port to send bulk data
```
ELASTIC_URL = # your URL goes here
ELASTIC_PORT = # same with port
```

3. Execute `python elasticsearch_bulk.py [<ip> <port>]`

4. Modify Sentilo Elasticsearch config files in order to send bulk data to script instead of Elasticsearch
```
elasticsearch.url = http://<script ip>:<script port>
```
at
`sentilo-agent-activity-monitor/src/main/resources/properties/monitor-config.properties`

5. Run Sentilo


Sentilo will now send data to the script as if it was for Elasticsearch itself and Elasticsearch will receive it transformed.
