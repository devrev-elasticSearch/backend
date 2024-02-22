insightsIndexName = 'insights'

insightsMapping = {
    "properties":{
        "app_name":{"type":"keyword"},
        "start_date":{"type":"date","index":True},
        "end_date":{"type":"date","index":True},
        "version":{"type":"keyword"},
        "attributes":{"type":"object"},
    }
}