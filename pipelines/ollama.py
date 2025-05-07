import re
from langchain_community.llms.ollama import Ollama
import logging
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import List

from getpass import getpass

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass()

# Pydantic models
class PersonalDetails(BaseModel):
    designationTitles: List[str] = Field(default_factory=list, description="An array of designationTitles of candidate.")
    name: str = Field(default="", description="A string representing the name.")
    email: str = Field(default="", description="A string representing the email.")
    phone: str = Field(default="", description="A string representing the phone number.")
    city: str = Field(default="", description="A string representing the city.")
    country: str = Field(default="", description="A string representing the country.")
    address: str = Field(default="", description="A string representing the street, state, and postalCode.")
    linkedin: str = Field(default="", description="A string representing the LinkedIn profile URL.")
    github: str = Field(default="", description="A string representing the GitHub profile URL.")
    portfolioSite: str = Field(default="", description="A string representing the personal website or portfolio site URL.")

class EducationDetails(BaseModel):
    institute_location: str = Field(default="", description="A string representing the location of the educational institute.")
    institute: str = Field(default="", description="A string representing the name of the educational institute.")
    degree: str = Field(default="", description="A string representing the degree earned.")
    fieldOfStudy: str = Field(default="", description="A string representing the field of study.")
    startDate: str = Field(default="", description="A string representing the start date of education (e.g., 'MM/DD/YYYY').")
    endDate: str = Field(default="", description="A string representing the end date of education (e.g., 'MM/DD/YYYY').")

class Experience(BaseModel):
    companyName: str = Field(default="", description="A string representing the name of the company.")
    title: str = Field(default="", description="A string representing the job title.")
    startDate: str = Field(default="", description="A string representing the start date of employment (e.g., 'MM/DD/YYYY').")
    endDate: str = Field(default="", description="A string representing the end date of employment (e.g., 'MM/DD/YYYY').")
    location: str = Field(default="", description="A string representing the company's location.")
    description: str = Field(default="", description="A string describing job responsibilities or achievements.")

class Project(BaseModel):
    title: str = Field(default="", description="A string representing the project title.")
    description: str = Field(default="", description="A string describing the project.")
    skillsUsed: List[str] = Field(default_factory=list, description="An array of strings representing technologies or skills used in the project.")
    liveUrl: str = Field(default="", description="A string representing the project's URL.")

class DateRange(BaseModel):
    fromMonth: int = Field(default=0, description="The starting month of the certification.")
    fromYear: int = Field(default=0, description="The starting year of the certification.")
    isOngoing: bool = Field(default=False, description="Indicates if the certification is ongoing.")
    toMonth: int = Field(default=0, description="The ending month of the certification.")
    toYear: int = Field(default=0, description="The ending year of the certification.")

class Certification(BaseModel):
    institute: str = Field(default="", description="The name of the institute offering the certification.")
    courseTitle: str = Field(default="", description="The title of the course or certification.")
    dateRange: DateRange = Field(default_factory=DateRange, description="The date range of the certification.")

class Resume(BaseModel):
    personalDetails: PersonalDetails = Field(description="Personal details of the candidate.")
    aboutMe: str = Field(default="", description="A brief summary of the candidate's professional background.")
    educationDetails: List[EducationDetails] = Field(default_factory=list, description="List of education details.")
    experiences: List[Experience] = Field(default_factory=list, description="List of work experiences.")
    technicalSkills: List[str] = Field(default_factory=list, description="An array of technical skills.")
    softSkills: List[str] = Field(default_factory=list, description="An array of soft skills.")
    languages: List[str] = Field(default_factory=list, description="An array of languages spoken.")
    projects: List[Project] = Field(default_factory=list, description="List of projects.")
    areaOfInterest: List[str] = Field(default_factory=list, description="An array of interests.")
    certifications: List[Certification] = Field(default_factory=list, description="List of certifications.")


def get_resume_details(cv_text):
    """
    Simplifies and arranges CV details into a structured format using an LLM.

    Args:
        cv_text (str): Raw CV text.

    Returns:
        dict: A dictionary containing the organized CV details.
    """
    
    print("inside get_resume_details")
    try:
        prompt = f"""
        Simplify and organize the following CV details. Extract the required information and structure it as JSON. If any detail is missing, leave it empty. Additionally, generate a professional 'About Me' section based on the details provided.

        - Normalize all dates to MM/DD/YYYY format. Use '01' as the default day or month if missing.
        - Split and normalize all technicalSkills. Separate entries combined with symbols like brackets, slashes, commas, or hyphens into distinct entries.
        - The description of experiences is always be a string.

        Required format:
        {{
            "personalDetails": {{
                "name": "",
                "phone": "",
                "city": "",
                "country": "",
                "address": "",
                "email": "",
                "linkedin": "",
                "github": "",
                "portfolioSite": ""
            }},
            "aboutMe": "",
            "educationDetails": [
                {{
                    "institute": "",
                    "degree": "",
                    "fieldOfStudy": "",
                    "startDate": "",
                    "endDate": "",
                    "currentlyStudying": false
                }}
            ],
            "experiences": [
                {{
                    "companyName": "",
                    "title": "",
                    "startDate": "",
                    "endDate": "",
                    "location": "",
                    "description": "",
                    "currentlyWorking": false
                }}
            ],
            "skills": [
                {{
                    "title": "Soft Skills",
                    "tags": []
                }},
                {{
                    "title": "Technical Skills",
                    "tags": []
                }}
            ],
            "languages": [],
            "projects": [
                {{
                    "title": "",
                    "description": "",
                    "skillsUsed": [],
                    "liveUrl": ""
                }}
            ],
            "areaOfInterest": "",
            "certifications": []
        }}

        CV Details:
        {cv_text}
        """

        # OpenAimodel = ChatOpenAI(temperature=0 , model="gpt-3.5-turbo",)
        # OpenAimodel = ChatGoogleGenerativeAI(
        #     model="gemini-1.0-pro",
        #     temperature=0,
        #     google_api_key=os.getenv('GOOGLE_API_KEY')
        # )
        model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv('GROQ_API_KEY'),
        )

        parser = JsonOutputParser(pydantic_object=Resume)

        prompt2 = PromptTemplate(
            template="this is the prompt.\n{prompt}\n",
        )
        chain = prompt2 | model | parser
        output = chain.invoke({prompt})

        return output

    except Exception as e:
        logging.error(f"Error inside get_resume_details: {e}")
        return {
            "error": "LLM Processing Error",
            "message": str(e)
        }

def normalize_skills(skills):
    """
    Normalizes and separates skills into distinct entries.

    Args:
        skills (list): A list of skills as strings.

    Returns:
        list: A cleaned and normalized list of skills.
    """
    normalized = []
    for skill in skills:
        # Use a more comprehensive regex to split by common delimiters and parentheses
        split_skills = [s.strip() for s in re.split(r'[,/\\()\-\[\]]', skill) if s.strip()]
        normalized.extend(split_skills)
    return list(set(normalized))  # Remove duplicates
