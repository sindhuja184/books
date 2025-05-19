from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model= "deepseek-r1")

prompt_template = """
You are a helpful book recommender system.

Given the book title: "{book_title}", please provide a JSON dictionary of the top 5 books similar to it.
Return the dictionary with book names as keys and a short reason why they are similar as values.
"""

prompt = PromptTemplate(
    imput_variables = ["book_title"],
    template= prompt_template
)

chain = prompt | llm