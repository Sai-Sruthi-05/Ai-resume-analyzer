import re
import string
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nlp_utils import extract_entities, get_top_tfidf_keywords, nlp

# Technical skills list
TECH_SKILLS = [
    "python", "java", "javascript", "html", "css", "sql", "nosql", "mongodb", "postgresql",
    "mysql", "oracle", "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "agile", "scrum", "kanban",
    "react", "angular", "vue", "node", "express", "django", "flask", "spring", "hibernate",
    "typescript", "php", "ruby", "rails", "c++", "c#", ".net", "scala", "swift", "kotlin",
    "rust", "go", "r", "tableau", "power bi", "excel", "word", "powerpoint", "figma", "sketch",
    "ai", "ml", "deep learning", "nlp", "computer vision", "data analysis", "data science",
    "big data", "hadoop", "spark", "kafka", "elasticsearch", "kibana", "logstash", "grafana",
    "prometheus", "linux", "unix", "windows", "macos", "android", "ios", "mobile development",
    "web development", "backend", "frontend", "full stack", "devops", "sre", "security",
    "networking", "redux", "graphql", "rest api", "soap", "microservices", "architecture",
    "cloud", "serverless", "aws lambda", "azure functions", "firebase", "heroku", "digital ocean",
    "vercel", "netlify", "github actions", "ci/cd", "tdd", "bdd", "unit testing", "integration testing",
    "selenium", "cypress", "jest", "mocha", "pytest", "junit", "webpack", "babel", "sass", "less"
]

# Common job roles
JOB_ROLES = [
    "software engineer", "software developer", "frontend developer", "backend developer",
    "full stack developer", "devops engineer", "site reliability engineer", "data scientist",
    "data engineer", "data analyst", "machine learning engineer", "ai engineer", "cloud engineer",
    "cloud architect", "solution architect", "system architect", "database administrator",
    "network engineer", "security engineer", "product manager", "project manager", "scrum master",
    "technical lead", "engineering manager", "cto", "vp of engineering", "qa engineer",
    "quality assurance", "test engineer", "ui developer", "ux designer", "ui/ux designer",
    "graphic designer", "content writer", "technical writer", "marketing specialist",
    "sales representative", "customer support", "system administrator", "it support",
    "business analyst", "operations manager", "finance manager", "hr manager", "recruiter",
    "mobile developer", "android developer", "ios developer", "game developer", "blockchain developer",
    "web designer", "seo specialist", "digital marketer", "growth hacker", "content strategist"
]

# Education terms
EDUCATION_TERMS = [
    "bachelor", "master", "phd", "doctorate", "bs", "ms", "ba", "ma", "mba", "btech", "mtech",
    "bsc", "msc", "associate", "diploma", "certificate", "university", "college", "school",
    "institute", "academy", "degree", "major", "minor", "concentration", "specialization",
    "graduated", "gpa", "honors", "cum laude", "magna cum laude", "summa cum laude"
]

