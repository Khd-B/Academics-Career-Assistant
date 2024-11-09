import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

import streamlit as st
import sqlite3
from transformers import pipeline
from fpdf import FPDF

# --- Database setup ---
conn = sqlite3.connect('career_assistant.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS user_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age_group TEXT,
        marital_status TEXT,
        dependants INTEGER,
        education_level TEXT,
        fields_of_study TEXT,
        employment_status TEXT,
        years_of_experience TEXT,
        monthly_earnings TEXT,
        hard_skills TEXT,
        soft_skills TEXT,
        languages TEXT,
        career_interests TEXT,
        other_career TEXT,
        work_type TEXT,
        work_schedule TEXT,
        future_aspirations TEXT
    )
''')

# --- Use a high-level pipeline ---
from transformers import pipeline

# Load the FLAN-T5 model via pipeline for text-to-text generation
pipe = pipeline("text2text-generation", model="google/flan-t5-base")

# --- Streamlit App ---
st.title("Your Academics & Career Assistant")

st.markdown("""
Welcome to Your Academics & Career Assistant! This application will guide you through a series of questions to help recommend study and career options based on your inputs.
""")

# Reset Fields Functionality
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Questionnaire: Numbered Questions

# 1. Age Group Selection
st.subheader("1. Select your age group:")
age_group = st.selectbox(
    "",
    ["Select Age Group", "15 - 18", "18 - 22", "22 - 30", "30 - 40", "41 - 50", "51 - 65", "65+"],
    index=0 if not st.session_state.form_submitted else None
)

# 2. Marital Status & Dependants
st.subheader("2. What is your marital status?")
marital_status = st.selectbox("", 
                              ["Select Marital Status", "Single", "Married", "Divorced", "Widowed"], 
                              index=0 if not st.session_state.form_submitted else None)

# Disable dependants field if marital status is "Single"
dependants_disabled = False
if marital_status == "Single":
    dependants_disabled = True  

if not dependants_disabled:
    dependants = st.number_input("How many dependants do you have?", min_value=0, max_value=10, step=1)
else:
    dependants = None  # No input if Single

# 3. Education Level
st.subheader("3. What is your highest level of education?")
education_level = st.selectbox("", 
                               ["Select Education Level", "High School", "Undergraduate", "Graduate", "Postgraduate", "PhD"], 
                               index=0 if not st.session_state.form_submitted else None)

# 4. Fields of Study based on Education Level
st.subheader("4. What is your field of study? (Select one or more)")

fields_of_study = []

if education_level == "High School":
    fields_of_study = st.multiselect("", 
                                     ["Science", "Commerce", "Arts", "Humanities", "Medicine"])
elif education_level == "Undergraduate":
    fields_of_study = st.multiselect("", 
                                     ["Science", "Commerce", "Arts", "Humanities", "Law", "IT", "Engineering", "Business", "Medicine"])
elif education_level == "Graduate":
    fields_of_study = st.multiselect("", 
                                     ["Science", "Commerce", "Arts", "Humanities", "Law", "IT", "Engineering", "Business", "Medicine", "Social Sciences"])
elif education_level == "Postgraduate":
    fields_of_study = st.multiselect("", 
                                     ["Science", "Commerce", "Arts", "Humanities", "Law", "IT", "Engineering", "Business", "Medicine", "Social Sciences"])
elif education_level == "PhD":
    fields_of_study = st.multiselect("", 
                                     ["Science", "Commerce", "Arts", "Humanities", "Law", "IT", "Engineering", "Business", "Medicine", "Social Sciences"])

# 5. Employment Status
st.subheader("5. What is your current employment status?")
employment_status = st.selectbox("", 
                                 ["Select Employment Status", "Student", "Intern", "Unemployed", "Employed", "Self-employed"], 
                                 index=0 if not st.session_state.form_submitted else None)

# 6. Professional Experience
st.subheader("6. How many years of professional experience do you have?")
years_of_experience = st.selectbox("", ["Select Experience", "0", "1-3", "3-7", "7-10", "10+"], index=0 if not st.session_state.form_submitted else None)

# 7. Monthly Earnings
st.subheader("7. Select your monthly earnings (in PKR):")
monthly_earnings = st.selectbox("", 
                                ["Select Earnings", "< 20,000 PKR", "20,000 - 50,000 PKR", "50,000 - 100,000 PKR", 
                                 "100,000 - 200,000 PKR", "200,000 - 500,000 PKR", "500,000+ PKR"], 
                                index=0 if not st.session_state.form_submitted else None)

# 8. Skills (Hard Skills)
st.subheader("8. Select your hard and soft skills:")

# Hard Skills (Checkboxes)
hard_skills = [
    "Programming (Python, Java, etc.)",
    "Web Development",
    "Data Science & Machine Learning",
    "Cloud Computing",
    "Software Development",
    "Project Management",
    "Design (UI/UX, Graphic Design)",
    "Marketing & Digital Marketing",
    "Accounting & Finance",
    "Human Resources (HR)",
    "Legal Knowledge & Practices",
    "Sales & Customer Support",
    "Content Creation (Writing, Blogging, etc.)"
]

hard_skill_checkboxes = st.multiselect("Select your hard skills:", hard_skills, key="hard_skills")

# Soft Skills (Checkboxes)
soft_skills = [
    "Leadership",
    "Communication",
    "Problem Solving",
    "Teamwork",
    "Time Management",
    "Adaptability",
    "Critical Thinking"
]

soft_skill_checkboxes = st.multiselect("Select your soft skills:", soft_skills, key="soft_skills")

# 9. Language Skills
st.subheader("9. What languages do you speak?")
languages = ['English', 'Urdu', 'Arabic', 'Chinese', 'French']
language_checkboxes = st.multiselect("Select your languages:", languages, key="languages")

# 10. Career Interests
st.subheader("10. What career fields are you most interested in?")

career_interests = st.multiselect(
    "", 
    ["Select Career Field", "Technology", "Business", "Healthcare", "Education", "Government", "Others"], 
    default=[], key="career_interests")

# Show a text box for "Other" if selected
if "Others" in career_interests:
    other_career = st.text_input("Please specify your career interests:", key="other_career")

# 11. Work Preferences
st.subheader("11. What type of work setup and schedule do you prefer?")

work_type = st.selectbox("What is your preferred work setup?", ["Select Work Type", "Remote", "On-site", "Hybrid"], index=0 if not st.session_state.form_submitted else None)
work_schedule = st.selectbox("What type of work schedule do you prefer?", 
                             ["Select Schedule", "Full-time", "Part-time", "Freelance", "Contract"], index=0 if not st.session_state.form_submitted else None)

# 12. Future Aspirations (Now Always Visible)
st.subheader("12. What are your future aspirations?")
future_aspirations = st.text_input("Please specify your future aspirations:", key="future_aspirations")

# Submit button to save responses
submit_button = st.button("Submit")

# Handling the form submission
if submit_button:
    # Save responses to the database
    c.execute('''
        INSERT INTO user_responses (
            age_group, marital_status, dependants, education_level, fields_of_study, 
            employment_status, years_of_experience, monthly_earnings, hard_skills, 
            soft_skills, languages, career_interests, other_career, work_type, 
            work_schedule, future_aspirations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        age_group, marital_status, dependants, education_level, ",".join(fields_of_study),
        employment_status, years_of_experience, monthly_earnings, ",".join(hard_skill_checkboxes),
        ",".join(soft_skill_checkboxes), ",".join(language_checkboxes), ",".join(career_interests),
        other_career if "Others" in career_interests else None, work_type, work_schedule, future_aspirations
    ))

    # Commit and close the database connection
    conn.commit()

    # Generate Recommendations using the FLAN-T5 pipeline
    user_input = f"Age Group: {age_group}, Marital Status: {marital_status}, Education: {education_level}, Employment: {employment_status}, Career Interests: {', '.join(career_interests)}"
    
    # Generate recommendation
    recommendation = pipe(user_input)[0]['generated_text']
    
    # Show the recommendations
    st.subheader("Recommendations")
    st.write(recommendation)

    st.session_state.form_submitted = True
    st.balloons()

# PDF generation function
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="User Responses and Career Recommendations", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=user_input)
    pdf.multi_cell(0, 10, txt=f"Recommendation: {recommendation}")
    pdf.output("user_recommendations.pdf")

if submit_button:
    generate_pdf()
