# OpenTable-Sentiment-Analysis
Skills: Web Scrapping, Prompt Engineering, Streamlit, Matplotlib

# 🍽️ Restaurant Review Analyzer

**Restaurant Review Analyzer** is a multi-page Streamlit web app that scrapes and analyzes restaurant reviews from **OpenTable**. It uses the **Groq LLM API** to extract structured insights about food and staff quality from customer feedback.

---

## 🧠 Key Features

- 🔍 **Review Dashboard**:  
  Scrape reviews of a single restaurant and analyze sentiment on food and staff.
  
- 📊 **Competitor Analysis**:  
  Compare average ratings between two restaurants using visual graphs.

- 🎯 **LLM-Based Analysis**:  
  Uses structured prompts and LLM output to categorize review content.

- 🧾 **Export**:  
  Saves analysis results as `.json` and competitor comparison as `.jpg`.

---

## 🗂️ Project Structure

restaurant-review-analyzer/
│
├── Dashboard.py # Landing page with sidebar navigation
├── pages
    ├── 1_Reviews_Dashboard.py # Single restaurant review dashboard
    ├── 2_Competitor_Analysis_Dashboard.py # Compare two restaurants
├── util.py # Core logic: scraping, prompting, formatting
├── requirements.txt # (You generate this using pip freeze)
├── LICENSE
└── README.md # Project instructions (you are here)

---

## ⚙️ Setup Instructions

### 🔁 1. Clone the Repository

git clone https://github.com/your-username/restaurant-review-analyzer.git
cd restaurant-review-analyzer

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

🖼️ Output
The Reviews Dashboard will save a .json file with categorized review data and would display the colour-coded reviews on the streamlit dashboard.
The Competitor Analysis page will generate a .jpg line chart comparing average ratings over time.

📌 Notes
This app is specifically built for OpenTable review URLs.
Selenium is used for dynamic scraping — make sure Chrome is installed and chromedriver is properly managed (via webdriver_manager).
All logic is modularized inside util.py to simplify maintenance and upgrades.

📄 License
This project is licensed under the MIT License.
