from ticket_generation import *
from common_imports import *

if __name__ == "__main__":
    os.environ["OPENAI_API"]=getpass("Enter the OpenAI API Key: ")
    os.environ["OPENAI_ORG"]=getpass("Enter the OpenAI ORG Key: ")
    # Loading processed reviews
    with open('datas/phase1_result_GooglePay_v0.json', 'r') as f:
        phase1_result = json.load(f)

    phase1_result = phase1_result[-20:] # last 20 reviews
    # fixed_first_order_label = "Bug Reports" # "None"
    # if none then the function will generate tickets for all high priority issues
    # count_cutoff = 5 # minimum number of high priority reviews to generate a ticket under a label

    tickets = issue_ticket_based_on_high_prio_v2(phase1_result,count_cutoff=1,fixed_first_order_label="None")
    print("Tickets ..... ")
    print(tickets)

    # Store the tickets
    with open('./datas/tickets_GooglePay_v0.json', 'w') as json_file:
        json.dump(tickets, json_file, indent=4)
    