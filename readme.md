# Design of the Backend

## AI Backend readme : [readme.md/AI]

## Techonologies Used

1. Language - Python is used

2. Database Technologies - We use Elastic Search hosted on Elastic Cloud as our primry database for storing insights
. Elastic Search is used for very efficient searching and indexing. It is very easy to integrate vector search due to out of box support as well

3. Message Queue - AWS SQS ( Simple Queueing Service ) is used due to easy of setup and usage.

4. Backend Server - Python Flask is used to build the server to communicate with the dashboard.

## High level design of the system

<img src="https://drive.google.com/uc?export=view&id=1A7zpvz2b2LFfuncLiCL04gHRi8De-GLY" alt="High Level Design" width="90%" height="500">

Above we have shown the high level design of our system

### Data Sources
We have considered theree data sources
1. Twitter most recent tweets by list of hashtags
2. Reddit hot posts of a subreddit
3. Get new reviews from the app store given an app id


### Description of the Flow

#### Registration Flow

The client registers an app and provides the name and google play store id ( this is done for ease of implementation ). The description, pricing if relevant, other required metadata is fetched by the google play scraper and the first and second order clusters are dynamically generated on a per app basis.

#### Runtime Flow

From the three data source snap ins the data is published to a message queue, the data is fetched by using a cron job within the snap in within the snap in.

The denoiser function polls this queue, processes the messages, and publishes the data to a raw data queue,
The clustering function polls this queue, and clusters this data into multiple first and secord order labels which are extracted during the app registration page. The processed data is written to a database.

The Denoiser function translates the text into english using the Google Translate Api. Thena check is applied on the number of non ascii characters remaning as well as the number of spelling errors. Based on the the review is accepted or rejected

The ticket generation function periodically queries this database for high priority reviews, grouped by first order clusters. Multiple such rviews are then merged to create a ticket that is published on the ticket queue.

A snap in registered on the devrev platform, polls by queue when a command is invoked and creates the tickets on the devrev platform.

An alternative flow is the insights generated from feature requests on common organization hashtags on twitter. For example if a payment app is registered, these hashtags may relate to different payment or upi apps like Google/Apple/Amazon pay. These are general feature requests for the market segment not related to the registered app in particular. The feature requests are extracted within the snap in and tickets are created on the devrev platform. 
To display this data on the dashboard, the generated requests are parallely published to a message queue which is polled by the feature request extraction service.

### Building for scale

The entire architecture is completely decoupled with clearly defined services. The services communicated asynchronously with each other through message queues. Any part of the system can be independantly scaled. For example if the clustering function if very computationally heavy, multiple workers funning that function can be added as consumers to the queue. 

Moreover if any part of the system goes down, the data is persisted in queues, and processing can be resumed without any loss of data when the system comes back online.


## This backend consists of four main parts, as described in the runner.py file

### Denoiser Loop

This loop fetches raw data published to a sqs queue and filters it.
The filtering process involves translating to english, using criteria based on non english characters, spelling errors and number of words to filter the icoming data, the data is passed to another queue if it is not dropped

### DataModelCreator Loop

This loop fetches the filtered reviews from a queue from processes them to create data models. This loop
metches app metadata, which contains information about primary clustering labels for that application. Reviews are
clustered and the enriched data is written to the database

### TicketGenerator Loop

This loop periodically fetches high priority data from the database under a primary label, the reviews are then merged and a ticket is created which is published, this ticket can be fetched and created on the devrev plaform
using the ticket_creator_snap_in

### FeatureRequests Loop

This loop monitors for feature requests for a a group or organization specified by hashtags on the other_features_snap_in, for a payment application this would include hashtags for a multiple organizations in the upi and payment space like Google/Apple/Amazon Pay. where the associated command is called on the snap in, the tickets are created on the Devrev platform, the requests are also published to the queue which is listed for here.
This is done to integrate this functionality with our custom dashboard

## Running the app

```bash
pip3 install -r requirements.txt
python3 app.py
python3 run.py
```

app.py is the flask server for communication with the backend
run.py forks 4 processes for each of the four major parts of the backend and run the entire pipeline

### Information on specific subfolders and .env file setup can be found within the folders themselves
### Information on AI can be found in the AI folder
