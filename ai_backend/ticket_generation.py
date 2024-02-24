from common_imports import *
from semantic_union import *


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
def create_ticket(high_prio_review_list:list, common_second_order_label:str, urgent_frequency:int):
  # Now all keywords
  high_prio_keywords = []
  for _hp in high_prio_review_list:
    high_prio_keywords.extend(_hp['keywords'])
  combined_keywords = group_keywords_ticket(high_prio_keywords)
  
  ticket_llm = OpenAI(temperature=0.5, 
                      openai_api_key=os.getenv("OPENAI_API"),
                      openai_organization=os.getenv("OPENAI_ORG"),
                      )

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
  high_prio_review_text_combined = '\n'.join([_['other_metadata_dict']['content'] for _ in high_prio_review_list])
  ticket_body = ticket_llm_chain.invoke(high_prio_review_text_combined)['text']
  high_prio_review_ids_combined = [_['id'] for _ in high_prio_review_list]

  full_ticket = {
    "main":"Ticket",
    "body":ticket_body,
    "keywords":combined_keywords,
    "common_second_order_label":common_second_order_label,
    "urgent_frequency":urgent_frequency,
    "source review ids":high_prio_review_ids_combined
  }

  return full_ticket



# Dummy Function to create tickets based on high priority reviews
# Don't use this function
def issue_ticket_based_on_high_prio(phase1_result,count_cutoff=5):
  freq = defaultdict(list)
  for _ in phase1_result:
    pri = phase1_result[_]['tagging_metadata']['priority']
    if pri == 'High' or pri == 'Critical':
      k_list = list(phase1_result[_]['second_order_labels']['label_list'])
      for k in k_list:
        freq[k].append(phase1_result[_])
        freq[k][-1]['id'] = _
   
  freq = dict(freq)
  tickets = {}
  for issue in freq:
    if issue != 'other issues' and len(freq[issue])>count_cutoff:
      high_prio_review_list = freq[issue]
      common_second_order_label =  issue
      urgent_frequency = len(freq[issue])
      tickets[issue] = create_ticket(high_prio_review_list, common_second_order_label, urgent_frequency)

  return tickets