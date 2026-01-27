from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import profile_app.document_processing as dp
from profile_app.utils import llm_util as util
import datetime as dt


# llama = OllamaLLM(model='llama3.2', base_url="http://127.0.0.1:11434"

def get_context(file_path):
    return dp.normalize_text(dp.load_file(file_path))

def get_llm():
    return OllamaLLM(model='llama3.2', base_url="http://127.0.0.1:11434")

def ask_llm(prompt):
    return get_llm().invoke(prompt)

def get_current_datetime_str():
    return dt.datetime.now().strftime('%Y-%m-%d')

def get_prompt():
    return """
        You are an AI model with excellent skills in extracting information for a profile based on the fields, format and text below:
        Strict JSON format:
        Format: {FORMAT}
        Text: {CONTEXT}
    - Do not make up any information, leave the field empty if information is not present and not explicit.    
    - Answer in JSON format. No further explanation nor natural language outside of JSON can be present. 
    - Do not include any other information.
    - Do not give any other information except the JSON object.
    - Give the output without any escape characters and only in JSON format.
    - For Skills: Provide a list of skills mentioned in the text and provide a few additional skills relevant to the mentioned Work Experience(s). If no Work Experience is mentioned, only stick to the skills mentioned in the text.
    - For YoE: Provide the Years of Experience as a a float value only based on the Work Experience(s) mentioned in the text. If no Work Experience is mentioned, leave it empty.
    - For any date format, use a string format only. If encountered with present for an end date, use {CURRENT_DATE} as the end date.
    - Any date field should stricly be in either of the formats: "YYYY-MM-DD" or "YYYY/MM/DD" or "Month YYYY" or "Month DD, YYYY", but keep all the dates in concsistent format in the output JSON.
    - For Contact Number: Provide only numbers without any special characters or spaces.
    For role: Extract information from text or leave it empty if not present.
    """

def extract_with_llm(file_path) -> dict:
    """
    Extract information from a text using a language model.
    Input_variables = Provide input variables to be replaced on the prompt
    template = prompt template with mentioned input variables
    """
    FORMAT = util.FORMAT
    CONTEXT = get_context(file_path)
    if CONTEXT is None or len(CONTEXT.strip())<50:
        raise ValueError(f"Could not extract sufficient text from the document.\n Extracted Text: {CONTEXT}")
    
    input_variables = ['FORMAT', 'CONTEXT']
    input_variables_dict = {
        'FORMAT': FORMAT,
        'CONTEXT': CONTEXT,
        'CURRENT_DATE' : get_current_datetime_str()
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

