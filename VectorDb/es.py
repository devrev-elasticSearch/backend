import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch,RequestsHttpConnection
from requests_aws4auth import AWS4Auth

load_dotenv()
awsAccessKey = os.getenv("awsAccessKey")
awsSecretKey = os.getenv("awsSecretKey")
regionName = os.getenv("regionName") 
domainName = os.getenv("domainName")

print(awsAccessKey,awsSecretKey,domainName)

# basicAuth = f"{awsAccessKey}:{awsSecretKey}"

def connectToEs():
    aws_auth = AWS4Auth(awsAccessKey, awsSecretKey, regionName, "es")
    es = Elasticsearch(timeout=12000, max_retries=10,
        hosts = [{'host': domainName, 'port': 443}],
        http_auth = ["elastic","CVFgK6lVvTknVd4U59PzzZrk"],
        use_ssl = True)
    # es = AsyncElasticsearch(timeout=120, max_retries=10,
    #     hosts = [{'host': domainName, 'port': 443}],
    #     http_auth = aws_auth,
    #     verify_certs = True,
    #     connection_class = RequestsHttpConnection)
    print("Es connected successfully")
    print(es.ping)
    return es, aws_auth

class ESclient:
    def __init__(self) -> None:
        self.client = None
        self.aws_auth_client = None
    
    def getClient(self):
        if self.client is None:
            self.client, self.aws_auth_client = connectToEs()
        return self.client
    
esclient = ESclient()