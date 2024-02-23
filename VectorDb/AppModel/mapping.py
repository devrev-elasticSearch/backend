appIndexName = 'appindex'

appMapping = {
    "properties":{
        "name":{ "type":"keyword","index":True },
        "description":{ "type":"text" },
        "first_order_labels":{
            "type":"nested",
            "properties":{
                "name":{ "type":"keyword" },
                "second_order_labels":{"type":"keyword"}
            }
        }
    }
}