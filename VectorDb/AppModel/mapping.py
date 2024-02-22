appIndexName = 'appindex'

appMapping = {
    "properties":{
        "name":{ "type":"text","index":True },
        "description":{ "type":"text" },
        "first_order_labels":{
            "type":"nested",
            "properties":{
                "name":{ "type":"text" },
                "second_order_labels":{"type":"object"}
            }
        }
    }
}