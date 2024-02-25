## Description

This queue reads data from the queue where the snap ins publish data, filters them and forwards them to 
the rawDataQueueUrl

## .env setup

Create a .env with the following strings

1. snapInQueueUrl - Message queue Url where the snap in publishes the data from multiple sources
2. rawDataQueueUrl - Url where the filtered data is sent
3. googleApiKey - Apikey for google translate