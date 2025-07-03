# OpenTable-Sentiment-Analysis
Skills: Web Scrapping, Prompt Engineering, Streamlit, Matplotlib

# 🍽️ Restaurant Review Analyzer

**Restaurant Review Analyzer** is a multi-page Streamlit web app that scrapes and analyzes restaurant reviews from **OpenTable**. It uses the **Groq LLM API** to extract structured insights about food and staff quality from customer feedback.

---

## 🧠 Key Features

- 🔍 **Review Dashboard**:  
  Scrape reviews of a single restaurant, separate comments on food and staff and analyze sentiment on food and staff.
  
- 📊 **Competitor Analysis**:  
  Compare average ratings between two restaurants using visual graphs.

- 🎯 **LLM-Based Analysis**:  
  Uses structured prompts and LLM output to categorize review content.

- 🧾 **Export**:  
  Saves analysis results as `.json` and competitor comparison as `.jpg`.

---

## 🗂️ Project Structure

restaurant-review-analyzer/
|
|-- Dashboard.py # Landing page with sidebar navigation
|-- pages
    |-- 1_Reviews_Dashboard.py # Single restaurant review dashboard
    |-- 2_Competitor_Analysis_Dashboard.py # Compare two restaurants
|-- util.py # Core logic: scraping, prompting, formatting
|-- requirements.txt # (You generate this using pip freeze)
|-- LICENSE
|-- README.md # Project instructions (you are here)

---

## ⚙️ Setup Instructions

### 🔁 1. Clone the Repository

git clone https://github.com/RJ601/OpenTable-Sentiment-Analysis.git

cd OpenTable-Sentiment-Analysis

🧪 2. Create a Virtual Environment (optional but recommended)
python -m venv env

source env/bin/activate  # On Windows: env\Scripts\activate

📦 3. Install Dependencies
Install the required packages using:

pip install -r requirements.txt

🔑 4. Set Up Groq API Key
Login & setup your API key from here (https://console.groq.com/keys)

In the file util.py, find this line:
os.environ['GROQ_API_KEY'] = 'your_api_key_here'
Replace 'your_api_key_here' with your actual Groq API key.

⚙️ 5. Optional Configuration
In util.py, you may also edit:
def scrape_reviews(url, start=1, pages=10):
To change how many pages of reviews you want to scrape.

▶️ Running the App
Run the Streamlit app from the terminal:
streamlit run Dashboard.py
You’ll see a sidebar with the following options:

Reviews Dashboard: Analyze one restaurant.
Competitor Analysis Dashboard: Compare two restaurants.

![Main_Dashboard](https://github.com/user-attachments/assets/d64e6af3-fbcf-4ca0-804f-2deb332df196)

🖼️ Output
The Reviews Dashboard will save a .json file with categorized review data and would display the colour-coded reviews on the streamlit dashboard.
![Reviews_Dashbard_Form](https://github.com/user-attachments/assets/ade8d04b-9f7b-4325-9afc-9ab7c5c3180b)
![image](https://github.com/user-attachments/assets/136a2d08-1db1-4e4b-a938-6a1b3a39e594)
![Reviews_Dashbard](https://github.com/user-attachments/assets/70355e55-3068-424c-9b61-91e296ee85fc)
![Reviews_Dashbard_2](https://github.com/user-attachments/assets/1706cbb3-bef6-4a52-9655-f94c22f25e03)

The Competitor Analysis page will generate a .jpg line chart comparing average ratings over time.
![Competitor_Analysis_Dashbard_Form](https://github.com/user-attachments/assets/c6738381-c1c0-49a7-9587-5e2524ef9478)
![Competitor_Analysis_Output_Image](https://github.com/user-attachments/assets/0cd2e8f9-0757-427f-a613-3c95ca9632f5)
![Competitor_Analysis](https://github.com/user-attachments/assets/5a11a964-b150-4811-bb64-3257dbc0e76a)

📌 Notes
This app is specifically built for OpenTable review URLs.
Selenium is used for dynamic scraping — make sure Chrome is installed and chromedriver is properly managed (via webdriver_manager).
All logic is modularized inside util.py to simplify maintenance and upgrades.

📄 License
This project is licensed under the MIT License.
