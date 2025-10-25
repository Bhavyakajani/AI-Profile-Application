from extractors.profile_extractor import ProfileExtractor
from extractors.skills_extractor import SkillsExtractor
from extractors.education_extractor import EducationExtractor
from extractors.experience_extractor import ExperienceExtractor
from extractors.yoe_extractor import YoEExtractor


class ResumeProcessor:
    """Class for processing resumes and extracting information."""
    
    def __init__(self, resume_dir="./data", output_dir="./Results"):
        self.resume_dir = resume_dir
        self.output_dir = output_dir
        # Create extractors
        self.profile_extractor = ProfileExtractor()
        self.skills_extractor = SkillsExtractor()
        self.education_extractor = EducationExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.yoe_extractor = YoEExtractor()

    def process_resume(self, resume_text: str) -> dict:
        """Process the resume text and extract information."""
        extracted_data = {'profile': self.profile_extractor.extract(resume_text),
                          'skills': self.skills_extractor.extract(resume_text),
                          'education': self.education_extractor.extract(resume_text),
                          'experience': self.experience_extractor.extract(resume_text),
                          'yoe': self.yoe_extractor.extract(resume_text)}
        return extracted_data

