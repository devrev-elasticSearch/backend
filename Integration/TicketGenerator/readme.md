## Description

This folder details function for generating tickets. Tickets are generated and published to a message queue,
from where they are fetched by the snap in

## .env setup

Create a .env file with the following strings
 1. ticketQueue - Url for the message queue where tickets are published