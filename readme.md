# Design of the Backend

## Techonologies Used

1. Language - Python is used

2. Database Technologies - We use Elastic Search hosted on Elastic Cloud as our primry database for storing insights
. Elastic Search is used for very efficient searching and indexing. It is very easy to integrate vector search due to out of box support as well

3. Message Queue - AWS SQS ( Simple Queueing Service ) is used due to easy of setup and usage.

4. Backend Server - Python Flask is used to build the server to communicate with the dashboard.

# High level design of the system


# This backend consists of four main parts, as described in the runner.py file

## Denoiser Loop

This loop fetches raw data published to a sqs queue and filters it.
The filtering process involves translating to english, using criteria based on non english characters, spelling errors and number of words to filter the icoming data, the data is passed to another queue if it is not dropped

## DataModelCreator Loop

This loop fetches the filtered reviews from a queue from processes them to create data models. This loop
metches app metadata, which contains information about primary clustering labels for that application. Reviews are
clustered and the enriched data is written to the database

## TicketGenerator Loop

This loop periodically fetches high priority data from the database under a primary label, the reviews are then merged and a ticket is created which is published, this ticket can be fetched and created on the devrev plaform
using the ticket_creator_snap_in

## FeatureRequests Loop

This loop monitors for feature requests for a a group or organization specified by hashtags on the other_features_snap_in, for a payment application this would include hashtags for a multiple organizations in the upi and payment space like Google/Apple/Amazon Pay. where the associated command is called on the snap in, the tickets are created on the Devrev platform, the requests are also published to the queue which is listed for here.
This is done to integrate this functionality with our custom dashboard

## Information on specific subfolders and .env file setup can be found within the folders themselves