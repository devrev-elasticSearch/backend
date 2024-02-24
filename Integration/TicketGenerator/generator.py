from AI import ticket_generation
from AWS import sqs
from VectorDb.DataModel import query as dataQuery

from dotenv import load_dotenv
import time

import os
load_dotenv()

ticketUrl = os.getenv("ticketQueue")

def generateTickets():
    while True:
        try:
            message = dataQuery.getRandomHighPriorityDataElementInLastDays(5000)
            firstOrderLabel = message[0]['attributes']['first_order_labels'][0]
            
            ticket = ticket_generation.issue_ticket_based_on_high_prio_v2(message, firstOrderLabel,1)
            sqs.publishToSqsQueue(ticketUrl, [[ticket[k] for k in ticket.keys()]])
            print("Ticket generated for first order label: ", ticket[firstOrderLabel])
            time.sleep(10)
        
        except Exception as e:
            print(e)
            time.sleep(5)