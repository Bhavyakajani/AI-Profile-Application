from extractors.base_extractor import BaseExtractor
from typing import Type, Any, Dict
from pydantic import BaseModel
from profile_app.Profile import WorkExperience

class ExperienceExtractor(BaseExtractor):
    """Extract work experience from text"""

    def get_model(self) -> Type[BaseModel]:
        return WorkExperience

    def get_prompt_template(self) -> str:
        return """You are an assistant that extracts work experience from the following text.
                    Only focus on the Experience or Work History section.
                    Return a JSON object with the following FORMAT:
                    {FORMAT}

                    Text:
                    {CONTEXT}
        """

    def process_output(self, output: Any) -> Dict[str, Any]:
        return {
            "company": output.company,
            "start_date": output.start_date,
            "end_date": output.end_date,
            "location": output.location,
            "role": output.role,
            "currently_working": output.currently_working
        }
