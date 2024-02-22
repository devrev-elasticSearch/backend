rawDataIndexName = 'rawdataindex'

rawDataMapping = {
    "properties":{
        "id":{"type":"text"},
        "date": {"type": "date","index":True},
        "source":{"type":"keyword"},
        "metadata":{ "type": "object" },
        "text":{ "type": "text" },
        "title":{ "type": "text" },
    }
}