from ..Utils import api
from .mapping import insightsIndexName
from datetime import datetime

def getHitsFromResult(res):
    if(res["hits"]["total"] == 0):
        return []
    return res["hits"]["hits"]


def convertToTimestamp(elem):
    if(isinstance(elem, int)) or (isinstance(elem, float)):
        return elem
    element = datetime.strptime(elem, '%Y-%m-%d')
    return int(datetime.timestamp(element))

class QueryBuilder:
    def __init__(self, indexName=insightsIndexName):
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
    
    def addLessThanQuery(self, field, value):
        rangeQuery = {
            "range": {
                field: {
                    "lt": value
                }
            }
        }
        self.query["query"]["bool"]["must"].append(rangeQuery)
        return self
    
    def addGreaterThanQuery(self, field, value):
        rangeQuery = {
            "range": {
                field: {
                    "gt": value
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
    
    def buildQuery(self, query):
        for key in query:
            if key=="start_date":
                self.addGreaterThanQuery("end_date", query[key])

            if key=="end_date":
                self.addLessThanQuery("start_date", query[key])

            if key=="version":
                self.addTermQuery("version", query[key])
            
            if key=="app_name":
                self.addTermQuery("app_name", query[key])
        return
    
    def getCountsWithTimestamps(self,step_size_in_minutes,attributeName):
        res = api.client.search(index=self.indexName, body=self.query, ignore=400)
        res = getHitsFromResult(res)

        if(len(res) == 0):
            return [], []
        
        max_timestamp = max([convertToTimestamp(event["_source"]["end_date"]) for event in res])
        min_timestamp = min([convertToTimestamp(event["_source"]["start_date"]) for event in res])

        max_timestamp = int(max_timestamp - (max_timestamp % (step_size_in_minutes * 60)))
        min_timestamp = int(min_timestamp - (min_timestamp % (step_size_in_minutes * 60)))

        timestamps = []
        counts = []

        timeStamp2idx = dict()
        cnt=0

        for i in range(min_timestamp, max_timestamp, step_size_in_minutes * 60):
            timestamps.append(i)
            timeStamp2idx[i] = cnt
            cnt+=1
            counts.append(0)

        for event in res:
            #convert to timestamps first
            lower = int(convertToTimestamp(event["_source"]["start_date"]) - (convertToTimestamp(event["_source"]["start_date"]) % (step_size_in_minutes * 60)))
            upper = int(convertToTimestamp(event["_source"]["end_date"]) - (convertToTimestamp(event["_source"]["end_date"]) % (step_size_in_minutes * 60)))
            numSteps = int((upper - lower) / (step_size_in_minutes * 60))

            try:
                for i in range(lower, upper, step_size_in_minutes * 60):
                    counts[timeStamp2idx[i]] += event["_source"]["attributes"][attributeName] / numSteps

            except:
                continue

        return counts, timestamps
    
