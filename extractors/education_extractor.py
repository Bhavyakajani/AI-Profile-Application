# extractors/education_extractor.py

from extractors.base_extractor import BaseExtractor
from typing import Type, Any, Dict
from pydantic import BaseModel
from profile_app.Profile import Education

class EducationExtractor(BaseExtractor):
    """Extract education details from text"""

    def get_model(self) -> Type[BaseModel]:
        return Education

    def get_prompt_template(self) -> str:
        return """You are an assistant that extracts education details from the following text.
                    Only focus on the Education section.
                    Return a JSON object with the following FORMAT:
                    {FORMAT}

                    Text:
                    {CONTEXT}
                """

    def process_output(self, output: Any) -> Dict[str, Any]:
        return {
            "degree": output.degree,
            "institution": output.institution,
            "start_date": output.start_date,
            "end_date": output.end_date,
            "location": output.location,
            "cgpa": output.cgpa
        }
