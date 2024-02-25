# AI Backend

Our AI-powered pipeline runs in two phases. When a new app is registered for the first time, the "App-Registration" pipeline works. The result for each app is stored in the database. Later, the "Routing-Based-Soft-Clustering" pipeline clusters (routes) the reviews (or the group of reviews) into various 2nd order issue labels through Semantic Routing.

## App-Registration Pipeline

<img src="https://drive.google.com/uc?export=view&id=1Tmr-QFIyJpvw12uqSTnuuQcYlwZilpxZ" alt="App Registration" width="600" height="500">

When the target app is registered, the related description of that app is fetched from the Play Store or similar by the function `fetch_app_description/google_play_scape_utils.py`. A custom [LangChain](www.langchain.com) agent `convert_app_description_to_summary_list/custom_langchain_tools.py` converts the app description into a list of Technical Features. These are concatenated with "Issue related to" along with some Custom User Issue Labels, forming the "2nd Order Issue Labels".

`create_first_order_labels/utils.py` converts these "2nd Order Issue Labels" which are then grouped into less numbered "1st Order Issue Labels". Here, our custom-built `group_similar_strings/semantic_union.py` (OpenAI's 'text-embedding-ada-002' embedding-based O(n) algorithm) and `assign_title_to_groups/semantic_union.py` (custom LangChain agent) help to group and name these "1st Order Issue Labels".

<img src="https://drive.google.com/uc?export=view&id=1fglg5Uy2d78XLZdBQh5xdhPD2cNLSIoo" alt="Multi Query generation" width="700" height="300">


`gen_second_order_label_to_multiqry/custom_langchain_tools.py` generates different Multi Queries for each "2nd Order Issue Labels". It helps the semantic router to build a robust semantic sense for each route or issue label.

"2nd Order Issue Labels", "1st Order Issue Labels", and the multi queries are stored in the database and these are used by the next pipeline.

## Routing-Based-Soft-Clustering Pipeline

<img src="https://drive.google.com/uc?export=view&id=1uMLg8ImAHGrmgaTF08M7XIfEcfUieIyc" alt="Routing" width="600" height="400">

We used ["Aurelio AI"](www.aurelio.ai)'s "Semantic Router" powered by [OpenAI](openai.com)'s 'text-embedding-ada-002' Embedding. This routing layer is a very fast and efficient way to route the input text to respective routes. In `get_routelayer_for_second_order_layer/taggers_and_routers.py`, we build these routes based on each "2nd Order Issue Labels" using the multi queries generated previously. If any input text does not fall into existing routes, it goes into the "None" route.

We create `create_phase1_classif_tagger/taggers_and_routers.py`, where the sentiment and priority are extracted from the review text using OpenAI-function call-based "Tagging" chain. `get_price_sentiment` and `get_feature_suggestions`, ["Tagging"](python.langchain.com/docs/use_cases/tagging) and ["Extraction"](python.langchain.com/docs/use_cases/extraction) chains, operate when "price_route" and "feature_suggestion" route is active. Note: these two routes are optional.

<img src="https://drive.google.com/uc?export=view&id=1ZbIRwpUSeYYC9SnZ3M-eKdRtQrVrtJ5r" alt="Example" width="700" height="550">

After coming through 'SpamFilter' and 'Translator', the reviews enter the AI pipeline. The reviews may be grouped together using `TikTokenUtil/chunker.py`. Then they pass through another LangChain agent present in `key_word_extractor/custom_langchain_tools.py`. It reads the full text and breaks them into separate lists consisting of "positive phrase list" and "negative phrase list". All elements in the "negative phrase list" are then routed through the existing routers. If any review contains multiple different negative aspects (e.g., issues regarding RuPay card, problems with UPI ID, etc.), it is routed to different routers at a time. Hence, each review is labeled with multiple "2nd Order Issue Labels", achieving the aspect of soft clustering.

The whole pipeline runs in `run_phase1/utils.py`.

### Models and Thresholds

- LLM used: gpt-3.5-turbo-0613
- Temperature: 0 and 0.1
- Embedding model: text-embedding-ada-002
- Number of multi-queries: 10
- Threshold for text-embedding-ada-002: 0.87

## Ticket Generation

`issue_ticket_based_on_high_prio_v2/ticket_generation.py` creates tickets from a list processed reviews. It filters the 'High' and 'Critical' priority reviews. Then, it groups the priority tickets for each "2nd Order Issue Label". It then summarizes each group and assigns a title using 'gpt-3.5-turbo-0613' (temp=0.3). It assigns tags based on the keywords in the group.

# Output
- Sample app description fetched from API: `datas/api_result_appdescr_PhonePe.json`  
- Sample output after App-Registration Pipeline: `datas/standard_app_description_PhonePe_v0.json`  
- Sample output after Routing-Based-Soft-Clustering Pipeline: `datas/phase1_result_PhonePe_v0_0_100.json`  
- Sample generated ticket: `datas/tickets_GooglePay_v0.json`

# Discussions
1. The abstract is to break down the whole review into multiple different phrases and then assign it to multiple categories, rather than digesting the whole text at once and assigning multiple categories. The two-step process helps in better performance.

2. Scalable:
    The clustering labels are AI-generated and can also consist of user-defined labels. So, we can have as many labels as needed.
    We can add as many routes and tagging chains as required.
    As we are not dependent on a single high temperature and large prompt, the chances of LLM hallucination are greatly mitigated. So, there is no need to change the prompts to handle different types of app categories.

3. SEO and AdInsight: We can use the positive phrases from the inputs to improve Search Engine Optimization and Ad-Insight.

