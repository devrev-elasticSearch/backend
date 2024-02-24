from common_imports import *
from semantic_union import *

from dotenv import load_dotenv

load_dotenv()



# This function is used to extract the app description from the google play store
# The function returns the app description

def convert_app_description_to_summary_list(api_result_app_description):
  summarized_app_description_list = [None]
  class FeatureAppenderToolCheckInput(BaseModel):
      features: List[str] = Field(..., description="A list that describes multple features.")

  class FeatureAppenderTool(BaseTool):
      name = "FeatureAppenderTool"
      description = (
        "use this tool when you need to store app features"
        "given a list that describes multple features. Each element in this list is a string that describes a single feature"
      )

      def _run(self,features:List[str]):
          print("FeatureAppenderTool invoked ... Storing features ... ")
          summarized_app_description_list[0] = features
          return features

      def _arun(self,features: List[str]):
          raise NotImplementedError("This tool does not support async")

      args_schema: Optional[Type[BaseModel]] = FeatureAppenderToolCheckInput

  tools = [FeatureAppenderTool()]

#   print(f"2 >> {os.getenv('OPENAI_API')}")
#   print(f"3 >> {os.getenv('OPENAI_ORG')}")

  llm = ChatOpenAI(
      openai_api_key=os.getenv("OPENAI_API"),
      openai_organization=os.getenv("OPENAI_ORG"),
      temperature=0, model="gpt-3.5-turbo-0613")
  
  agent = initialize_agent(
      agent=AgentType.OPENAI_FUNCTIONS,
      tools=tools,
      llm=llm,
      verbose=False,
  )

  input_template = f"""App description: {api_result_app_description}

  Now, summarize all of the app features in less than 150 words:
  Answer: Let's write point by point.
  Invoke a relevant tool when you need to store these app features.
  """

  summarized_app_description_text = agent(input_template)['output']
  return summarized_app_description_text, summarized_app_description_list[0]



# This function is used to extract the key words from the summarized app description and the user reviews
# The function returns the positive and negative key words
# The function also stores the key words in the respective lists

def key_word_extractor(summarized_app_description_text, review, p_flag = True, n_flag = True, s_flag = False):
  postive_points = []
  negative_points = []
  class PostiveAppenderToolCheckInput(BaseModel):
      phrases: List[str] = Field(..., description="A list of string that describes multple positive aspects")

  class PostiveAppenderTool(BaseTool):
      name = "PositiveAspectHandlerTool"
      description = desc = (
        "use this tool when you need to store postive aspects of user reviews after analyzing"
        "given a list of keywords/phrases which covers positive aspects"
      )

      def _run(self,phrases:List[str]):
          print("PostiveAppenderTool invoked ... Storing positive reviews ...")
          postive_points.extend(phrases)
          return phrases

      def _arun(self,phrases: List[str]):
          raise NotImplementedError("This tool does not support async")

      args_schema: Optional[Type[BaseModel]] = PostiveAppenderToolCheckInput

  class NegativeAppenderToolCheckInput(BaseModel):
      phrases: List[str] = Field(..., description="A list of string that describes multple negative aspects")

  class NegativeAppenderTool(BaseTool):
      name = "NegativeAspectHandlerTool"
      description = desc = (
        "use this tool when you need to store negative aspects of user reviews after analyzing"
        "given a list of keywords/phrases which covers negative aspects"
      )

      def _run(self,phrases:List[str]):
          print("NegativeAppenderTool invoked ... Storing negative reviews ... ")
          negative_points.extend(phrases)
          return phrases

      def _arun(self,phrases: List[str]):
          raise NotImplementedError("This tool does not support async")

      args_schema: Optional[Type[BaseModel]] = NegativeAppenderToolCheckInput


  tools = []
  if p_flag :
    tools.append(PostiveAppenderTool())
  if n_flag :
    tools.append(NegativeAppenderTool())

  llm = ChatOpenAI(
      openai_api_key=os.getenv("OPENAI_API"),
      openai_organization=os.getenv("OPENAI_ORG"),
      temperature=0, model="gpt-3.5-turbo-0613")
  # initialize agent with tools
  agent = initialize_agent(
      agent=AgentType.OPENAI_FUNCTIONS,
      tools=tools,
      llm=llm,
      verbose=False,
  )

  input_template = f"""Given an App Description:
  {summarized_app_description_text}
  
  Reviews given by the few users :
  {review}

  You are an AI tool. Your task is to extract brief keywords or phrases that best describe the given user reviews relevant to the app description.
  Such keywords or phrases cover main {"positive" if p_flag else ""} {"and" if p_flag and n_flag else ""} {"negative" if n_flag else ""} aspects.
  Each single keywords or phrases briefly describes the respective issue.

  {f'Top {"1 or 2" if s_flag else "3"} Keywords or Phrases for positive aspects: <Write here point by point>  You need to store these positive aspects into a list. You must use specific tool to do this.' if p_flag else ""}

  {f'Top {"1 or 2" if s_flag else "3"} Keywords or Phrases for negative aspects: <Write here point by point> You need to store these negative aspects into a list. You must use specific tool to do this.' if n_flag else ""}
  """

  agent(input_template)['output']


  return postive_points, negative_points





