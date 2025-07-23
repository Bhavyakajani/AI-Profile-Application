from extractors.base_extractor import BaseExtractor
from typing import Type, Any, Dict
from pydantic import BaseModel
from profile_app.Profile import Skills

class SkillsExtractor(BaseExtractor):
    """Extract skills from text"""
    def get_prompt_template(self) -> str:
        return """You are an assistant that extracts a list of skills mentioned in the text below.
                    Only focus on Skills section of the below text.
                    Return your output as a JSON object with the below schema.
                    {FORMAT}
                    Text:
                    {CONTEXT}
                """
    def get_model(self)-> Type[BaseModel]:
        return Skills

    def process_output(self, output: Any) -> Dict[str, Any]:
        return {"skills": output.skills}
    