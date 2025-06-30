import streamlit as st
import pandas as pd
from datetime import date, timedelta
import uuid # For generating unique IDs
import spacy # For NLP capabilities

# --- Session State Initialization ---
# Initialize core data structures in Streamlit's session state.
# This data will persist as long as the user's browser session is active.
if 'people' not in st.session_state:
    st.session_state.people = [] # List to store Person objects
    # Example initial data (optional, for demonstration)
    st.session_state.people.append({
        "id": str(uuid.uuid4()),
        "name": "Daniel Sundheim",
        "current_title": "Founder & Chief Investment Officer",
        "current_company_name": "D1 Capital Partners L.P.",
        "email": "dan@d1capital.com",
        "linkedin_profile_url": "https://linkedin.com/in/danielsundheim",
        "reference_list_url": "#"
    })
    st.session_state.people.append({
        "id": str(uuid.uuid4()),
        "name": "Matthew Markovics",
        "current_title": "Partner",
        "current_company_name": "Durable Capital Partners LP",
        "email": "",
        "linkedin_profile_url": "",
        "reference_list_url": ""
    })
    st.session_state.people.append({
        "id": str(uuid.uuid4()),
        "name": "Elizabeth Wahab",
        "current_title": "Investment Analyst",
        "current_company_name": "B Capital",
        "email": "",
        "linkedin_profile_url": "",
        "reference_list_url": ""
    })