# This function is used to generate multiple queries to generate multiple negative aspects of an app from multiple perspectives
# The function returns the generated reviews
# The function also stores the generated reviews in the respective list
def gen_multiqry(qry_text,higher_level_description,number=6):
  generated_review_list = []
  class ReviewAppenderToolCheckInput(BaseModel):
    reviews: List[str] = Field(..., description="A list that describes multple generated phrases.")

  class ReviewAppenderTool(BaseTool):
      name = "ReviewAppenderTool"
      description = (
        "use this tool when you need to store generated phrases"
        "given a list that describes multple generated reviews. Each element in this list is a string that describes a single generated phrase"
      )

      def _run(self,reviews:List[str]):
          print(reviews)
          print("ReviewAppenderTool invoked ... Storing generated phrases ... ")
          generated_review_list.extend(reviews)
          return reviews

      def _arun(self,reviews: List[str]):
          raise NotImplementedError("This tool does not support async")

      args_schema: Optional[Type[BaseModel]] = ReviewAppenderToolCheckInput


  tools = [ReviewAppenderTool()]

  llm = ChatOpenAI(
      openai_api_key=os.getenv("OPENAI_API"),
      openai_organization=os.getenv("OPENAI_ORG"),
      temperature=0, model="gpt-3.5-turbo-0613")

  # initialize agent with tools
  agent = initialize_agent(
      agent=AgentType.OPENAI_FUNCTIONS,
      tools=tools,
      llm=llm,
      verbose=False,
  )

  input_template = f"""
  Your task is to generate {number} different phrases that aim to
  describe different NEGATIVE aspects of an app from multiple perspectives. The aspects
  are focused on {higher_level_description}.
  Each phrase MUST tackle the angle from a different negative viewpoint, we
  want to get a variety of RELEVANT negative user feedback.

  Each phrase has to be within 20 words briefly describing the respective aspect.

  Provide these alternative phrases separated by newlines.
  You have to generate diffent negative aspects based on : {qry_text}
  Invoke a relevant tool when you need to store these generated phrases.
  """

  agent(input_template)['output']
  return generated_review_list





# This function is used to generate multiple queries to generate multiple negative aspects of an app from multiple perspectives
# The function returns the generated reviews for each cluster
def gen_second_order_label_to_multiqry(second_order_labels, general_descripion,count_per_label):
  cluster_to_multiqry = {}
  for _second_order_raw_cluster in second_order_labels:
    generated_review_list = gen_multiqry(_second_order_raw_cluster, general_descripion,count_per_label)
    cluster_to_multiqry[_second_order_raw_cluster] = generated_review_list
  return cluster_to_multiqry