dataIndexName = "datamodel"

dataMapping = {
    "properties":{
        "id":{"type":"text"},
        "date": {"type": "date","index":True},
        "metadata":{ "type": "object" },
        "sub_info":{ "type": "object" },
        "main_text":{ "type": "text" },
        "attributes":{
            "properties":{
                "keywords":{"type":"text"},
                "first_order_label":{"type":"keyword"},
                "second_order_label":{"type":"keyword"},
                "sentiment":{"type":"keyword"},
                "priority":{"type":"keyword"},
            }
        }
    }
}