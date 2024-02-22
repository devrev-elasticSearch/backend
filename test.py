from AWS import sqs
from VectorDb.DataModel import mapping as dataMapping
from VectorDb.Utils import api
from VectorDb.DataModel import insert as dataInsert
from VectorDb.DataModel import query as dataQuery

from VectorDb.InsightsModel import mapping as insightsMapping
from VectorDb.InsightsModel import insert as insightsInsert
from VectorDb.InsightsModel import query as insightsQuery

if __name__ == "__main__":
    # sqs.loop(callback=insert.bulkInsert,maxMessages=1,timeInMinutes=1)
    # api.deleteAllRecords(rawDataIndexName)
    # api.deleteIndex(mapping.dataIndexName)
    # api.createIndex(mapping.dataIndexName)
    # api.createMapping(mapping.dataIndexName, mapping.dataMapping)
    # dummyData =[
    #     {
    #         "id":"1",
    #         "date":"2020-01-01",
    #         "metadata":{},
    #         "sub_info":{},
    #         "main_text":"This is a test",
    #         "vector_sparse_model":{
    #             "0":1
    #         },
    #         "attributes":{
    #             "keywords":"test",
    #             "first_order_label":"test",
    #             "second_order_label":"test",
    #             "sentiment":"test",
    #             "priority":"test"
    #         }
    #     },
    #     {
    #         "id":"2",
    #         "date":"2020-01-02",
    #         "metadata":{},
    #         "sub_info":{},
    #         "main_text":"This is a test",
    #         "vector_sparse_model":{
    #             "0":1
    #         },
    #         "attributes":{
    #             "keywords":"test",
    #             "first_order_label":"test",
    #             "second_order_label":"test",
    #             "sentiment":"test",
    #             "priority":"test"
    #         }
    #     }
    # ]
    # builder = query.QueryBuilder()
    # builder.buildQuery({
    #     "first_order_label":"test",
    #     "keywords":"test"
    # })

    # print(builder.execute())
    # api.deleteAllRecords(mapping.dataIndexName)
    # api.deleteIndex(mapping.dataIndexName)
    # api.createIndex(mapping.dataIndexName)
    # api.createMapping(mapping.dataIndexName, mapping.dataMapping)
    # insert.bulkInsert(dummyData)
    # api.createIndex(insightsMapping.insightsIndexName)
    # api.createMapping(insightsMapping.insightsIndexName, insightsMapping.insightsMapping)
    # dummyData = [
    #     {
    #         "app_name": "test",
    #         "version": "1.0",
    #         "start_date": '2020-01-01',
    #         "end_date": '2020-01-02',
    #         "attributes": {
    #             "bug_report": 10
    #         }
    #     },
    #     {
    #         "app_name": "test",
    #         "version": "1.0",
    #         "start_date": '2020-01-02',
    #         "end_date": '2020-01-03',
    #         "attributes": {
    #             "bug_report": 20
    #         }
    #     }
    # ]

    insightsInsert.bulkInsert(dummyData)
    builder = insightsQuery.QueryBuilder()
    builder.buildQuery({
        "app_name":"test",
        "version":"1.0",
        "start_date":"2020-01-01",
        "end_date":"2020-01-02"
    })

    # print(builder.getCountsWithTimestamps(60,"feature_request"))
    # api.deleteAllRecords(dataMapping.dataIndexName)
    # api.deleteIndex(dataMapping.dataIndexName)
    # api.createIndex(dataMapping.dataIndexName)
    # api.createMapping(dataMapping.dataIndexName, dataMapping.dataMapping)

