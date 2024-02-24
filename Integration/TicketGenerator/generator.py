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
            message = dataQuery.getRandomHighPriorityDataElementInLastDays(days=5000)
            firstOrderLabel = message[0]['attributes']['first_order_labels'][0]
            
            ticket = ticket_generation.issue_ticket_based_on_high_prio_v2(message, "None",1)
            
            for t in ticket.keys():
                if ticket[t]['title'] is None:
                    ticket[t]['title'] = t
            
            for k in ticket.keys():
                sqs.publishToSqsQueue(ticketUrl, [ticket[k]])
            print("Ticket generated for first order label: ", ticket)
            time.sleep(5)
        
        except Exception as e:
            # print(e)
            time.sleep(1)