resume_extraction_temp = """

Please extract the following details from the provided resume and format them as a single, well-structured JSON object:

{
  "personalDetails": {
    "firstName": "",
    "lastName": "",
    "email": "",
    "phone": "",
    "address": {
      "street": "",
      "city": "",
      "state": "",
      "postalCode": "",
      "country": ""
    },
    "linkedin": "",
    "github": "",
    "website": ""
  },
  "summary": "",
  "education": [
    {
      "institution": "",
      "degree": "",
      "fieldOfStudy": "",
      "startDate": "",
      "endDate": "",
      "grade": "",
      "location": ""
    }
  ],
  "workExperience": [
    {
      "company": "",
      "jobTitle": "",
      "startDate": "",
      "endDate": "",
      "location": "",
      "description": []
    }
  ],
  "skills": {
    "technicalSkills": [
      ""
    ],
    "softSkills": [
      ""
    ],
    "languages": [
      ""
    ]
  },
  "projects": [
    {
      "title": "",
      "description": "",
      "technologiesUsed": [
        ""
      ],
      "link": "",
      "startDate": "",
      "endDate": ""
    }
  ],
  "interests": [],
  "certifications": [
    {
      "name": "",
      "issuingOrganization": "",
      "issueDate": "",
      "expirationDate": "",
      "credentialId": "",
      "credentialUrl": ""
    }
  ]
}

Ensure the JSON output is well-formatted and accurately reflects the data from the resume. 
If no information is found for a specific field, genrate it according to the given input if didnot fint the details from the input leave the field empty instead of deleting it. did not use any data from outside the prompt
Only return a single JSON object as the output.

***RESUME***

"""


jsonObject = """

And Now i want this type object with same keys.

{
  "personalDetails": {
    "name": "",
    "phone": "",
    "city": "",
    "country": "",
    "address": "",
    "linkedin": "",
    "github": "",
    "portfolioSite": ""
  },
  "aboutMe": "",
  "educationDetails": [
    {
      "institute": "",
      "degree": "",
      "fieldOfStudy": "",
      "startDate": "",
      "endDate": "",
      "currentlyStudying": false
    }
  ],
  "experiences": [
    {
      "companyName": "",
      "title": "",
      "startDate": "",
      "endDate": "",
      "location": "",
      "description": [],
      "currentlyWorking": false
    }
  ],
  "technicalSkills": [],
  "softSkills": [],
  "languages": [],
  "projects": [
    {
      "title": "",
      "description": "",
      "skillsUsed": [],
      "liveUrl": ""
    }
  ],
  "areaOfInterest": [],
  "certifications": [
    {
      "name": "",
      "issuingOrganization": "",
      "issueDate": "",
      "expirationDate": "",
      "credentialId": "",
      "credentialUrl": ""
    }
  ]
}

"""

