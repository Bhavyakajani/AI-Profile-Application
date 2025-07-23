# extractors/profile_extractor.py

from extractors.base_extractor import BaseExtractor
from typing import Type, Any, Dict
from pydantic import BaseModel
from profile_app.Profile import ProfileModel  # Import the model with name, email, contact_number


class ProfileExtractor(BaseExtractor):
    """Extract basic profile information: name, contact number, email"""

    def get_model(self) -> Type[BaseModel]:
        return ProfileModel

    def get_prompt_template(self) -> str:
        return """
        You are an assistant that extracts the candidate's personal details from the text below.
        Return ONLY a valid JSON object that matches this schema:
        {FORMAT}

        Do not include any additional text, explanations, or markdown formatting.
        Only include actual values.

        Text:
        {CONTEXT}
        """


    def process_output(self, output: Any) -> Dict[str, Any]:
        return {
            "name": output.name,
            "contact_number": output.contact_number,
            "email": output.email
        }
