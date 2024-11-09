import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='streamlit')

import streamlit as st
import sqlite3

# --- Database setup ---
# Create or connect to an SQLite database
conn = sqlite3.connect('career_assistant.db')
c = conn.cursor()

# Create a table to store user responses if it doesn't already exist
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
        future_aspirations TEXT,
        other_future_career TEXT
    )
''')

# --- Streamlit App ---
# Title of the app
st.title("Your Academics & Career Assistant")

# Introduction
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
    index=0 if not st.session_state.form_submitted else None  # Use None when form is submitted
)

# 2. Marital Status & Dependants
st.subheader("2. What is your marital status?")
marital_status = st.selectbox("", 
                              ["Select Marital Status", "Single", "Married", "Divorced", "Widowed"], 
                              index=0 if not st.session_state.form_submitted else None)

# Disable dependants field if marital status is "Single"
dependants_disabled = False
if marital_status == "Single":
    dependants_disabled = True  # Disable the dependants field if the user is single

# Show dependants input only if marital status is not "Single"
if not dependants_disabled:
    dependants = st.number_input("How many dependants do you have?", min_value=0, max_value=10, step=1)
else:
    dependants = None  # No input if Single

# 3. Education Level
st.subheader("3. What is your highest level of education?")
education_level = st.selectbox("", 
                               ["Select Education Level", "High School", "Undergraduate", "Graduate", "Postgraduate", "PhD"], 
                               index=0 if not st.session_state.form_submitted else None)  # Default empty

# 4. Fields of Study based on Education Level
st.subheader("4. What is your field of study? (Select one or more)")

fields_of_study = []

# Conditional fields of study based on education level
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

# 6. Professional Experience (if employed or self-employed)
if employment_status in ["Employed", "Self-employed"]:
    st.subheader("6. How many years of professional experience do you have?")
    years_of_experience = st.selectbox("", ["Select Experience", "0", "1-2", "3-5", "5+"], index=0 if not st.session_state.form_submitted else None)

# 7. Monthly Earnings (moved here)
st.subheader("7. Select your monthly earnings (in PKR):")
monthly_earnings = st.selectbox("", 
                                ["Select Earnings", "< 20,000 PKR", "20,000 - 50,000 PKR", "50,000 - 100,000 PKR", 
                                 "100,000 - 200,000 PKR", "200,000 - 500,000 PKR", "500,000+ PKR"], 
                                index=0 if not st.session_state.form_submitted else None)

# 8. Skills (Hard Skills)
st.subheader("8. Select your hard and soft skills:")

# Hard Skills (Checkboxes Grid - diversified)
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

# Soft Skills (Checkboxes Grid)
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
                             ["Select Schedule", "Full-time", "Part-time", "Project-based", "Freelance", "Temporary"], 
                             index=0 if not st.session_state.form_submitted else None)

# 12. What do you want to be in future? (Career Aspirations)
st.subheader("12. What do you want to be in future? (Select one or more)")

future_aspirations = st.multiselect(
    "", 
    ["Businessman", "Bureaucrat", "Finance Professional", "Doctor", "IT Professional", 
     "Lawyer", "Engineer", "Pilot", "Other"], default=[], key="future_aspirations")

# Show a text box for "Other" if selected
if "Other" in future_aspirations:
    other_future_career = st.text_input("Please specify your future career aspirations:", key="other_future_career")

# Submit Button (Trigger form submission)
if st.button("Submit"):
    st.session_state.form_submitted = True

    # Store the responses in the database
    c.execute('''
        INSERT INTO user_responses (
            age_group, marital_status, dependants, education_level, fields_of_study, employment_status,
            years_of_experience, monthly_earnings, hard_skills, soft_skills, languages, career_interests,
            other_career, work_type, work_schedule, future_aspirations, other_future_career
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        age_group, marital_status, dependants, education_level, ', '.join(fields_of_study), employment_status,
        years_of_experience if employment_status in ["Employed", "Self-employed"] else None, monthly_earnings,
        ', '.join(hard_skill_checkboxes), ', '.join(soft_skill_checkboxes), ', '.join(language_checkboxes),
        ', '.join(career_interests), other_career if "Others" in career_interests else None,
        work_type, work_schedule, ', '.join(future_aspirations), other_future_career if "Other" in future_aspirations else None
    ))

    conn.commit()

    # Output user responses
    st.write(f"**Age Group**: {age_group}")
    st.write(f"**Marital Status**: {marital_status}")
    if not dependants_disabled:
        st.write(f"**Dependants**: {dependants}")
    st.write(f"**Education Level**: {education_level}")
    st.write(f"**Fields of Study**: {', '.join(fields_of_study)}")
    st.write(f"**Employment Status**: {employment_status}")
    
    if employment_status in ["Employed", "Self-employed"]:
        st.write(f"**Years of Experience**: {years_of_experience}")
    
    st.write(f"**Hard Skills**: {', '.join(hard_skill_checkboxes)}")
    st.write(f"**Soft Skills**: {', '.join(soft_skill_checkboxes)}")
    st.write(f"**Languages**: {', '.join(language_checkboxes)}")
    st.write(f"**Career Interests**: {', '.join(career_interests)}")
    if "Others" in career_interests:
        st.write(f"**Other Career Interests**: {other_career}")
    st.write(f"**Work Type**: {work_type}")
    st.write(f"**Work Schedule**: {work_schedule}")
    st.write(f"**Future Aspirations**: {', '.join(future_aspirations)}")
    if "Other" in future_aspirations:
        st.write(f"**Other Future Career**: {other_future_career}")

# Close the database connection
conn.close()
