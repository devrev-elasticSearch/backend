from AWS import sqs
from VectorDb.DataModel import mapping as dataMapping
from VectorDb.Utils import api
from VectorDb.DataModel import insert as dataInsert
from VectorDb.DataModel import query as dataQuery

from VectorDb.InsightsModel import mapping as insightsMapping
from VectorDb.InsightsModel import insert as insightsInsert
from VectorDb.InsightsModel import query as insightsQuery

from VectorDb.AppModel import mapping as appMapping
from VectorDb.AppModel import insert as appInsert
from VectorDb.AppModel import query as appQuery

from Integration.DataModelCreator import loop
from Integration.TicketGenerator import generator
from datetime import datetime
from AI import ticket_generation
from AI import utils
import json

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

    # insightsInsert.bulkInsert(dummyData)
    # builder = insightsQuery.QueryBuilder()
    # builder.buildQuery({
    #     "app_name":"test",
    #     "version":"1.0",
    #     "start_date":"2020-01-01",
    #     "end_date":"2020-01-02"
    # })
    # loop.loop()
    # api.createIndex(appMapping.appIndexName)
    # api.createMapping(appMapping.appIndexName, appMapping.appMapping)

    # print(builder.getCountsWithTimestamps(60,"feature_request"))
    # api.deleteAllRecords(dataMapping.dataIndexName)
    # api.deleteIndex(dataMapping.dataIndexName)
    # api.createIndex(dataMapping.dataIndexName)
    # api.createMapping(dataMapping.dataIndexName, dataMapping.dataMapping)
    # dummyData = []

    # with open('dummy_app.json') as json_file:
    #     dummyData = json.load(json_file)
    
    # appInsert.insertAppData(dummyData)
    # dummyData = []
    # with open('sample.json') as json_file:
    #     dummyData = json.load(json_file)

    # d = []

    # for key in dummyData.keys():
    #     data=dummyData[key]
    #     temp=dict()
    #     unixTimestamp = int(datetime.timestamp(datetime.strptime(data['other_metadata_dict']["at"],"%Y-%m-%d %H:%M:%S")))

    #     lis = []

    #     if 'label_to_keylist' in data['second_order_labels'].keys():
    #         for key in data['second_order_labels']['label_to_keylist'].keys():
    #             temp1 = dict()
    #             temp1['name'] = key
    #             temp1['keywords'] = data['second_order_labels']['label_to_keylist'][key]
    #             lis.append(temp1)

    #     temp["app_name"]="Google Pay"
    #     temp["date"]=unixTimestamp
    #     temp["main_text"]=data['other_metadata_dict']['content']
    #     temp["attributes"]={
    #         "keywords":data["keywords"],
    #         "first_order_labels":data["first_order_labels"]["label_list"],
    #         "second_order_labels":data["second_order_labels"]["label_list"],
    #         "sentiment":data["tagging_metadata"]["sentiment"],
    #         "priority":data["tagging_metadata"]["priority"],
    #         "second_order_label_to_keywordlist":lis
    #     }
    #     temp["metadata"]=data["other_metadata_dict"]

    #     d.append(temp)

    # with open('dummy_datamodel.json', 'w') as outfile:
    #     json.dump(d, outfile)
    # dummyData = []    
    # with open('phase1_result_GooglePay_v0_0_500.json') as json_file:
    #     dummyData = json.load(json_file)
    
    # for d in dummyData:
    #     d['app_name'] = "Google Pay"
    #     d['date'] = int(datetime.timestamp(datetime.strptime(d['date'],"%Y-%m-%d %H:%M:%S")))
    # dataInsert.bulkInsert(dummyData)
    # print(api.getAllRecords(dataMapping.dataIndexName))
    # api.deleteIndex(appMapping.appIndexName)
    # api.createIndex(appMapping.appIndexName)
    # api.createMapping(appMapping.appIndexName, appMapping.appMapping)
    # api.deleteAllRecords(dataMapping.dataIndexName)
    # api.deleteAllRecords(appMapping.appIndexName)
    # api.deleteIndex(appMapping.appIndexName)
    # loop.loop()
    # print(dataQuery.queryForDataByFirstOrderLabelInPrevDays(dataQuery.queryMaxFirstOrderLabel(1000)))
    # loop.loop()
    # print(api.getAllRecords(dataMapping.dataIndexName) )
    # firstOrderLabel = appQuery.queryRandomFirstOrderLabel()
    # print(dataQuery.getRandomHighPriorityDataElementInLastDays(50000))
    print(utils.get_app_model("com.google.android.apps.nbu.paisa.user","Google Pay"))
    # generator.generateTickets()
    #print(ticket_generation.issue_ticket_based_on_high_prio_v2(dataQuery.queryForDataByFirstOrderLabelInPrevDays(dataQuery.queryMaxFirstOrderLabel(1000)),dataQuery.queryMaxFirstOrderLabel(1000),1))
    print("hello")