if 'employments' not in st.session_state:
    st.session_state.employments = [] # List to store Employment objects
    # Map names to IDs for initial employment data
    daniel_id = next((p['id'] for p in st.session_state.people if p['name'] == "Daniel Sundheim"), None)
    matthew_id = next((p['id'] for p in st.session_state.people if p['name'] == "Matthew Markovics"), None)
    elizabeth_id = next((p['id'] for p in st.session_state.people if p['name'] == "Elizabeth Wahab"), None)

    if daniel_id:
        st.session_state.employments.extend([
            {"id": str(uuid.uuid4()), "person_id": daniel_id, "company_name": "D1 Capital Partners L.P.", "title": "Founder & Chief Investment Officer", "start_date": date(2018, 1, 1), "end_date": None},
            {"id": str(uuid.uuid4()), "person_id": daniel_id, "company_name": "Viking Global Investors", "title": "Portfolio Manager", "start_date": date(2002, 1, 1), "end_date": date(2017, 12, 31)}
        ])
    if matthew_id:
        st.session_state.employments.extend([
            {"id": str(uuid.uuid4()), "person_id": matthew_id, "company_name": "Durable Capital Partners LP", "title": "Partner", "start_date": date(2020, 1, 1), "end_date": None},
            {"id": str(uuid.uuid4()), "person_id": matthew_id, "company_name": "Viking Global Investors", "title": "Analyst", "start_date": date(2015, 6, 1), "end_date": date(2019, 12, 31)}
        ])
    if elizabeth_id:
        st.session_state.employments.extend([
            {"id": str(uuid.uuid4()), "person_id": elizabeth_id, "company_name": "B Capital", "title": "Associate", "start_date": date(2023, 3, 1), "end_date": None},
            {"id": str(uuid.uuid4()), "person_id": elizabeth_id, "company_name": "Viking Global Investors", "title": "Analyst", "start_date": date(2018, 1, 1), "end_date": date(2022, 12, 31)}
        ])
    # Add more shared history data for other people if needed to match the image
    # For now, let's assume some data for the "Viking Global Investors" overlap example
    st.session_state.people.extend([
        {"id": str(uuid.uuid4()), "name": "Vivek M", "current_title": "Unknown", "current_company_name": "Shearlink Capital", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Melissa Livingston", "current_title": "Unknown", "current_company_name": "Tfg Asset Management", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Theodore Gleser", "current_title": "Unknown", "current_company_name": "D1 Capital Partners L.P.", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Aaron Gelband", "current_title": "Unknown", "current_company_name": "Warren Street Capital LLC", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "David Schwartz", "current_title": "Unknown", "current_company_name": "Elmwood Asset Management", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Arnau Porto", "current_title": "Unknown", "current_company_name": "F&W Networks", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Yu Liu", "current_title": "Unknown", "current_company_name": "Kings Court Capital", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Hannah Clark", "current_title": "Unknown", "current_company_name": "American Express", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Deanna Wagner", "current_title": "Unknown", "current_company_name": "J. Goldman & CO, L.P.", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Jeff Eberwein", "current_title": "Unknown", "current_company_name": "Hudson Global", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Grant Wonders", "current_title": "Unknown", "current_company_name": "Voyager", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
        {"id": str(uuid.uuid4()), "name": "Adrienne Mcateer-Santiago", "current_title": "Unknown", "current_company_name": "Viking Global Investors", "email": "", "linkedin_profile_url": "", "reference_list_url": ""},
    ])

    # Add shared employments for the new people at Viking Global Investors
    viking_id = "Viking Global Investors" # Using company name as a pseudo-ID for simplicity
    for person_data in st.session_state.people:
        if person_data['name'] in ["Vivek M", "Melissa Livingston", "Theodore Gleser", "Aaron Gelband",
                                   "David Schwartz", "Arnau Porto", "Yu Liu", "Hannah Clark",
                                   "Deanna Wagner", "Jeff Eberwein", "Grant Wonders", "Adrienne Mcateer-Santiago"]:
            start_year = 2010 + hash(person_data['name']) % 5 # Randomize start year a bit
            end_year = start_year + 3 + hash(person_data['name']) % 3 # Randomize duration
            st.session_state.employments.append({
                "id": str(uuid.uuid4()),
                "person_id": person_data['id'],
                "company_name": "Viking Global Investors",
                "title": "Analyst" if person_data['name'] != "Adrienne Mcateer-Santiago" else "Director",
                "start_date": date(start_year, 1, 1),
                "end_date": date(end_year, 12, 31) if end_year < 2025 else None
            })

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'list' # 'list' or 'details'
if 'selected_person_id' not in st.session_state:
    st.session_state.selected_person_id = None

# --- SpaCy Model Loading ---
@st.cache_resource
def load_spacy_model():
    """Loads the English SpaCy NLP model, cached for efficiency."""
    try:
        nlp_model = spacy.load("en_core_web_sm")
        return nlp_model
    except OSError:
        st.error("SpaCy model 'en_core_web_sm' not found. Please install it by running:")
        st.code("pip install spacy && python -m spacy download en_core_web_sm")
        st.stop()

nlp = load_spacy_model()

# --- Helper Functions for Data Management ---

def calculate_overlap_years(start1, end1, start2, end2):
    """
    Calculates the overlapping years between two date ranges.
    Treats None as 'present' (up to current date).
    """
    today = date.today()
    period1_end = end1 if end1 is not None else today
    period2_end = end2 if end2 is not None else today

    # Find the later of the two start dates
    latest_start = max(start1, start2)
    # Find the earlier of the two end dates
    earliest_end = min(period1_end, period2_end)

    overlap_days = (earliest_end - latest_start).days
    if overlap_days <= 0:
        return 0.0 # No overlap or invalid overlap
    return round(overlap_days / 365.25, 2) # Account for leap years

def get_person_by_id(person_id):
    """Retrieves a person dictionary by their ID."""
    return next((p for p in st.session_state.people if p['id'] == person_id), None)

def get_employments_by_person_id(person_id):
    """Retrieves a list of employment dictionaries for a given person ID."""
    return [e for e in st.session_state.employments if e['person_id'] == person_id]

def get_all_companies():
    """Returns a set of all unique company names from employment history."""
    return set(e['company_name'] for e in st.session_state.employments)

def go_to_details(person_id):
    """Sets the session state to view details of a specific person."""
    st.session_state.selected_person_id = person_id
    st.session_state.current_view = 'details'

def go_to_list():
    """Sets the session state back to the main list view."""
    st.session_state.selected_person_id = None
    st.session_state.current_view = 'list'

# --- UI Functions ---

def display_person_list():
    """Displays the main list of all people in the system."""
    st.header("All Professional Profiles")

    if not st.session_state.people:
        st.info("No professional profiles added yet. Use the form below to add one!")
        return

    # Prepare data for display
    people_data = []
    for person in st.session_state.people:
        people_data.append({
            "Name": person['name'],
            "Current Title": person['current_title'],
            "Current Company": person['current_company_name'],
            "ID": person['id'] # Hidden ID for internal use
        })

    df_people = pd.DataFrame(people_data)
    df_display = df_people.drop(columns=["ID"]) # Don't show ID in the main table

    st.dataframe(df_display, use_container_width=True)

    st.markdown("---")
    st.subheader("View Profile Details")
    # Create buttons for each person to view their details
    cols = st.columns(5) # Adjust columns for better layout
    for i, person in enumerate(st.session_state.people):
        with cols[i % 5]: # Distribute buttons across columns
            if st.button(f"View {person['name']}", key=f"view_{person['id']}"):
                go_to_details(person['id'])
                st.rerun()

def display_person_details(person_id):
    """Displays detailed information for a selected person."""
    person = get_person_by_id(person_id)
    if not person:
        st.error("Person not found.")
        go_to_list()
        st.rerun()
        return

    st.header(f"Employee Details: {person['name']}")
    st.markdown(f"**Current Role:** {person['current_title']} at {person['current_company_name']}")
    if person['email']:
        st.markdown(f"**Email:** [{person['email']}](mailto:{person['email']})")
    if person['linkedin_profile_url']:
        st.markdown(f"**LinkedIn Profile:** [Link]({person['linkedin_profile_url']})")
    if person['reference_list_url']:
        st.markdown(f"**Reference List:** [Link]({person['reference_list_url']})")

    st.markdown("---")
    st.subheader("Employment History")
    employments = get_employments_by_person_id(person_id)
    if employments:
        emp_data = []
        for emp in employments:
            emp_data.append({
                "Company": emp['company_name'],
                "Title": emp['title'],
                "Start Date": emp['start_date'].strftime("%Y-%m-%d"),
                "End Date": emp['end_date'].strftime("%Y-%m-%d") if emp['end_date'] else "Present"
            })
        df_employments = pd.DataFrame(emp_data)
        st.dataframe(df_employments, use_container_width=True)
    else:
        st.info("No employment history recorded for this person yet.")

    # --- Add New Employment Form ---
    st.markdown("---")
    st.subheader(f"Add New Employment for {person['name']}")
    with st.form(key="add_employment_form", clear_on_submit=True):
        new_company_name = st.text_input("Company Name*", key="new_emp_company")
        new_title = st.text_input("Title*", key="new_emp_title")
        new_start_date = st.date_input("Start Date*", value=date.today() - timedelta(days=365), key="new_emp_start")
        new_end_date = st.date_input("End Date (optional, leave blank for present)", value=None, key="new_emp_end", help="Set to today if still employed")
        
        submitted_emp = st.form_submit_button("Add Employment")
        if submitted_emp:
            if new_company_name and new_title and new_start_date:
                # Basic validation: End date should not be before start date if both are provided
                if new_end_date and new_end_date < new_start_date:
                    st.error("End Date cannot be before Start Date.")
                else:
                    st.session_state.employments.append({
                        "id": str(uuid.uuid4()),
                        "person_id": person_id,
                        "company_name": new_company_name,
                        "title": new_title,
                        "start_date": new_start_date,
                        "end_date": new_end_date
                    })
                    # Update current company/title if this is the most recent employment
                    if not new_end_date or new_end_date >= date.today():
                        person['current_company_name'] = new_company_name
                        person['current_title'] = new_title
                    st.success("Employment added successfully!")
                    st.rerun() # Rerun to update the display

            else:
                st.error("Please fill in Company Name, Title, and Start Date.")


    # --- Shared Work History ---
    st.markdown("---")
    st.subheader("Shared Work History")

    # This is the core logic for the "Shared Work History" section
    shared_history_data = []
    
    # Get all employments for the selected person
    selected_person_employments = get_employments_by_person_id(person_id)

    # Iterate through all other people
    for other_person in st.session_state.people:
        if other_person['id'] == person_id:
            continue # Skip the selected person themselves

        other_person_employments = get_employments_by_person_id(other_person['id'])
        
        # Find common companies
        for selected_emp in selected_person_employments:
            for other_emp in other_person_employments:
                if selected_emp['company_name'] == other_emp['company_name']:
                    overlap = calculate_overlap_years(
                        selected_emp['start_date'], selected_emp['end_date'],
                        other_emp['start_date'], other_emp['end_date']
                    )
                    if overlap > 0:
                        shared_history_data.append({
                            "Full Name": other_person['name'],
                            "Contact": "📞🔗", # Placeholder for contact icons (as per image)
                            "Overlap Company": selected_emp['company_name'],
                            "Current Company": other_person['current_company_name'],
                            "Overlap Years": overlap
                        })
    
    if shared_history_data:
        # Remove duplicates if any (e.g., if two people worked at the same company multiple times with overlap)
        # Using a tuple of key fields for uniqueness
        unique_shared_history = []
        seen = set()
        for entry in shared_history_data:
            key = (entry["Full Name"], entry["Overlap Company"])
            if key not in seen:
                unique_shared_history.append(entry)
                seen.add(key)
        
        # Sort by Overlap Years descending for better visibility
        df_shared_history = pd.DataFrame(unique_shared_history).sort_values(by="Overlap Years", ascending=False)
        
        st.dataframe(df_shared_history, use_container_width=True)
    else:
        st.info("No shared work history found with other professionals in the system.")


    st.markdown("---")
    if st.button("← Back to All Profiles"):
        go_to_list()
        st.rerun()

# --- Main Application Logic ---
st.sidebar.title("Navigation")
if st.sidebar.button("All Profiles", key="nav_all_profiles"):
    go_to_list()
    st.rerun()

if st.session_state.current_view == 'list':
    display_person_list()
    
    st.markdown("---")
    st.header("Add New Professional Profile")
    with st.form(key="add_person_form", clear_on_submit=True):
        st.subheader("Personal Details")
        person_name = st.text_input("Full Name*", key="person_name_input")
        current_title = st.text_input("Current Title (e.g., Founder & CIO)", key="current_title_input")
        current_company = st.text_input("Current Company Name (e.g., D1 Capital Partners L.P.)", key="current_company_input")
        email = st.text_input("Email (optional)", key="email_input")
        linkedin_url = st.text_input("LinkedIn Profile URL (optional)", key="linkedin_url_input")
        reference_url = st.text_input("Reference List URL (optional)", key="reference_url_input")

        st.subheader("Initial Employment Details (for current role)")
        # These fields are required for initial employment
        initial_company_name = st.text_input("Company Name for Initial Employment*", value=current_company, key="initial_comp_input")
        initial_title = st.text_input("Title for Initial Employment*", value=current_title, key="initial_title_input")
        initial_start_date = st.date_input("Start Date for Initial Employment*", value=date.today() - timedelta(days=365), key="initial_start_date_input")
        initial_end_date = st.date_input("End Date for Initial Employment (optional, leave blank for present)", value=None, key="initial_end_date_input")


        submitted_person = st.form_submit_button("Add Profile")
        if submitted_person:
            if person_name and current_title and current_company and initial_company_name and initial_title and initial_start_date:
                # Basic validation: End date should not be before start date if both are provided
                if initial_end_date and initial_end_date < initial_start_date:
                    st.error("Initial Employment: End Date cannot be before Start Date.")
                else:
                    new_person_id = str(uuid.uuid4())
                    st.session_state.people.append({
                        "id": new_person_id,
                        "name": person_name,
                        "current_title": current_title,
                        "current_company_name": current_company,
                        "email": email,
                        "linkedin_profile_url": linkedin_url,
                        "reference_list_url": reference_url
                    })
                    st.session_state.employments.append({
                        "id": str(uuid.uuid4()),
                        "person_id": new_person_id,
                        "company_name": initial_company_name,
                        "title": initial_title,
                        "start_date": initial_start_date,
                        "end_date": initial_end_date
                    })
                    st.success(f"Profile for {person_name} added successfully!")
                    st.rerun() # Rerun to update the person list
            else:
                st.error("Please fill in all required fields (Full Name, Current Title, Current Company, Initial Employment details).")

elif st.session_state.current_view == 'details' and st.session_state.selected_person_id:
    display_person_details(st.session_state.selected_person_id)

# --- NLP Integration (Optional: For future "parsing" from newsletters, not directly for OWL system) ---
st.sidebar.markdown("---")
st.sidebar.subheader("NLP for Newsletter (Separate Feature)")
uploaded_file = st.sidebar.file_uploader("Upload Newsletter .txt for NLP suggestions (Doesn't add to OWL data)", type="txt")

if uploaded_file is not None:
    file_contents = uploaded_file.read().decode("utf-8", errors="ignore")
    doc = nlp(file_contents)
    person_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])))
    org_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"])))

    st.sidebar.markdown("**Suggested Names:**")
    if person_names:
        st.sidebar.write(", ".join(person_names))
    else:
        st.sidebar.write("No names found.")

    st.sidebar.markdown("**Suggested Organizations:**")
    if org_names:
        st.sidebar.write(", ".join(org_names))
    else:
        st.sidebar.write("No organizations found.")
    st.sidebar.info("These are just suggestions from the newsletter. Add them manually to the system via the forms.")


