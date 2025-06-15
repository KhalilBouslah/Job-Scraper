from seleniumbase import Driver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import re
import regex
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import requests
from time import sleep

# Define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Sheet name
SHEET_NAME = "indeed_jobs"
SHARE_EMAIL = "user@example.com"


# --- CONFIG ---
OPENROUTER_API_KEY = "you_api_key"  # Replace with your key
MODEL = "meta-llama/llama-3-8b-instruct"

def generate_description_openrouter(title,Entreprise,description):
    prompt = (
        f">You are an expert resume and cover letter writer, write a professional cover letter to apply for the following role:\n\n"
        f"Job Title: {title}\n"
        f"Company: {Entreprise}\n"
        f"Summary: {description}\n"
    )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()['choices'][0]['message']['content']
    else:
        return f"Error from LLM: {res.text}"


def add_cover_letters_to_sheet(sheet):
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):  # Skip header (start from row 2)
        title = row["title"]
        description = row["description"]
        Entreprise= row['Entreprise']
        cover_letter = generate_description_openrouter(title,Entreprise, description)

        cell_range = f"G{i}"
        sheet.update(cell_range, [[cover_letter]])
        print(f"✅ Row {i} updated with cover letter.")
        sleep(5)  # Optional delay to avoid flooding the local model


def scrape_indeed_jobs(search_query: str) -> pd.DataFrame:
    # Encode search query for URL
    encoded_query = quote_plus(search_query)
    url = f"https://fr.indeed.com/jobs?q={encoded_query}"
    
    # Set up Selenium
    driver = Driver(uc=True)
    driver.maximize_window()
    driver.get(url)


    # Let the page load
    time.sleep(30)

    # Get HTML after JavaScript has rendered
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.execute_script("window.scrollBy(0, 1000);")
    sh = client.create(SHEET_NAME)
    sh.share(SHARE_EMAIL, perm_type='user', role='writer')
    sheet = sh.sheet1

    # Step 4: Set headers
    headers = ["title", "Entreprise","link", "description", "location", "job_type", "cover_letter"]
    sheet.insert_row(headers, index=1)

    print("✅ Headers created successfully in Google Sheet.")
    row=2
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for block in soup.find_all('li', class_='css-1ac2h1w eu4oa1w0'):
            Entreprise_tag = block.find('div', class_='css-1afmp4o e37uo190')
            if Entreprise_tag:
                Entreprise = Entreprise_tag.text.strip()
            a_tag = block.find('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag.get('href')
                if link.startswith('/'):
                    link = "https://fr.indeed.com" + link

                #Open new page (Description of each card)
                driver.execute_script('window.open("")')
                driver.switch_to_window(driver.window_handles[1])
                driver.get(link)
                time.sleep(5)


                description = 'No description found'
                location = 'No location found'
                job_type = 'No type found'
                
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    for block in soup.find_all('div', class_='css-r6t43x eu4oa1w0'):
                        desc_tag = block.find('div', class_='jobsearch-JobComponent-description css-1rybqxq eu4oa1w0')
                        loc_tag = block.find('div', class_='css-fa4tq9 eu4oa1w0')
                        type_tag = block.find('div', class_='js-match-insights-provider-y9j299 eu4oa1w0')
                        if desc_tag:
                            description = desc_tag.text.strip()
                        if loc_tag:
                            location = loc_tag.text.strip()
                        if type_tag:
                            job_type = type_tag.text.strip()
                except Exception as e:
                    print(f"Error while extracting details from {link}: {e}")

                # Return to main tab and close current tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                print(f"Title:{title}\n Entreprise:{Entreprise}\n link: {link} \n Description: {description} \n type:{job_type}")
                
                row_values=[title,Entreprise,link,description,location,job_type]
                range_to_update="A{0}:G{0}".format(row)
                
                
                sheet.update(range_to_update,[row_values])
                row+=1
                

        break

    driver.quit()
