# extractors/yoe_extractor.py

from extractors.base_extractor import BaseExtractor
from typing import Type, Any, Dict
from pydantic import BaseModel
from pydantic import Field


class YoEModel(BaseModel):
    YoE: str = Field(description="Total years of experience, e.g., '3 years', '2.5 years'")

class YoEExtractor(BaseExtractor):
    """Extract years of experience from text"""

    def get_model(self) -> Type[BaseModel]:
        return YoEModel

    def get_prompt_template(self) -> str:
        return """You are an assistant that extracts the total years of experience from the resume text below.
                    Return a JSON object with the following FORMAT:
                    {FORMAT}

                    Text:
                    {CONTEXT}
                """

    def process_output(self, output: Any) -> Dict[str, Any]:
        return {"YoE": output.YoE}
