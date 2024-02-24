import copy
import datetime
import numpy as np
import json
import os
import openai
import time
import string
import re
import collections
import tiktoken
import google_play_scraper

from datetime import datetime as dt
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from collections import defaultdict
from typing import Optional, Type, List, Tuple
from pydantic import BaseModel, Field
from getpass import getpass


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.agents import Tool,initialize_agent, AgentType
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain, LLMMathChain, TransformChain, SequentialChain,  create_extraction_chain, create_extraction_chain_pydantic, create_tagging_chain, create_tagging_chain_pydantic

from semantic_router import Route
from semantic_router.encoders import OpenAIEncoder
from semantic_router.layer import RouteLayer
from dotenv import load_dotenv

"""
pip install -qU langchain tqdm google-play-scraper langchain_openai pydantic openai tiktoken semantic-router matplotlib python-dotenv
"""