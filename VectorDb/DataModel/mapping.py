dataIndexName = "datamodel"

dataMapping = {
    "properties":{
        "app_name":{"type":"keyword","index":True},
        "id":{"type":"text"},
        "date": {"type": "date","index":True},
        "metadata":{ "type": "object" },
        "sub_info":{ "type": "object" },
        "main_text":{ "type": "text" },
        "attributes":{
            "properties":{
                "keywords":{"type":"keyword"},
                "first_order_labels":{"type":"keyword"},
                "second_order_labels":{"type":"keyword"},
                "sentiment":{"type":"keyword"},
                "priority":{"type":"keyword"},
                "pricing":{"type":"object"},
                "feature_requests":{"type":"object"},
                "positive_keywords":{"type":"keyword"},
                "second_order_label_to_keywordlist":{
                    "properties":{
                        "name":{"type":"keyword"},
                        "keywords":{"type":"keyword"}
                    }
                }
            }
        }
    }
}