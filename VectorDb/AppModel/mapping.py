appIndexName = 'appindex'

appMapping = {
    "properties":{
        "name":{ "type":"keyword","index":True },
        "description_list":{ "type":"text" },
        "first_order_labels":{
            "type":"nested",
            "properties":{
                "name":{ "type":"keyword" },
                "second_order_labels":{"type":"keyword"}
            }
        },P
        "price":{ "type":"keyword" },
        "free":{"type":"keyword"},
        "currency":{"type":"keyword"},
        "inAppProductPrice":{"type":"keyword"},
        "minInstalls":{"type":"keyword"},
        "realInstalls":{"type":"keyword"},
        "score":{"type":"keyword"},
        "ratings":{"type":"keyword"},
        "generated_qrys_for_sec_labels":{"type":"object"}
    }
}