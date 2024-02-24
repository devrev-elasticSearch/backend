from common_imports import *
from dotenv import load_dotenv

load_dotenv()

def get_routelayer_for_second_order_layer(second_order_label_to_multiqry):
  def create_routes_for_cluster_to_multiqry(cluster_to_multiqry):
    # Routes for different issues
    routes = []
    for c,qs in cluster_to_multiqry.items():
      route = Route(
          name=c,
          utterances=qs,
      )
      routes.append(route)
    return routes

  routes = create_routes_for_cluster_to_multiqry(second_order_label_to_multiqry)
  encoder = OpenAIEncoder(
        openai_api_key=os.getenv("OPENAI_API"),
        openai_org_id=os.getenv("OPENAI_ORG"),
    )
  rl = RouteLayer(encoder=encoder, routes=routes)
  return rl





def create_phase1_classif_tagger():
  phase1_order_tagging_schema = {
      "properties": {
          "sentiment": {
              "type": "string",
              "enum": ["positive", "neutral", "negative"],
              "description": "The sentiment expressed in the user review, categorized as positive, neutral, or negative. 'Positive' means high satisfaction, 'Neutral' indicates no strong sentiment, and 'Negative' signifies dissatisfaction , limite features, contains bad feedback or issues encountered.",
          },
          "priority": {
              "type": "string",
              "enum": ["Low", "Moderate", "High", "Critical"],
              "description": "The priority level assigned to the user review, indicating the seriousness of issues raised. 'Low' suggests minor issues, 'Moderate' implies noticeable issues, 'High' signifies significant issues, and 'Critical' indicates severe issues requiring immediate attention.",
          },
          "language": {
              "type": "string",
              "enum": ["english", "hindi", "others"],
              "description": "The language used in the user review.",
          },
      },
      "required": ["sentiment", "priority", "language"]
  }

  tagging_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API"),openai_organization=os.getenv("OPENAI_ORG"),temperature=0, model="gpt-3.5-turbo-0613")
  tagging_chain = create_tagging_chain(phase1_order_tagging_schema, tagging_llm)
  return tagging_chain






def get_price_sentiment(review_text):
  # keywords = review['keywords']
  text = review_text#['other_metadata_dict']['content']

  pricing_schema = {
    "properties": {
        "is_pricing": {
                "type": "string",
                "description": "Indicates whether the review contains pricing-related aspects such as in-app purchases, subscription-related prices, etc. 'Yes' signifies that the review includes sentiments related to pricing, while 'No' indicates that it does not contain such sentiments.",
                "enum": ['Yes', 'No']
        },
        "sentiment_of_current_pricing": {
            "type": "string",
            "description": "The overall sentiment or feeling associated with the current pricing strategy. This could include feedback from users, market analysis, or internal assessments. Possible values are 'Positive', 'Neutral', or 'Negative'." ,
            "enum": ['Positive', 'Neutral', 'Negative']
        },
        "worthiness_of_pricing": {
            "type": "string",
            "description": "An evaluation of the perceived value or worthiness of the current pricing model. This could include considerations such as features offered, competition pricing, and perceived fairness. Possible values are 'Overpriced', 'Not worthed', 'Value for money', or 'Cheap'.",
            "enum": ['Overpriced', 'Not worthed', 'Value for money', 'Cheap']
        }
    },
    "required": ["sentiment_of_current_pricing","worthiness_of_pricing"]
  }

  pricing_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API"),openai_organization=os.getenv("OPENAI_ORG"),temperature=0, model="gpt-3.5-turbo-0613")
  pricing_chain = create_tagging_chain(pricing_schema, pricing_llm)
  pricing_output = pricing_chain(text)['text']

  return pricing_output



def get_feature_suggestions(review_text):
  # keywords = review['keywords']
  text = review_text#['other_metadata_dict']['content']

  feature_schema = {
    "properties": {
        "is_feature_suggestion": {
                "type": "string",
                "description": "Indicates whether the review contains REQUESTS for new features or improvements to existing features. 'Yes' signifies that the review includes feature requests, while 'No' indicates that it does not contain such requests.",
                "enum": ['Yes', 'No']
        },
        "suggetions_on_features": {
            "type": "array",
            "description": "A list of suggestions or feedback on new features or improvements to existing features. This could include user requests, feedback from internal teams, or market analysis.",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["is_feature"]
  }

  feature_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API"),openai_organization=os.getenv("OPENAI_ORG"),temperature=0.3, model="gpt-3.5-turbo-0613")
  feature_chain = create_extraction_chain(feature_schema, feature_llm)
  feature_output = feature_chain(text)['text']

  return feature_output


# if __name__ == "__main__":
#   os.environ["OPENAI_API"]=getpass("Enter the OpenAI API Key: ")
#   os.environ["OPENAI_ORG"]=getpass("Enter the OpenAI ORG Key: ")
#   print(get_feature_suggestions("I would like to see a feature that allows me to pay for my bills using the app."))