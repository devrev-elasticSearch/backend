from Utils import api
from DataModel import mapping as dataMapping
from DataModel import query
from RawDataModel import mapping as rawDataMapping
from RawDataModel import insert as rawDataInsert
from AWS import sqs


if __name__ == "__main__":
    # api.deleteAllRecords(mapping.dataIndexName)
    # api.deleteIndex(mapping.dataIndexName)
    # api.createIndex(mapping.dataIndexName)
    # api.createMapping(mapping.dataIndexName,mapping.dataMapping)
    # print(api.getAllRecords(mapping.dataIndexName,size=2))
    # dims = 368

    # vector = []
    # for i in range(1, 369):
    #     vector.append(i)
    # api.insertRecord(mapping.dataIndexName, {
    #     "id":"1",
    #     "date": "2021-10-10",
    #     "other_metadata": {
    #         "source": "twitter",
    #         "user": "user1"
    #     },
    #     "sub_info": {
    #         "sub1": "info1",
    #         "sub2": "info2"
    #     },
    #     "main_text": "This is a test text",
    #     "vector_main_text": vector,
    #     "vector_sparse_model": {
    #         "1": 0.1,
    #         "2": 0.2,
    #         "0": 0.3,
    #     },
    #     "sentiment": "positive"
    # })
    # querySparse = {"30521": 0.3}
    # print(query.queryByKnnSparseVector(mapping.dataIndexName, querySparse, k=1))
    # api.createIndex(rawDataMapping.rawDataIndexName)
    # api.createMapping(rawDataMapping.rawDataIndexName, rawDataMapping.rawDataMapping)
    dataList = [
        {
            "date": "2021-10-10",
            "source": "twitter",
            "title": "user1",
            "text": "This is a test text"
        },
        {
            "date": "2021-10-10",
            "source": "twitter",
            "title": "user2",
            "text": "This is a test text"
        },
        {
            "date": "2021-10-10",
            "source": "twitter",
            "title": "user3",
            "text": "This is a test text"
        }
    ]
    # api.deleteIndex(rawDataMapping.rawDataIndexName)
    # rawDataInsert.bulkInsert(dataList)
    # print(api.getAllRecords(rawDataMapping.rawDataIndexName, size=3))
    # print("Index Created")
    sqs.loop(callback=rawDataInsert.bulkInsert)