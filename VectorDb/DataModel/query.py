from .mapping import dataIndexName, dataMapping
from ..Utils import api

def getHitsFromResult(res):
    if(res['hits']["total"] == 0):
        return []
    
    return res["hits"]["hits"]

def queryInDateRange(start, end, indexName=dataIndexName):
    dataQuery={
        "query": {
            "range": {
                "date": {
                    "gte": start,
                    "lte": end
                }
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)

def queryByAppName(appName, indexName=dataIndexName):
    dataQuery={
        "query": {
            "term": {
                "app_name": appName
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)

def queryByIdList(indexName, idList):
    dataQuery={
        "query": {
            "ids": {
                "values": idList
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)


def queryByKnnSparseVector(vector, k=1, indexName=dataIndexName):
    #define script for cosine similarity
    script = {
        "source": "cosineSimilaritySparse(params.query_vector, doc['vector_sparse_model']) + 1.0",
        "params": {
            "query_vector": vector
        }
    }

    #define query
    dataQuery={
        "size": k,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": script
            }
        }
    }

    #execute query
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)

def queryByFirstOrderLabel(indexName, firstOrderLabel):
    dataQuery={
        "query": {
            "term": {
                "attributes.first_order_label": firstOrderLabel
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)

def queryBySentiment(indexName, sentiment):
    dataQuery={
        "query": {
            "term": {
                "attributes.sentiment": sentiment
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)

def queryByPriority(priority, indexName=dataIndexName):
    dataQuery={
        "query": {
            "term": {
                "attributes.priority": priority
            }
        }
    }
    res = api.client.search(index=indexName, body=dataQuery, ignore=400)
    return getHitsFromResult(res)



class QueryBuilder:
    def __init__(self, indexName=dataIndexName):
        self.indexName = indexName
        self.query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

    def addRangeQuery(self, field, start, end):
        rangeQuery = {
            "range": {
                field: {
                    "gte": start,
                    "lte": end
                }
            }
        }
        self.query["query"]["bool"]["must"].append(rangeQuery)
        return self

    def addTermQuery(self, field, value):
        termQuery = {
            "term": {
                field: value
            }
        }
        self.query["query"]["bool"]["must"].append(termQuery)
        return self
    
    def addKeywordMatch(self, field, keyWordList):

        if(type(keyWordList) != list):
            keywordMatch = {
                "match": {
                    field: keyWordList
                }
            }
            self.query["query"]["bool"]["must"].append(keywordMatch)
        
        else:
            for keyword in keyWordList:
                keywordMatch = {
                    "match": {
                        field: keyword
                    }
                }
                self.query["query"]["bool"]["must"].append(keywordMatch)
        return self

    
    def buildQuery(self,values):
        if "start_date" in values and "end_date" in values:
            self.addRangeQuery("date", values["start_date"], values["end_date"])

        if "first_order_labels" in values:
            self.addKeywordMatch("attributes.first_order_labels", values["first_order_labels"])

        if "sentiment" in values:
            self.addTermQuery("attributes.sentiment", values["sentiment"])
        
        if "priority" in values:
            self.addTermQuery("attributes.priority", values["priority"])
        
        if "second_order_labels" in values:
            self.addKeywordMatch("attributes.second_order_labels", values["second_order_labels"])

        if "keywords" in values:
            self.addKeywordMatch("attributes.keywords", values["keywords"])

        if "app_name" in values:
            self.addTermQuery("app_name", values["app_name"])

    def execute(self):
        res = api.client.search(index=self.indexName, body=self.query, ignore=400)
        return getHitsFromResult(res)
    

    def executeWithKnn(self,vector,k=1):
        res = api.client.search(index=self.indexName, body=self.query, ignore=400)
        idList = [hit["_id"] for hit in getHitsFromResult(res)]

        if len(idList) == 0:
            return []
        
        script = {
            "source": "cosineSimilaritySparse(params.query_vector, doc['vector_sparse_model']) + 1.0",
            "params": {
                "query_vector": vector
            }
        }

        dataQuery={
            "size": k,
            "query": {
                "script_score": {
                    "query": {
                        "ids": {
                            "values": idList
                        }
                    },
                    "script": script
                }
            }
        }

        res = api.client.search(index=self.indexName, body=dataQuery, ignore=400)
        return getHitsFromResult(res)