def extract_text_from_pdf(pdf_path_or_file):
    """Extract text content from a PDF file or BytesIO object"""
    text = ""
    try:
        # Check if the input is a BytesIO object
        if hasattr(pdf_path_or_file, 'read'):
            pdf_reader = PyPDF2.PdfReader(pdf_path_or_file)
        else:
            # If it's a file path
            pdf_reader = PyPDF2.PdfReader(pdf_path_or_file)
            
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def preprocess_text(text):
    """Preprocess text by removing punctuation, lowercase, and tokenizing"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

def identify_skills(text):
    """
    Identify technical skills from resume text using NER and rule-based matching
    """
    tokens = preprocess_text(text)
    skills = []
    
    # Process with SpaCy for better token analysis
    doc = nlp(text.lower())
    
    # Check for single word skills
    for token in tokens:
        if token.lower() in TECH_SKILLS:
            skills.append(token.lower())
    
    # Check for multi-word skills
    text_lower = text.lower()
    for skill in TECH_SKILLS:
        if ' ' in skill and skill in text_lower:
            skills.append(skill)
    
    # Use SpaCy's token attributes to identify potential technical terms
    for token in doc:
        # Check if token looks like a technical term (e.g., camelCase, PascalCase, etc.)
        if (re.match(r'^[a-z]+[A-Z][a-zA-Z]*$', token.text) or  # camelCase
            re.match(r'^[A-Z][a-z]+[A-Z][a-zA-Z]*$', token.text)):  # PascalCase
            if token.text.lower() not in [s.lower() for s in skills]:
                skills.append(token.text.lower())
    
    # Remove duplicates and sort
    return sorted(list(set(skills)))

def identify_job_roles(text):
    """
    Identify potential job roles from resume text using NER and rule-based matching
    """
    text_lower = text.lower()
    roles = []
    
    # Use SpaCy NER to identify organizations that might be job titles
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            for role in JOB_ROLES:
                if role in ent.text.lower():
                    roles.append(role)
    
    # Also check for direct matches
    for role in JOB_ROLES:
        if role in text_lower:
            roles.append(role)
    
    return list(set(roles))  # Remove duplicates

def extract_education(text):
    """
    Extract education information from resume text using NER and pattern matching
    """
    # Use named entity recognition to extract educational institutions
    doc = nlp(text)
    education_info = []
    
    # Extract organizations that are likely to be educational institutions
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    edu_keywords = ["university", "college", "institute", "school", "academy"]
    
    for org in orgs:
        if any(keyword in org.lower() for keyword in edu_keywords):
            education_info.append(org)
    
    # Also extract sections containing education terms
    entities = extract_entities(text)
    if "DEGREE" in entities:
        education_info.extend(entities["DEGREE"])
    
    # Keep your existing pattern matching logic for completeness
    text_lower = text.lower()
    for term in EDUCATION_TERMS:
        if term in text_lower:
            matches = re.finditer(
                r'([^.!?]*' + term + r'[^.!?]*[.!?])',
                text_lower,
                re.IGNORECASE
            )
            
            for match in matches:
                education_info.append(match.group(0).strip())
    
    # Clean up education info
    cleaned_info = []
    for info in education_info:
        # Remove extra whitespace, newlines, etc.
        cleaned = re.sub(r'\s+', ' ', info).strip()
        if len(cleaned) > 5:  # Only keep substantial entries
            cleaned_info.append(cleaned)
    
    # Remove duplicates
    return list(set(cleaned_info))

def extract_keywords(text):
     """
    Extract important keywords from resume text using NER, TF-IDF and rule-based methods
    """
    # Clean text by removing emails, phone numbers, and URLs
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)  # Remove emails
    text = re.sub(r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', '', text)  # Remove phone numbers
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'\b\d{9,12}\b', '', text)  # Remove numbers that look like IDs or phone numbers
    
    # Remove personal identifying names
    text = re.sub(r'\b(?:Name|Full Name|Full|Candidate)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b[A-Z][a-z]+\s+(?:[A-Z]\.?\s+)?[A-Z][a-z]+\b', '', text)
    
    # Extract named entities
    entities = extract_entities(text)
    
    # Extract skills
    skills = identify_skills(text)
    
    # Extract job roles
    roles = identify_job_roles(text)
    
    # Extract TF-IDF keywords (more accurate than frequency-based)
    tfidf_keywords = get_top_tfidf_keywords(text, n=15)
    
    # Combine keywords with priority on technical terms and named entities
    combined_keywords = []
    
    # First add skills (highest priority)
    combined_keywords.extend(skills)
    
    # Then add roles
    combined_keywords.extend([role for role in roles if role not in combined_keywords])
    
    # Then add organizations that might be relevant
    if "ORG" in entities:
        combined_keywords.extend([org for org in entities["ORG"] 
                                if org.lower() not in [k.lower() for k in combined_keywords]])
    
    # Then add TF-IDF keywords
    combined_keywords.extend([kw for kw in tfidf_keywords 
                            if kw.lower() not in [k.lower() for k in combined_keywords]])
    
    # Ensure uniqueness and remove very short keywords
    unique_keywords = []
    for k in combined_keywords:
        if (k.lower() not in [uk.lower() for uk in unique_keywords] and len(k) > 2):
            unique_keywords.append(k)
    
    return unique_keywords[:30]  # Limit to top 30 keywords