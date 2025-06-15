import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from indeed_to_sheet import scrape_indeed_jobs, add_cover_letters_to_sheet

# Google Sheets setup
SHEET_NAME = "indeed_jobs"
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

st.set_page_config(page_title="Indeed Job Scraper", layout="centered")
st.title("📄 Indeed Job Scraper + AI Cover Letter")

# Input field
search_query = st.text_input("🔍 Enter Job Title or Keywords", "data engineer junior")
start_btn = st.button("🚀 Start Scraping and Generate Cover Letters")

if start_btn:
    with st.spinner("Scraping Indeed and generating AI cover letters..."):
        scrape_indeed_jobs(search_query)  # Uses hardcoded sheet name and client inside
        sheet = client.open(SHEET_NAME).sheet1
        add_cover_letters_to_sheet(sheet)
    st.success("✅ Done! Check your Google Sheet.")
    st.markdown(f"[🔗 Open your Google Sheet](https://docs.google.com/spreadsheets/d/{sheet.spreadsheet.id})", unsafe_allow_html=True)
