insightsIndexName = 'insights'

insightsMapping = {
    "properties":{
        "app_name":{"type":"keyword"},
        "start_date":{"type":"date","index":True},
        "end_date":{"type":"date","index":True},
        "version":{"type":"keyword"},
        "attributes":{
            "properties":{
                "bug_report":{"type":"integer"},
                "feedback":{"type":"integer"},
                "positive_sentiment":{"type":"integer"},
                "neutral_sentiment":{"type":"integer"},
                "negative_sentiment":{"type":"integer"},
            }
        }
    }
}