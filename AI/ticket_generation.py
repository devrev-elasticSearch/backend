from .common_imports import *
from .semantic_union import *

from dotenv import load_dotenv

load_dotenv()

# Group similar keywords
# Uses the semantic similarity of the keywords to group them
def group_keywords_ticket(raw_keywords, num_threshold=2,score_threshold=0.90):
  groups = group_similar_strings(raw_keywords,threshold=score_threshold)
  combined_keywords = []
  for g in groups:
    if len(g) < num_threshold:
      combined_keywords.extend(g)
    else:
      combo = assign_title_to_groups(g)
      combined_keywords.append(combo)
  return combined_keywords


# Call this function to create a ticket based on high priority reviews
# It takes a list of high priority reviews (Of type of review frame), a common second order label(String) and the frequency of the urgent issues(Int)
def group_keywords_ticket(raw_keywords, num_threshold=2,score_threshold=0.90):
  groups = group_similar_strings(raw_keywords,threshold=score_threshold)
  combined_keywords = []
  for g in groups:
    if len(g) < num_threshold:
      combined_keywords.extend(g)
    else:
      combo = assign_title_to_groups(g)
      combined_keywords.append(combo)
  return combined_keywords




# Call this function to create a ticket based on high priority reviews
# It takes a list of high priority reviews (Of type of review frame), a common second order label(String) and the frequency of the urgent issues(Int)
# Uses gpt-3.5-turbo-0613 Temparature 0.5 to summarize the reviews and assign a title to the ticket
# Uses LangChain Agent
def create_ticket(high_prio_review_list:list, common_label:str, urgent_frequency:int):
  # Now all keywords
  high_prio_keywords = []
  for _hp in high_prio_review_list:
    high_prio_keywords.extend(_hp["attributes"]['keywords'])
  combined_keywords = group_keywords_ticket(high_prio_keywords)

  ticket_llm = OpenAI(temperature=0.5, 
                      openai_api_key=os.getenv("OPENAI_API"),
                      openai_organization=os.getenv("OPENAI_ORG"),)

  ticket_template = """
    GIven some high priorty user reviews of an app :
    {reviews}

    You are an AI tool to summarize these reviews to create a ticket body.
    The ticket body should be brief and cover all points in the given user reviews. Word limt less than 150 words.
    The ticket body should only contain technical words.

    Answer: < ticket body >
    """

  ticket_prompt = PromptTemplate(input_variables=['reviews'], template=ticket_template)
  ticket_llm_chain = LLMChain(prompt= ticket_prompt, llm=ticket_llm, verbose=False)
  high_prio_review_text_combined = '\n'.join([_['main_text'] for _ in high_prio_review_list])
  ticket_body = ticket_llm_chain.invoke(high_prio_review_text_combined)['text']
  high_prio_review_ids_combined = [_['id'] for _ in high_prio_review_list]

  ticket_title_prompt = f"""
      Given a short summary high priorty user reviews of an app :
      {ticket_body}
      
      Assign a brief title to this ticket to this summary. The title should be within 5 - 6 words . It should be very technical.
      Ticket title: <Ticket Title>
      Invoke a relevant tool when you need to store <Ticket Title>.
      """
  
  full_ticket = {
    "title": assign_title_to_groups(None,ticket_title_prompt),
    "description":ticket_body,
    "date":"{}".format(dt.now()),
    "tags":combined_keywords,
    "metadata":{
        "common_label":common_label,
        "source review ids":high_prio_review_ids_combined
        },
    "priority":urgent_frequency,
  }

  return full_ticket



# Issue ticket based on high priority reviews
# This function takes a list of reviews and returns a ticket for each high priority issue under each first order label
# The function also takes a fixed first order label to issue the ticket under
# If the fixed first order label is not present in the high priority reviews, it returns a dummy ticket
# The function also takes a count cutoff to issue a ticket for a high priority issue
def issue_ticket_based_on_high_prio_v2(standad_phase1_result,fixed_first_order_label="None",count_cutoff=5):
  freq = defaultdict(list)
  for _,_res in enumerate(standad_phase1_result):
    pri = standad_phase1_result[_]['attributes']['priority']
    if pri == 'High' or pri == 'Critical':
      k_list = list(standad_phase1_result[_]['attributes']['first_order_labels'])
      for k in k_list:
        freq[k].append(standad_phase1_result[_])
        freq[k][-1]['id'] = standad_phase1_result[_]['id']
  
  freq = dict(freq)
  # print(freq)
  for fff in freq:
    print(fff,len(freq[fff]))

  dummy_ticket = {
      "title": "",
      "description":"",
      "date":"",
      "tags":[],
      "metadata":{
          "common_label":"",
          "source review ids":[]
          },
      "priority":"",
    }

  if fixed_first_order_label != "None":
    issue = fixed_first_order_label
    if issue not in freq:
      print("Warning: No high priority reviews for the given issue")
      return dummy_ticket
    high_prio_review_list = freq[issue]
    common_first_order_label =  issue
    urgent_frequency = len(freq[issue])
    ticket = create_ticket(high_prio_review_list, common_first_order_label, urgent_frequency)
    print(ticket)
    if ('title' not in ticket.keys()) or (ticket['title']=="Ticket Title"):
      ticket['title'] = common_first_order_label
    return {
        fixed_first_order_label:ticket
        }

  tickets = {}
  # print(freq)
  for issue in freq:
    if issue != 'other issues' and len(freq[issue])>=count_cutoff:
      high_prio_review_list = freq[issue]
      common_first_order_label =  issue
      urgent_frequency = len(freq[issue])
      tickets[issue] = create_ticket(high_prio_review_list, common_first_order_label, urgent_frequency)
      if (tickets[issue]['title']=="Ticket Title"):
        tickets[issue]['title'] = common_first_order_label

  return tickets