resume_format_instructions = """
You are an AI that generates structured JSON objects based on user-provided information. Respond strictly with a valid JSON object following the schema below. 

**Do not modify, rename, or reformat any field names in the schema.** 
**Ensure all field names are exactly as provided in the schema.** 
**Respond only with the JSON object, without any text, comments, or characters outside the JSON object.**

If data for a field is not found, leave it as an empty string ("") or an empty array ([]). If a field requires a specific format, adhere strictly to the format described in the schema.

Schema:
{
  "personalDetails": {
    "name": "A string representing the name. If not found, leave it as an empty string ('').",
    "phone": "A string representing the phone number. If not found, leave it as an empty string ('').",
    "city": "A string representing the city. If not found, leave it as an empty string ('').",
    "country": "A string representing the country. If not found, leave it as an empty string ('').",
    "address": "A string representing the street, state, and postalCode. If not found, leave it as an empty string ('').",
    "linkedin": "A string representing the LinkedIn profile URL. If not found, leave it as an empty string ('').",
    "github": "A string representing the GitHub profile URL. If not found, leave it as an empty string ('').",
    "portfolioSite": "A string representing the personal website or portfolio site URL. If not found, leave it as an empty string ('')."
  },
  "aboutMe": "A string providing a brief summary of the candidate's professional background. If not found, generate it based on the provided information.",
  "educationDetails": [
    {
      "institute": "A string representing the name of the educational institute. If not found, leave it as an empty string ('').",
      "degree": "A string representing the degree earned. If not found, leave it as an empty string ('').",
      "fieldOfStudy": "A string representing the field of study. If not found, leave it as an empty string ('').",
      "startDate": "A string representing the start date of education (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "endDate": "A string representing the end date of education (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "currentlyStudying": "A boolean indicating whether the candidate is currently studying. If not found, set it to false."
    }
  ],
  "experiences": [
    {
      "companyName": "A string representing the name of the company. If not found, leave it as an empty string ('').",
      "title": "A string representing the job title. If not found, leave it as an empty string ('').",
      "startDate": "A string representing the start date of employment (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "endDate": "A string representing the end date of employment (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "location": "A string representing the company's location. If not found, leave it as an empty string ('').",
      "description": "An array of strings describing job responsibilities or achievements. If not found, leave it as an empty array ([]).",
      "currentlyWorking": "A boolean indicating whether the candidate is currently working in this job. If endDate is provided, set this to false. If endDate is not provided, set this to true."
    }
  ],
  "technicalSkills": "An array of strings representing technical skills. If not found, leave it as an empty array ([]).",
  "softSkills": "An array of strings representing soft skills. If not found, leave it as an empty array ([]).",
  "languages": "An array of strings representing languages spoken. If not found, leave it as an empty array ([]).",
  "projects": [
    {
      "title": "A string representing the project title. If not found, leave it as an empty string ('').",
      "description": "A string describing the project. If the description is missing but the title is available, reuse the title as the description. If not found, leave it as an empty string ('').",
      "skillsUsed": "An array of strings representing technologies or skills used in the project. If not found, leave it as an empty array ([]).",
      "liveUrl": "A string representing the project's URL. If not found, leave it as an empty string ('')."
    }
  ],
  "areaOfInterest": "An array of strings representing the candidate's interests. If not found, leave it as an empty array ([]).",
  "certifications": [
    {
      "name": "A string representing the certification name. If not found, leave it as an empty string ('').",
      "issuingOrganization": "A string representing the issuing organization. If not found, leave it as an empty string ('').",
      "issueDate": "A string representing the issue date of the certification (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "expirationDate": "A string representing the expiration date of the certification (e.g., 'MM/YYYY'). If not found, leave it as an empty string ('').",
      "credentialId": "A string representing the credential ID. If not found, leave it as an empty string ('').",
      "credentialUrl": "A string representing the credential URL. If not found, leave it as an empty string ('')."
    }
  ]
}

Extract or generate the details from the data provided and strictly return a valid JSON object following the schema above.
"""
schema = """ 
{
  "personalDetails": {
    "name": "A string representing the name. Leave empty if not found.",
    "phone": "A string representing the phone number. Leave empty if not found.",
    "city": "A string representing the city. Leave empty if not found.",
    "country": "A string representing the country. Leave empty if not found.",
    "address": "A string representing the street, state, and postal code. Leave empty if not found.",
    "linkedin": "A string representing the LinkedIn profile URL. Leave empty if not found.",
    "github": "A string representing the GitHub profile URL. Leave empty if not found.",
    "portfolioSite": "A string representing the personal website or portfolio URL. Leave empty if not found."
  },
  "aboutMe": "A string providing a brief summary of the candidate's professional background. If missing, generate one.",
  "educationDetails": [
    {
      "institute": "The name of the educational institution. Leave empty if not found.",
      "degree": "The degree earned. Leave empty if not found.",
      "fieldOfStudy": "The field of study. Leave empty if not found.",
      "startDate": "Start date of education. If missing, use '01/01/YYYY'.",
      "endDate": "End date of education. If missing, use '01/01/YYYY'.",
      "currentlyStudying": "Boolean indicating if currently studying. Set to false if not found."
    }
  ],
  "experiences": [
    {
      "companyName": "The name of the company. Leave empty if not found.",
      "title": "The job title. Leave empty if not found.",
      "startDate": "Start date of employment. If missing, use '01/01/YYYY'.",
      "endDate": "End date of employment. If missing, use '01/01/YYYY'.",
      "location": "Company's location. Leave empty if not found.",
      "description": "A string describing job responsibilities or achievements. Leave empty if not found.",
      "currentlyWorking": "Boolean indicating if still working in the job. Set to false if endDate is provided."
    }
  ],
  "technicalSkills": "An array of strings representing technical skills. Split combined skills into individual entries. Leave empty if not found.",
  "softSkills": "An array of strings representing soft skills. Leave empty if not found.",
  "languages": "An array of strings representing languages spoken. Leave empty if not found.",
  "projects": [
    {
      "title": "The project title. Leave empty if not found.",
      "description": "Project description. If missing but title is found, use the title as the description.",
      "skillsUsed": "Array of technologies or skills used in the project. Leave empty if not found.",
      "liveUrl": "The URL for the project's live version. Leave empty if not found."
    }
  ],
  "areaOfInterest": "An array of strings representing the candidate's areas of interest. Leave empty if not found.",
  "certifications": [
    {
      "name": "The name of the certification. Leave empty if not found.",
      "issuingOrganization": "The issuing organization. Leave empty if not found.",
      "issueDate": "Issue date of the certification. Use '01/01/YYYY' if missing.",
      "expirationDate": "Expiration date of the certification. Use '01/01/YYYY' if missing.",
      "credentialId": "Credential ID. Leave empty if not found.",
      "credentialUrl": "Credential URL. Leave empty if not found."
    }
  ]
}

"""

job_extraction_temp = """

Please extract the following details from the provided job description and format them as JSON without any comments:

{
  "jobTitle": "",
  "company": "",
  "location": "",
  "employmentType": "",
  "industry": "",
  "experienceRequired": "",
  "educationLevel": "",
  "skills": [],
  "responsibilities": [],
  "qualifications": [],
}




Ensure the JSON output is well-formatted and accurately reflects the data from the job description.
if you can not find anything leave it empty, plz do not remove it completely
Even if you can not find job description, do not remove the field from the json. instead leave it empty

***JOB DESCRIPTION***

"""



recruiter_temp = """

Assess the relevance of this resume to the job description.

Evaluation Metrics:

1. Job Title
2. Skills Match
3. Education
4. Experience

The less these things match with the job description, the less the score will be.

Don't add anything below and after result
Example output overall score between 0 and 100:

{
  "score": "",
  "reason": ""
}


Ensure the JSON output is well-formatted and accurately reflects the results.
Below is the resume and Job description

"""