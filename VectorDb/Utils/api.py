from ..es import esclient
from elasticsearch import helpers
import json
import uuid
client = esclient.getClient()

def createIndex(indexName):
    res=client.indices.create(index=indexName)
    print(res)
    return res

def getRecord(indexName,id=id):
    return client.get(index=indexName, doc_type="_doc", id=id)

def getAllIndex():
    res=client.indices.get_alias("*")
    print(res)

def deleteAllIndex():
    indices=client.indices.get_alias().keys()
    for name in indices:
        print(f"Deleted {name}")
        client.indices.delete(index=name)

def deleteIndex(indexName):
    client.indices.delete(index=indexName)


def createMapping(indexName,params):
    res = client.indices.put_mapping(index = indexName,body=params)
    return res

def createSetting(indexName,params):
    res = client.indices.put_settings(index=indexName,body=params)

def closeIndex(indexName):
    res = client.indices.close(index=indexName)

def openIndex(indexName):
    res = client.indices.open(index=indexName)

def getMapping(indexName):
    res = client.indices.get_mapping(index = indexName)
    return res

def getAllRecords(indexName, size=1):
    dataQuery={
      "size":size,
        "query" : {
            "match_all" : {}
        }
    }
    res = client.search(index=indexName, body=dataQuery, ignore=400)
    return res

def deleteAllRecords(indexName):
  data={
        "query": {
            "match_all": {}
        }
    }
  res=client.delete_by_query(index=indexName,doc_type="_doc",body=data)
  return res

def insertRecord(indexName, record):
    if "id" in record:
        return client.index(index=indexName, doc_type="_doc", id = record["id"],body = record)
    else:
        return client.index(index=indexName, doc_type="_doc",body = record)

def updateRecord(indexName, id, record):
    return client.update(index = indexName, id=id, body={"doc": record})

#data is a json object
def bulkInsert(indexName, data, saveSize=50):

    actions = []

    #if id is not present, generate a hash for the id based on timestamp
    for record in data:
        if "id" in record:
            action = {
                "_index": indexName,
                "_id": record["id"],
                "_source": record
            }
        
        else:
            action = {
                "_index": indexName,
                "_source": record,
                "_id": str(uuid.uuid4())
            }
        actions.append(action)

    helpers.bulk(client, actions, chunk_size=saveSize)
    