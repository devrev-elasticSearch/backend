# AI Backend
Our AI powered pipeline runs in two phases. When a new APP is registered for the first time , then the "App-Registration" pipeline works. The result for each app is stored in the database. Later, the "Routing-Based-Soft-Clustering" pipeline clusters(routes) the revews(or the gorup of reviews) into various 2nd order issue labels though Sematic Routing. 

## App-Registration Pipeline
[Add picutre]
When the target app is registed then related description of that app is feteched from the Playstore or similar by the function `fetch_app_description/google_play_scape_utils.py`. A custom LangChain agent `convert_app_description_to_summary_list/custom_langchain_tools.py` converts the App Description into list of Technical Features. These are concatentaed with "Issue realted to" along with some Custom User Issue Labels, form the "2nd Order Issue Labels". 

`create_first_order_labels/utils.py` converts these "2nd Order Issue Labels" are then grouped into less numbered "1st Order Issue Labels". Here our custom built `group_similar_strings/semantic_union.py`(OpenAI's 'text-embedding-ada-002' embedding based O(n) algorthm) and `assign_title_to_groups/semantic_union.py` (custom LangChain agent) help to group and name these "1st Order Issue Labels". 

[Add picutre]
`gen_second_order_label_to_multiqry/custom_langchain_tools.py` generates different Multi Queries for each "2nd Order Issue Labels". It helps the semaantic router to build a robust semnatic sense for each route or issue labels.

"2nd Order Issue Labels", "1st Order Issue Labels" and the multi queries are store in the database and these are be used by the next pipeline.

## Routing-Based-Soft-Clustering Pipeline
[Add picutre]
We used "Aurelio AI"'s "Semantic Router" powerd by OpenAI's 'text-embedding-ada-002' Embedding. This routing layer is very fast and effecient way to route the input text to respective routes. In `get_routelayer_for_second_order_layer/taggers_and_routers.py` we build these routes based on each "2nd Order Issue Labels" using the multi queries generated previously. If any input texts does not fall in existing routes into "None" route.

We create `create_phase1_classif_tagger/taggers_and_routers.py`, where the sentiment and priority are extracted from the review text using OpenAI-fucntion call based "Tagging" chain. `get_price_sentiment` and `get_feature_suggestions`, "Tagging" are "Extraction" chains, operates when "price_route" and "feature_suggestion" route is active. Note: these two routes are optional. 

[Add picutre]
After coming thorugh 'SpamFilter' and 'Translator', the reviews enters the AI pipeline. The reviews may be gouped together using `TikTokenUtil/chunker.py`. Then it passes another LangChain agent present in `key_word_extractor/custom_langchain_tools.py`. It reads the full text and breaks them two sperate lists consisting of "postive phrase list" and "negative phrase list". 
All elements in "negative phrase list" are then routed throuch the existing routers. If any review contains multiple different negative aspects (eg. issues regarding RuPay card, problem with UPI ID etc. ), it is routed different routers at a time. Hence, each review is labeled with multiple "2nd Order Issue Labels" achieving the aspect of soft clustering. 

The whole pipeline runs in `run_phase1/utils.py`.

# Models and Thresholds
LLm used = gpt-3.5-turbo-0613
Temperature = 0 and 0.1
Embedding model = text-embedding-ada-002

number of multqries = 10
threshold for text-embedding-ada-002 = 0.87


## Ticket Generation
`issue_ticket_based_on_high_prio_v2/ticket_generation.py` creates tickets from a list processed reviews. It filters the 'High' and 'Critical' priority reviews. Then, it groups the priority tickets
for each "2nd Order Issue Label". It then summarizes each group and assigns title using 'gpt-3.5-turbo-0613'(temp=0.3). It assigns tags based on the keywords in the group. 

# Discussions
The abstract is to break down the whole review into muliple different phrases and then assigning it to multple categories. Rather than, digesting the whole text at time and assigning multple categories. The two step proceess helps in better performance. 

1. Scalable : 
    The clustering labels are AI genearted and also can consist user defined. So, we can as many as labels.
    We can add as many as routes and tagging chains.
    As we are not depended on a single high temoperature and large prompt, the chances of LLM halucaination is vey much mitigated. So, no need to change the prompts to handle differnt types of app cateory. 
    SEO and AdIsight
2.  