# --- Export Data to CSV ---
st.sidebar.markdown("---")
st.sidebar.subheader("Export Data")

if st.session_state.people:
    df_export_people = pd.DataFrame([p for p in st.session_state.people])
    df_export_people['email'] = df_export_people['email'].apply(lambda x: x if x else '')
    df_export_people['linkedin_profile_url'] = df_export_people['linkedin_profile_url'].apply(lambda x: x if x else '')
    df_export_people['reference_list_url'] = df_export_people['reference_list_url'].apply(lambda x: x if x else '')
    csv_people = df_export_people.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download All People Data (CSV)",
        data=csv_people,
        file_name="professional_profiles.csv",
        mime="text/csv",
        help="Downloads all professional profiles data."
    )

if st.session_state.employments:
    df_export_employments = pd.DataFrame([
        {
            "person_id": e['person_id'],
            "company_name": e['company_name'],
            "title": e['title'],
            "start_date": e['start_date'].strftime("%Y-%m-%d"),
            "end_date": e['end_date'].strftime("%Y-%m-%d") if e['end_date'] else "Present"
        }
        for e in st.session_state.employments
    ])
    csv_employments = df_export_employments.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download All Employment History (CSV)",
        data=csv_employments,
        file_name="employment_history.csv",
        mime="text/csv",
        help="Downloads all employment history data."
    )

st.sidebar.markdown("---")
st.sidebar.info("Data is stored in-memory for the session. It will reset if the app restarts.")

