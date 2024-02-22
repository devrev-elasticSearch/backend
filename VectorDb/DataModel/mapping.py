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
                "keywords":{"type":"text"},
                "first_order_labels":{"type":"keyword"},
                "second_order_labels":{"type":"keyword"},
                "sentiment":{"type":"keyword"},
                "priority":{"type":"keyword"},
            }
        }
    }
}