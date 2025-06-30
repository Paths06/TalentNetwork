# Import necessary libraries
import streamlit as st
import pandas as pd
import io
import spacy
from datetime import date # Import date for automatic entry dates

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
st.markdown("Upload your newsletter text file. NLP will automatically suggest Names and add them to the table for review. You can also manually add or refine entries. View the data in a table and download it as a CSV.")

# --- Session State Initialization ---
# Streamlit's session state is used to persist data across reruns of the app.
# Initialize lists and dictionaries in session state if they don't already exist.
if 'data_entries' not in st.session_state:
    st.session_state.data_entries = [] # Stores all the manually and automatically added data rows.
if 'extracted_text_content' not in st.session_state:
    st.session_state.extracted_text_content = "" # Stores the content of the last uploaded file.
if 'nlp_suggestions' not in st.session_state:
    # Stores NLP-extracted PERSON and ORG entities as suggestions (for display only now).
    st.session_state.nlp_suggestions = {"PERSON": [], "ORG": []}

# --- File Uploader Section ---
st.header("1. Upload Newsletter File")
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
    # Read file contents. Using errors="ignore" to handle potential encoding issues gracefully.
    file_contents = uploaded_file.read().decode("utf-8", errors="ignore")
    st.session_state.extracted_text_content = file_contents # Store content in session state.

    st.write(f"File uploaded: {uploaded_file.name}")
    st.info("File content loaded. NLP has processed the text and added suggested entries to the dashboard below.")

    # Process content with SpaCy for Named Entity Recognition (NER).
    # This happens only when a new file is uploaded.
    doc = nlp(st.session_state.extracted_text_content)

    # Extract PERSON (people names) and ORG (organization names) entities.
    person_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])))
    org_names = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"])))

    # Store extracted entities in session state for potential display/review.
    st.session_state.nlp_suggestions["PERSON"] = person_names
    st.session_state.nlp_suggestions["ORG"] = org_names

    # --- Automatically Add NLP-Detected Entries ---
    st.subheader("Automatically Added NLP Suggestions:")
    auto_added_count = 0
    current_date_str = date.today().strftime("%Y-%m-%d") # Get today's date for new entries

    # Add PERSON entities to the main data table
    for person_name in person_names:
        # Check for duplicates based on Name (simplistic to avoid repeated entries for the same person)
        is_duplicate = any(entry["Name"] == person_name for entry in st.session_state.data_entries)
        if not is_duplicate:
            new_entry = {
                "Name": person_name,
                "Firm Name": "NLP Suggestion (Review)", # Placeholder, user needs to refine
                "Movement": "NLP Detected (Review)",  # Placeholder, user needs to refine
                "Area/Role": "NLP Detected (Review)", # Placeholder, user needs to refine
                "Date": current_date_str
            }
            st.session_state.data_entries.append(new_entry)
            auto_added_count += 1
    
    # Optionally, add ORG entities as well, but this can lead to many generic entries.
    # For now, let's focus on PERSON as the primary "LinkedIn-like" entity.
    # If you want to also add ORGs as separate entries, uncomment and adapt this block:
    # for org_name in org_names:
    #     is_duplicate_org = any(entry["Firm Name"] == org_name for entry in st.session_state.data_entries)
    #     if not is_duplicate_org:
    #         new_entry = {
    #             "Name": "N/A (Firm Entity)", # Indicate it's a firm, not a person
    #             "Firm Name": org_name,
    #             "Movement": "NLP Detected (Firm)",
    #             "Area/Role": "N/A",
    #             "Date": current_date_str
    #         }
    #         st.session_state.data_entries.append(new_entry)
    #         auto_added_count += 1

    if auto_added_count > 0:
        st.success(f"Automatically added {auto_added_count} new entries from the uploaded file.")
        st.info("Please review these entries in the 'Extracted Information Dashboard' below and manually refine 'Firm Name', 'Movement', and 'Area/Role' as needed.")
    else:
        st.info("No new unique PERSON entities were detected or added from the uploaded file.")


    # Display raw content and NLP suggestions for manual reference
    with st.expander("Click to view raw newsletter content"):
        st.text_area("Content", st.session_state.extracted_text_content, height=200)

    st.markdown("**Original NLP Suggestions (for reference):**")
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


