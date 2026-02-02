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
        You are an expert resume parser. Your task is to extract relevant information from the given text according to the specified format.
        Specifically, extract the following fields:
        - Name: Name of the Canidate
        - Email: The candidate's email address
        - Phone: The candidate's phone number, including country code if present
        - College/School (output as "institution")
        - Degree
        - Start Date of Education: in dd/mm/yyyy format. If the resume does not provide the day or month, default the missing parts to "01". If you encounter Present then use the current date, i.e. {CURRENT_DATE}.
        - End Date of Education: in dd/mm/yyyy format. If the resume does not provide the day or month, default the missing parts to "01". If you encounter Present then use the current date, i.e. {CURRENT_DATE}.
        - Location
        - Skills: A list of relevant skills mentioned in the text. Extract the skills only from the skills section if present, else derive from the entire text. Add a few additional relevant skills based on the Work Experience(s) mentioned in the text.
        - YoE: Total Years of Experience as a float value.
        - Company
        - Start Date: in dd/mm/yyyy format. If the resume does not provide the day or month, default the missing parts to "01". If you encounter Present then use the current date, i.e. {CURRENT_DATE}.
        - End Date: in dd/mm/yyyy format. If the resume does not provide the day or month, default the missing parts to "01". If you encounter Present then use the current date, i.e. {CURRENT_DATE}.
        Location
        - Role: Extract ONLY the job title (e.g., "Data Engineer", "Software Developer", "Project Manager"). Do NOT include project information or descriptions in this field - just the official job title.
        FOR EXPERIENCE, IMPORTANT: Create only ONE entry per company, even if the person worked on multiple projects or had multiple roles at the same company. If there were multiple positions at the same company, use the most senior or most recent role in the Role field. The earliest start date and the latest end date should be used for the company's overall employment period.
        
        If any of these fields are not present in the resume, return null for that field

        Return your output as a JSON object with the below schema. 
        {FORMAT}

        Text:
        {CONTEXT}
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

