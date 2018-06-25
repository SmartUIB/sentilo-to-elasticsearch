# sentilo-to-elasticsearch

Utility script to connect Sentilo v1.7.0 with Elasticsearch v6.3.0.

Sentilo v1.7.0 does not match how indexes work in Elasticsearch v6.3.0. This script does a Man In The Middle approach in order to modify the needed data to work with Elasticsearch.

## How To Use
1. Put sentilo template index into Elasticsearch. We can do this by sending the next curl to Elasticsearch
```
curl -X PUT "<elasticsearch url>:<elasticsearch port>/_template/sentilo" -H 'Content-Type: application/json' -d @template.json
```

2. Modify elasticsearch_bulk.py with Elasticsearch url and port to send bulk data
```
ELASTIC_URL = # your URL goes here
ELASTIC_PORT = # same with port
```

3. Execute `python elasticsearch_bulk.py [ <ip> <port> ]`  or modify the inner variables:
```
HOST = # your host
PORT = # a port
```
and then execute the script with no params.

4. Modify Sentilo elasticsearch config files in order to send bulk data to script instead of Elasticsearch
```
elasticsearch.url = http://<script ip>:<script port>
```
at
`sentilo-agent-activity-monitor/src/main/resources/properties/monitor-config.properties`

5. Run Sentilo


Sentilo will now send data to the script as if it was Elasticsearch itself and Elasticsearch will receive it transformed.