else:
    # If no file is uploaded, clear previously loaded content and suggestions from session state.
    st.session_state.extracted_text_content = ""
    st.session_state.nlp_suggestions = {"PERSON": [], "ORG": []}


# --- Data Input Form ---
st.header("2. Manually Add/Refine Information")
st.markdown("Use this form to add new entries or refine existing automatically detected ones. You can copy from the 'Original NLP Suggestions' above if helpful.")

# Create input fields for each piece of information
with st.form("info_input_form", clear_on_submit=True):
    name = st.text_input("Name (e.g., John Doe)")
    firm_name = st.text_input("Firm Name (e.g., ABC Capital)")
    movement = st.text_input("Movement (e.g., Appointed, Joined, Left, Promoted)")
    area = st.text_input("Area/Role (e.g., Head of Equities, Portfolio Manager, Analyst)")
    date_input = st.date_input("Date (e.g., Date of announcement/movement)", value="today") # Renamed to avoid conflict

    submitted = st.form_submit_button("Add/Update Entry") # Changed button text

    if submitted:
        # Validate that essential fields are not empty.
        if name and firm_name and movement and area:
            new_entry = {
                "Name": name,
                "Firm Name": firm_name,
                "Movement": movement,
                "Area/Role": area,
                "Date": date_input.strftime("%Y-%m-%d") # Format date consistently as YYYY-MM-DD.
            }

            # Check if this is an update to an existing entry (e.g., if a user refines an NLP-added entry)
            # This is a simple check; more robust update logic might be needed for complex scenarios.
            found_and_updated = False
            for i, entry in enumerate(st.session_state.data_entries):
                if entry["Name"] == name and entry["Firm Name"] == "NLP Suggestion (Review)":
                    # Simple update: if name matches and it's an NLP placeholder, update it.
                    st.session_state.data_entries[i] = new_entry
                    found_and_updated = True
                    st.success(f"Entry for '{name}' updated successfully!")
                    break

            if not found_and_updated:
                # If not an update, check if it's a completely new duplicate before adding
                is_duplicate_manual = any(
                    entry["Name"] == name and entry["Firm Name"] == firm_name
                    for entry in st.session_state.data_entries
                )
                if not is_duplicate_manual:
                    st.session_state.data_entries.append(new_entry)
                    st.success("New entry added successfully!")
                else:
                    st.warning("This exact entry (Name and Firm Name) already exists. No new entry added.")
        else:
            st.error("Please fill in all required fields (Name, Firm Name, Movement, Area/Role) for manual entry.")

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
    st.info("No data entries yet. Upload a file or use the form above to add information.")

# --- Instructions/Disclaimer ---
st.markdown(
    """
    ---
    **Note on Automation:**
    This dashboard now uses Natural Language Processing (NLP) with `spaCy` to automatically add suggested "Names" (PERSON entities) from the uploaded text directly to the table. For these auto-added entries, "Firm Name", "Movement", and "Area/Role" are set as "NLP Suggestion (Review)" or "NLP Detected (Review)".

    Fully automating the precise extraction of "Movement" (e.g., "Appointed," "Joined," "Left") and "Area/Role" (e.g., "Head of Equities"), along with accurately linking them to specific firms, from arbitrary news text is a complex NLP task. It typically requires:
    * **Contextual Analysis:** Understanding the relationship between entities and actions.
    * **Rule-Based Systems:** Defining intricate patterns for specific types of announcements.
    * **Machine Learning Models:** Training models on large datasets of similar text to recognize these patterns.

    For now, `Movement` and `Area/Role` (and detailed `Firm Name` for NLP entries) remain areas for manual refinement to ensure accuracy, leveraging the NLP for initial entity identification and population of your dashboard.
    """
)
