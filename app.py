# Import necessary libraries
import streamlit as st
import pandas as pd
import io
import spacy

# --- SpaCy Model Loading ---
# @st.cache_resource decorates functions that return a global resource that you want to share across reruns and users.
# This ensures the SpaCy model is loaded only once across the application's lifecycle,
# significantly improving performance by avoiding redundant loading.
@st.cache_resource
def load_spacy_model():
    """
    Loads the English SpaCy NLP model.
    This function is cached to ensure the model is loaded only once.
    """
    try:
        # Attempt to load the small English model
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        # If the model is not found, inform the user and stop the Streamlit app.
        st.error("SpaCy model 'en_core_web_sm' not found. Please install it by running:")
        st.code("python -m spacy download en_core_web_sm")
        st.stop() # Stop the app if the model isn't available, as it's a critical dependency.

# Load the NLP model
nlp = load_spacy_model()

# --- Streamlit App Configuration ---
# Sets the page layout to 'wide' to make better use of screen real estate
# and sets the page title for the browser tab.
st.set_page_config(layout="wide", page_title="Newsletter Data Extractor")

# --- Application Title and Description ---
st.title("Newsletter Information Dashboard 📰")
st.markdown("Upload your newsletter text file, get NLP-driven suggestions for Names and Firms, and then manually input other relevant LinkedIn-style information. View the data in a table and download it as a CSV.")

# --- Session State Initialization ---
# Streamlit's session state is used to persist data across reruns of the app.
# Initialize lists and dictionaries in session state if they don't already exist.
if 'data_entries' not in st.session_state:
    st.session_state.data_entries = [] # Stores all the manually entered data rows.
if 'extracted_text_content' not in st.session_state:
    st.session_state.extracted_text_content = "" # Stores the content of the last uploaded file.
if 'nlp_suggestions' not in st.session_state:
    # Stores NLP-extracted PERSON and ORG entities as suggestions.
    st.session_state.nlp_suggestions = {"PERSON": [], "ORG": []}

# --- File Uploader Section ---
st.header("1. Upload Newsletter File")
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
    # Read file contents. Using errors="ignore" to handle potential encoding issues gracefully.
    file_contents = uploaded_file.read().decode("utf-8", errors="ignore")
    st.session_state.extracted_text_content = file_contents # Store content in session state.

    st.write(f"File uploaded: {uploaded_file.name}")
    st.info("File content loaded. See NLP suggestions below for Names and Firms.")

    # Process content with SpaCy for Named Entity Recognition (NER).
    # This happens only when a new file is uploaded.
    doc = nlp(st.session_state.extracted_text_content)

    # Extract PERSON (people names) and ORG (organization names) entities.
    # Convert to a set to get unique names, then back to a sorted list.
    person_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])))
    org_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"])))

    # Store extracted entities in session state.
    st.session_state.nlp_suggestions["PERSON"] = person_names
    st.session_state.nlp_suggestions["ORG"] = org_names

    # Display content preview in an expandable section.
    with st.expander("Click to view raw newsletter content"):
        st.text_area("Content", st.session_state.extracted_text_content, height=200)

    # Display NLP Suggestions clearly to the user.
    st.subheader("NLP Suggestions from Uploaded File:")
    if st.session_state.nlp_suggestions["PERSON"]:
        st.markdown("**Suggested Names (PERSON entities):**")
        st.code(", ".join(st.session_state.nlp_suggestions["PERSON"]))
    else:
        st.info("No PERSON entities found in the uploaded text.")

    if st.session_state.nlp_suggestions["ORG"]:
        st.markdown("**Suggested Firms (ORG entities):**")
        st.code(", ".join(st.session_state.nlp_suggestions["ORG"]))
    else:
        st.info("No ORG entities found in the uploaded text.")

    st.warning("Copy and paste suggestions into the input form below. 'Movement' and 'Area/Role' still require manual entry.")
else:
    # If no file is uploaded, clear previously loaded content and suggestions from session state.
    st.session_state.extracted_text_content = ""
    st.session_state.nlp_suggestions = {"PERSON": [], "ORG": []}


