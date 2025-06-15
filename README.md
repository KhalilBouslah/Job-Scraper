# Job-Scraper
This project is a powerful automation tool that scrapes job listings from **Indeed**, stores them in **Google Sheets**, and generates **personalized AI cover letters** using the **Meta LLaMA 3** model via the **OpenRouter API**. It also includes a **Streamlit web app** to launch everything with a single click.


---

## 🚀 Features

✅ Scrapes live job data from [Indeed France](https://fr.indeed.com)  
✅ Extracts title, company, location, description, job type, and job link  
✅ Automatically stores results in a Google Sheet  
✅ Generates professional, AI-powered cover letters for each job using LLaMA 3  
✅ User-friendly UI built with Streamlit  
✅ Google Sheet auto-created and shared with your email  
✅ Rate-limited to avoid IP bans or API abuse

---

## 🛠️ Tech Stack

- **Python**
- **SeleniumBase** & **BeautifulSoup** – Job scraping & dynamic content parsing
- **gspread** & **Google Sheets API** – Data storage
- **OpenRouter API (Meta LLaMA 3)** – AI cover letter generation
- **Streamlit** – Frontend interface
- **OAuth2** – Secure access to Google Sheets

---

## 🧪 How It Works

1. **Enter a job title** in the Streamlit app (e.g., "data engineer junior")
2. The scraper fetches the first-page jobs from Indeed.
3. It extracts all job details and stores them in a Google Sheet.
4. Each job gets a tailored cover letter using a prompt sent to OpenRouter’s LLaMA 3 model.
5. You can access and edit your personalized job applications directly in Google Sheets!

---

## 🖼️ Demo

![Streamlit Screenshot](https://github.com/KhalilBouslah/Job-Scraper/blob/main/Screenshots/streamlit_job.png)

---

## 📦 Installation

### 1. Clone the Repo
    git clone https://github.com/KhalilBouslah/Job-Scraper-ai.git
    cd Job-Scraper-ai.git
### 2. install requirements  

    pip install -r requirements.txt
    
### 3. Set Up Google Sheets API

    Go to Google Developers Console

    Enable Google Sheets API and Google Drive API

    Create a Service Account and download the credentials.json

    Share your sheet with the service account email

### 4. Configure Your API Key

    Replace the placeholder in the script:
    
    OPENROUTER_API_KEY = "sk-or-your-api-key"
    
    Get yours from: https://openrouter.ai

    
### 3. run app 
    python run streamlit_app.py 






### 📬 Contact: khalilbouslah@gmail.com

    
