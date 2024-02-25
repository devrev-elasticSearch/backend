from .common_imports import *
from .semantic_union import *
from .taggers_and_routers import *
from .custom_langchain_tools import *
from .google_play_scrape_utils import *

from dotenv import load_dotenv

load_dotenv()

# This function is used to extract the app first order labels and their mapping to second order labels
def create_first_order_labels(user_defined_raw_clusters, generated_raw_clusters, num_threshold=1,score_threshold=0.90):
  groups = group_similar_strings(generated_raw_clusters,threshold=score_threshold)
  for u in user_defined_raw_clusters:
    groups.append([u])
  sec_order_to_first_order_labels = {}
  first_order_to_sec_order_labels = defaultdict(list)
  first_order_labels = []

  for g in groups:
    if len(g) < num_threshold:
      first_order_labels.extend(g)
      for _g in g:
        sec_order_to_first_order_labels[_g] = _g
    else:
      title = assign_title_to_groups(g)
      print(f"Grouped: {title}")
      first_order_labels.append(title)
      for _g in g:
        sec_order_to_first_order_labels[_g] = title

  for _ in sec_order_to_first_order_labels:
    first_order_to_sec_order_labels[sec_order_to_first_order_labels[_]].append(_)

  return first_order_labels, dict(first_order_to_sec_order_labels), sec_order_to_first_order_labels






# This function is used to standardize the app description
def standardize_app_description(api_result_app, summarized_app_description_list, first_order_to_sec_order_labels, second_order_label_to_multiqry):
    app_description_store = {}
    app_description_store['name'] = "{}".format(api_result_app['title'])
    app_description_store['price'] = "{}".format(api_result_app['price'])
    app_description_store['free'] = "{}".format(api_result_app['free'])
    app_description_store['currency'] = "{}".format(api_result_app['currency'])
    app_description_store['inAppProductPrice'] = "{}".format(api_result_app['inAppProductPrice'])
    app_description_store['minInstalls'] = "{}".format(api_result_app['minInstalls'])
    app_description_store['realInstalls'] = "{}".format(api_result_app['minInstalls'])
    app_description_store['score'] = "{}".format(api_result_app['score'])
    app_description_store['ratings'] = "{}".format(api_result_app['ratings'])
    app_description_store['description_list'] = summarized_app_description_list
    app_description_store['first_order_labels'] = [{"name":_,"second_order_labels":first_order_to_sec_order_labels[_]} for _ in first_order_to_sec_order_labels]
    app_description_store["generated_qrys_for_sec_labels"] = second_order_label_to_multiqry
    return app_description_store


# Running utility function for app description generation
def generate_full_app_descritpion(api_result_app, generic_raw_clusters, general_descripion ,multi_qry_count_per_label = 10):
    api_result_app_description = api_result_app['description']
    print("----------------------------------- App Description -----------------------------------")
    print(api_result_app_description)
    print("---------------------------------------------------------------------------------------")
    # Extracting the app description from the google play store
    summarized_app_description_text,summarized_app_description_list = convert_app_description_to_summary_list(api_result_app_description)
    print("----------------------------------- Summarized App Description -----------------------------------")
    print(summarized_app_description_text)
    print("---------------------------------------------------------------------------------------")

    generated_raw_clusters = ["Issues related to "+_ for _ in summarized_app_description_list]

    # First order labels and their mapping to second order labels
    first_order_labels,first_order_to_sec_order_labels,sec_order_to_first_order_labels = create_first_order_labels(
        generic_raw_clusters, 
        generated_raw_clusters, 
        num_threshold=2,
        score_threshold=0.86)
    
    print("-----------------------------------first_order_to_sec_order_labels -----------------------------------")
    print(first_order_to_sec_order_labels)
    print("---------------------------------------------------------------------------------------")

    # MultiQry for second order labels
    second_order_labels = list(sec_order_to_first_order_labels.keys())
    second_order_label_to_multiqry = {}
    # second_order_label_to_multiqry = gen_second_order_label_to_multiqry(second_order_labels, general_descripion = general_descripion, count_per_label = multi_qry_count_per_label)

    print("-----------------------------------second_order_label_to_multiqry -----------------------------------")
    print(second_order_label_to_multiqry)
    print("---------------------------------------------------------------------------------------")

    standard_app_description = standardize_app_description(api_result_app, summarized_app_description_list, first_order_to_sec_order_labels, second_order_label_to_multiqry)
    return standard_app_description

















# This function is used to standardize the phase 1 output
def statndardize_phase1_output(phase1_result,app_meta):
  standard_phase1_output = []
  for id,res in phase1_result.items():
    temp = {}
    temp["app_name"] = app_meta['name']
    temp["id"] = "{}".format(res['_id'])
    temp["date"] = res['date']
    temp["metadata"] = res['other_metadata_dict']
    temp["subinfo"] = {}
    temp["main_text"] = res['text-content']
    temp["attributes"] = {}
    temp["attributes"]["keywords"] = res['keywords']
    temp["attributes"]["first_order_labels"] = res['first_order_labels']['label_list']
    temp["attributes"]["second_order_labels"] = res['second_order_labels']['label_list']
    temp["attributes"]["sentiment"] = res['tagging_metadata']['sentiment']
    temp["attributes"]["priority"] = res['tagging_metadata']['priority']
    temp["attributes"]["pricing"] = res['pricing']
    temp["attributes"]["feature_requests"] = res['feature_requests']
    temp["attributes"]["positive_keywords"] = res['positive_keywords']
    __l_to_k = res['second_order_labels']['label_to_keylist']
    temp["attributes"]["second_order_label_to_keywordlist"] = [{"name":_,"keywords":__l_to_k[_]} for _ in __l_to_k]
    standard_phase1_output.append(temp)
  return standard_phase1_output


