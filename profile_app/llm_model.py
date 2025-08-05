from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import document_processing as dp
from profile_app.utils import llm_util as util


# llama = OllamaLLM(model='llama3.2', base_url="http://127.0.0.1:11434"

def get_context(file_path):
    return dp.normalize_text(dp.load_file(file_path))

def get_llm():
    return OllamaLLM(model='llama3.2', base_url="http://127.0.0.1:11434")

def ask_llm(prompt):
    return get_llm().invoke(prompt)

def get_prompt():
    return """
        You are an AI model with excellent skills in extracting information for a profile based on the fields, format and text below:
        Strict JSON format:
        Format: {FORMAT}
        Text: {CONTEXT}
    - For the start_date and end_date, if it is not explicitly mentioned, then fill the field from implicit mention
    - Do not make up any information, leave if the field empty if information is not present.    
    - Answer in JSON format. No further explanation nor natural language outside of JSON can be present. 
    - Do not include any other information.
    - Give the output without any escape characters and only in JSON format.
    """

def extract_with_llm(file_path):
    """
    Extract information from a text using a language model.
    Input_variables = Provide input variables to be replaced on the prompt
    template = prompt template with mentioned input variables
    """
    FORMAT = util.FORMAT
    CONTEXT = get_context(file_path)
    input_variables = ['FORMAT', 'CONTEXT']
    input_variables_dict = {
        'FORMAT': FORMAT,
        'CONTEXT': CONTEXT
    }
    prompt = PromptTemplate(
        input_variables=input_variables,
        template = get_prompt()
    )

    #Instantiate llm
    llm = get_llm()

    #Create a chain
    chain = prompt | llm | JsonOutputParser()

    # Send a dictionary to map the input variables(place holders) with actual values
    response_json = chain.invoke(input_variables_dict)

    return response_json

