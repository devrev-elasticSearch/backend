from flask import Flask, request, jsonify
from VectorDb.AppModel import query as appQuery
from VectorDb.DataModel import query as dataQuery
from VectorDb.FeatureModel import query as featureQuery
import json
from AI import utils
from VectorDb.AppModel import insert as appInsert
from flask_executor import Executor

def backGroundProcessAppModel(appData,description):
    appName = appData["name"]
    appData = utils.augment_multiqry_to_standard_app_description(appData,description)
    appInsert.updateByAppName(appName,appData)
    return

app = Flask(__name__)
executor = Executor(app)

def getBodyFromRequest(request):
    try:
        return request.get_json()
    except:
        return None
    

#{"app_name":"Google Pay"} return list of first order labels
@app.route('/api/app/firstorderlabels', methods=['POST'])
def firstorderlabel():
    body = getBodyFromRequest(request)

    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    if("app_name" not in body):
        return jsonify({"error": "Invalid request"}), 400
    appName = body["app_name"]
    print(appName)
    res = appQuery.queryByAppName(appName)

    res = res[0]
    res = [x['name'] for x in res["_source"]["first_order_labels"]]
    return jsonify(res)

#{"app_name":"Google Pay","first_order_label":"feature_request"} return list of second order labels
@app.route('/api/app/firstorderlabel/secondorderlabels', methods=['POST'])
def secondorderlabels():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    if("app_name" not in body):
        return jsonify({"error": "Invalid request"}), 400
    if("first_order_label" not in body):
        return jsonify({"error": "Invalid request"}), 400
    appName = body["app_name"]
    firstOrderLabel = body["first_order_label"]
    res = appQuery.queryByAppName(appName)

    res = [x["_source"]["first_order_labels"] for x in res]
    res = [x for x in res if x["name"] == firstOrderLabel]
    if(len(res) == 0):
        return jsonify([])
    return jsonify(res[0]["second_order_labels"])

#{'app_name':'Google Pay'} returns all processed data
@app.route('/api/app/datamodel/getall',methods=['POST'])
def getall():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    if("app_name" not in body):
        return jsonify({"error": "Invalid request"}), 400
    appName = body["app_name"]
    res = dataQuery.queryByAppName(appName)
    res = [x["_source"] for x in res]
    
    for data in res:
        temp = dict()
        
        for arr in data["attributes"]["second_order_label_to_keywordlist"]:
            temp[arr["name"]] = arr["keywords"]
        data['attributes']["second_order_labels"] = temp
    return jsonify(res)

@app.route('/api/app/appmodel/getdata',methods=['POST'])
def getappModel():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    if("app_name" not in body):
        return jsonify({"error": "Invalid request"}), 400
    appName = body["app_name"]
    appId = body["app_id"]
    
    if ("general_label_list" in body) and ("description" in body):
        res = utils.get_app_model(appId,appName,body["general_label_list"],body["description"])
    else:
        res= utils.get_app_model(appId,appName)
    return jsonify(res)

'''
Can add filters

filters are -
"app_name" string
"first_order_labels" list of strings
"second_order_labels" list of strings
"sentiment" positive or negative
"start_date" unix ts
"end_date" unix ts
priority - Low or High

all except app_name are optional

eg -
{
    "app_name":"Google Pay",
    "first_order_labels":["feature_request"],
    "sentiment":"positive",
    "start_date":1577836800,
    "end_date":1577923200
}
'''
@app.route('/api/app/datamodel/filter',methods=['POST'])
def filterDataModel():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    
    queryBuilder = dataQuery.QueryBuilder()
    queryBuilder.buildQuery(body)
    res = queryBuilder.execute()

    res = [x["_source"] for x in res]
    return jsonify(res)


@app.route('/api/app/appmodel/insert',methods=['POST'])
def insertAppModel():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    
    if "app_model" not in body:
        return jsonify({"error": "Invalid request"}), 400
    
    if(appQuery.isAppNamePresent(body["app_model"])):
        return jsonify({"error": "App already exists"}), 500
    
    if("description" not in body):
        return jsonify({"error": "Description not present"}), 500
    
    executor.submit(backGroundProcessAppModel,body["app_model"],body["description"])
    return jsonify({"success": "Data inserted"})


@app.route('/api/app/appmodel/appnames',methods=['GET'])
def getAppNames():
    res = appQuery.queryUniqueAppNames()
    res = [x["key"] for x in res]
    return jsonify(res)

@app.route('/api/app/features/getdata',methods=['POST'])
def getFeatureData():
    body = getBodyFromRequest(request)
    if(body == None):
        return jsonify({"error": "Invalid request"}), 400
    
    res = featureQuery.queryAll()
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=8000,debug=True)