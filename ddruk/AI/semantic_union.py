from common_imports import *
from dotenv import load_dotenv

load_dotenv()

def assign_title_to_groups(groups,custom_input_template = None):
  titles = [None]

  class StringSaveNamerToolCheckInput(BaseModel):
    label: str = Field(..., description="A single technical phrase string")

  class StringSaveTool(BaseTool):
      name = "StringSaveTool"
      description = (
        "use this tool when you need to store a single technical phrase string "
        "given a technical phrase string"
      )

      def _run(self,label:str):
          print("StringSaveTool invoked ... Storing a technical phrase ... ")
          titles[0] = label
          return  label

      def _arun(self,reviews: str):
          raise NotImplementedError("This tool does not support async")

      args_schema: Optional[Type[BaseModel]] = StringSaveNamerToolCheckInput

  tools = [StringSaveTool()]

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
  if custom_input_template is None:
    input_template = f"""
      Given a list of same type of phrases :
      {' , '.join(groups)} .

      Your task is to assign a <common technical phrase> that best describes this list.
      This list cover mutiple same type of problems of certain type of user reviews.

      The <common technical phrase> must describe the common meaning of the entire list.
      The <common technical phrase> must be brief and it should contain technical words to describe the whole list EXACTLY and UNAMBIGUOUSLY. It should start with 'Issues related to'

      Answer: <common technical phrase to describe the list>
      Invoke a relevant tool when you need to store <common technical phrase>.
      """
  else:
    input_template = custom_input_template 
    
  agent(input_template)['output']
  return titles[0]


def union_lists(list1:List[str], list2:List[str],threshold=0.85):
    encoder = OpenAIEncoder(
        openai_api_key=os.getenv("OPENAI_API"),
        openai_org_id=os.getenv("OPENAI_ORG"),
    )
    emb1,emb2 = encoder(list1),encoder(list2)
    union = []
    used_indices = set()

    for i, s1_emb in enumerate(emb1):
        matched = False
        for j, s2_emb in enumerate(emb2):
            if j not in used_indices:
                if np.dot(s1_emb, s2_emb) > threshold:
                    union.append([list1[i], list2[j]])
                    used_indices.add(j)
                    matched = True
                    break
        if not matched:
            union.append([list1[i]])

    for j, s2_emb in enumerate(emb2):
        if j not in used_indices:
            union.append([list2[j]])

    return union


def group_similar_strings(L,threshold=0.85):
    groups = []
    used_indices = set()
    encoder = OpenAIEncoder(
        openai_api_key=os.getenv("OPENAI_API"),
        openai_org_id=os.getenv("OPENAI_ORG"),
    )
    emb = encoder(L)

    for i in range(len(L)):
        if i not in used_indices:
            current_group = [L[i]]
            used_indices.add(i)
            for j in range(i + 1, len(L)):
                if j not in used_indices:
                    if np.dot(emb[i], emb[j]) > threshold:
                        current_group.append(L[j])
                        used_indices.add(j)
            groups.append(current_group)

    return groups