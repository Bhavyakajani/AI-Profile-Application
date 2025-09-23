from typing import Type, Dict, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from profile_app.ai.llm_model import extract_with_llm  # Assuming llm_model is defined in a module named llm_model


class BaseExtractor(ABC):
    """Base extractor class """
    @abstractmethod
    def get_model(self) -> Type[BaseModel]:
        """Get the Pydantic model for the extractor."""
        pass
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Get the prompt template for the extractor."""
        pass
    @abstractmethod
    def process_output(self, output: Any) -> Dict[str, Any]:
        """Process the output from the LLM."""
        pass

    def get_input_variables(self) -> list:
        """Return list of variable names used in the prompt template."""
        return ["text"]
    
    def prepare_input_data(self, extracted_text: str) -> Dict[str, Any]:
        """Prepare the input data for the LLM."""
        return {"text": extracted_text}

    def extract(self, extracted_text:str) -> Dict[str, Any]:
        """Extract information from the resume"""
        input_data = self.prepare_input_data(extracted_text)
        output = extract_with_llm(self.get_model())
        print("LLM raw output:", output)
        
        # parsed_data = json.loads(output)  # or however you're decoding LLM output
        model_class = self.get_model()
        model_instance = model_class(**output)  # ← create Pydantic model
        return self.process_output(model_instance)
        