# --- Data Input Form ---
st.header("2. Input Information")
st.markdown("Manually enter the details (you can copy from the NLP suggestions above).")

# Use a Streamlit form for input to handle submission and clear fields.
with st.form("info_input_form", clear_on_submit=True):
    # Pre-fill 'Name' and 'Firm Name' input fields if there's only one NLP suggestion,
    # otherwise leave them blank for the user to type or copy.
    initial_name = st.session_state.nlp_suggestions["PERSON"][0] if len(st.session_state.nlp_suggestions["PERSON"]) == 1 else ""
    initial_firm = st.session_state.nlp_suggestions["ORG"][0] if len(st.session_state.nlp_suggestions["ORG"]) == 1 else ""

    # Input fields for data entry.
    name = st.text_input("Name (e.g., John Doe)", value=initial_name)
    firm_name = st.text_input("Firm Name (e.g., ABC Capital)", value=initial_firm)
    movement = st.text_input("Movement (e.g., Appointed, Joined, Left, Promoted)")
    area = st.text_input("Area/Role (e.g., Head of Equities, Portfolio Manager, Analyst)")
    date = st.date_input("Date (e.g., Date of announcement/movement)", value="today") # Defaults to today's date.

    submitted = st.form_submit_button("Add Entry") # Button to submit the form.

    if submitted:
        # Validate that essential fields are not empty.
        if name and firm_name and movement and area:
            # Create a dictionary for the new data entry.
            new_entry = {
                "Name": name,
                "Firm Name": firm_name,
                "Movement": movement,
                "Area/Role": area,
                "Date": date.strftime("%Y-%m-%d") # Format date consistently as YYYY-MM-DD.
            }
            # Add the new entry to the list in session state.
            st.session_state.data_entries.append(new_entry)
            st.success("Entry added successfully!")
        else:
            st.error("Please fill in all required fields (Name, Firm Name, Movement, Area/Role).")

# --- Dashboard Display ---
st.header("3. Extracted Information Dashboard")

if st.session_state.data_entries:
    # Convert the list of dictionaries (data entries) into a Pandas DataFrame.
    df = pd.DataFrame(st.session_state.data_entries)

    # Display the DataFrame as an interactive table.
    st.dataframe(df, use_container_width=True)

    # --- CSV Download Button ---
    st.header("4. Download Data")
    st.markdown("Download the collected information as a CSV file.")

    # Use io.StringIO to create an in-memory text buffer for the CSV data.
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False) # Write DataFrame to the buffer without the Pandas index.
    csv_bytes = csv_buffer.getvalue().encode('utf-8') # Get the string value and encode to bytes.

    # Streamlit's download_button widget for downloading the CSV.
    st.download_button(
        label="Download Data as CSV",
        data=csv_bytes,
        file_name="linkedin_style_newsletter_data.csv",
        mime="text/csv",
        help="Click to download all current entries as a CSV file."
    )
else:
    st.info("No data entries yet. Upload a file and use the form above to add information.")

# --- Instructions/Disclaimer ---
st.markdown(
    """
    ---
    **Note on Automation:**
    This dashboard now uses Natural Language Processing (NLP) with `spaCy` to identify potential "Names" (PERSON entities) and "Firm Names" (ORG entities) from the uploaded text. These are provided as suggestions to streamline your manual data entry.

    Fully automating the extraction of "Movement" (e.g., "Appointed," "Joined," "Left") and "Area/Role" (e.g., "Head of Equities") from arbitrary news text is a complex NLP task. It typically requires:
    * **Contextual Analysis:** Understanding the relationship between entities and actions.
    * **Rule-Based Systems:** Defining intricate patterns for specific types of announcements.
    * **Machine Learning Models:** Training models on large datasets of similar text to recognize these patterns.

    For now, "Movement" and "Area/Role" remain manual inputs to ensure accuracy, leveraging the NLP for initial entity identification.
    """
)
