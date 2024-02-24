from common_imports import *
from semantic_union import *
from utils import *
from custom_langchain_tools import *
from taggers_and_routers import *


if __name__ == "__main__":
    os.environ["OPENAI_API"]=getpass("Enter the OpenAI API Key: ")
    os.environ["OPENAI_ORG"]=getpass("Enter the OpenAI ORG Key: ")
    # this is the raw review data
    all_reviews_file_path = './datas/api_result_reviews_relv_GooglePay_v0.json'
    with open(all_reviews_file_path, "r") as json_file:
        all_reviews = json.load(json_file)

    # this is the processed app data from the appmeta_path by AI
    appmeta_path = './datas/standard_app_description_GooglePay_v0.json'
    with open(appmeta_path, "r") as json_file:
        app_meta = json.load(json_file)


    # Run the phase 1 model
    start_index=None # 0
    end_index=20 # Number of reviews (But testing e 10 dbo)
    chunk_mode=False # Is the data chunked
    p_flag=False # Are we processing the postive reviews
    price_flag=False # Are we processing the price
    featreq_flag=False # Are we processing the feature requests
    
    phase1_result,phase1_cluster_labels_meta = run_phase1(
        all_reviews,
        app_meta,
        start_index=start_index,
        end_index=end_index,
        chunk_mode=chunk_mode, 
        p_flag=p_flag, 
        price_flag=price_flag, 
        featreq_flag=featreq_flag
        )

    # Store the phase 1 result (Processes data model)
    with open('./datas/phase1_result_GooglePay_v0.json', 'w') as json_file:
        json.dump(phase1_result, json_file, indent=4)