# Running Phase 1 pipeline
def run_phase1(vectors, app_meta,start_index=None,end_index=None,chunk_mode=False, p_flag=False, price_flag=False, featreq_flag=False):

  app_meta["first_order_to_sec_order_labels"] = {}
  for _ in app_meta["first_order_labels"]:
    app_meta["first_order_to_sec_order_labels"][_["name"]]=(_["second_order_labels"])

  second_order_label_to_multiqry = app_meta['generated_qrys_for_sec_labels']
  summarized_app_description_text = ' , '.join(app_meta['description_list'])
  first_order_to_sec_order_labels = app_meta['first_order_to_sec_order_labels']
  sec_order_to_first_order_labels = {value: key for key, values in first_order_to_sec_order_labels.items() for value in values}

  # Routing layer for second order labels
  rl = get_routelayer_for_second_order_layer(second_order_label_to_multiqry)
  tagging_chain = create_phase1_classif_tagger()

  phase1_result = {}
  phase1_cluster_labels_meta = {}
  start_index = 0 if start_index is None else start_index
  end_index = len(vectors) if end_index is None else end_index
  __total_len = len(vectors[start_index:end_index])
  for _vid,_vec in enumerate(list(vectors)[start_index:end_index]): 
    print(f"Processing {_vid+1}/{__total_len} ...")
    _vtext = vectors[_vid]["text"]
    # Extracting the phrases from the review text
    # _pos stores the positive phrases and _negs stores the negative phrases
    _pos ,_negs = key_word_extractor(summarized_app_description_text, _vtext,p_flag=p_flag,s_flag=not chunk_mode)
    phase1_result[_vid] = {'keywords':_negs}

    _1st_order_temp = set()
    _2nd_order_temp = set()
    _temp_dict_route_to_keys = defaultdict(list)

    for _n in _negs:
      _rout_label = rl(_n).name
      if _rout_label is None:
        _rout_label = 'other issues'
      _2nd_order_temp.add(_rout_label)
      if _rout_label != 'other issues':
        _1st_order_temp.add(sec_order_to_first_order_labels[_rout_label])
      _temp_dict_route_to_keys[_rout_label].append(_n)

    phase1_result[_vid]['first_order_labels'] = {"label_list":list(_1st_order_temp)}
    phase1_result[_vid]['second_order_labels'] = {"label_list":list(_2nd_order_temp),"label_to_keylist":dict(_temp_dict_route_to_keys)}
    phase1_result[_vid]['tagging_metadata'] = tagging_chain.invoke(_vtext)['text']
    phase1_result[_vid]['other_metadata_dict'] = vectors[_vid]['metadata']
    phase1_result[_vid]['positive_keywords'] = _pos
    phase1_result[_vid]['date']= vectors[_vid]['date']
    phase1_result[_vid]['text-content'] = vectors[_vid]['text']
    phase1_result[_vid]["_id"] = "[Processed]_"+_vec["title"]

    pricing_output = {
        "is_pricing":"No",
        "sentiment_of_current_pricing":"",
        "satisfaction_of_users":"",
        "worthiness_of_pricing":"",
        "suggestions_on_pricing":""
    }

    featreq_output = {
        "is_feature":"",
        "suggetions_on_features":[]
    }

    if price_flag:
      pricing_output = get_price_sentiment(_vtext)
    if featreq_flag:
      #TODO: Add feature request analysis
      pass
    phase1_result[_vid]['pricing'] = pricing_output
    phase1_result[_vid]['feature_requests'] = featreq_output

    for route in _temp_dict_route_to_keys:
      if route not in phase1_cluster_labels_meta:
        phase1_cluster_labels_meta[route]={'count':0,'keywords':[]}
      phase1_cluster_labels_meta[route]['count']+=1
      phase1_cluster_labels_meta[route]['keywords'].extend(_temp_dict_route_to_keys[route])

  phase1_result = statndardize_phase1_output(phase1_result,app_meta)
  return phase1_result,phase1_cluster_labels_meta

def get_app_model(app_id, app_name, generic_raw_clusters=['Bug Reports', 'Requesting for new features or limited feature', 'Issues related to Customer Support', ' Issues related to debit/credit cards compatibility','Issues related to Transaction failure','Issues related to Security and Privacy'], general_descripion="App Reviews for a payment and UPI app", multi_qry_count_per_label=10):
    loaded_api_result_app = fetch_app_description(app_id, app_name)
    standard_app_description = generate_full_app_descritpion(
        api_result_app = loaded_api_result_app,
        generic_raw_clusters=generic_raw_clusters,
        general_descripion=general_descripion,
        multi_qry_count_per_label=multi_qry_count_per_label
        )
    return standard_app_description