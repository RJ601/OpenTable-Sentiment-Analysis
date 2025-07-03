import streamlit as st
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import matplotlib.pyplot as plt

from groq import Groq
import os


# MODULE 1 - WEB SCRAPPING

driver = None


def scrape_reviews(url, start = 1, pages = 10): #can change number of pages to be scraped for reviews
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    
    # name of restaurant
    name_of_restaurant = (driver.find_element(By.TAG_NAME, 'h1')).text
    print(name_of_restaurant)
    
    # reviews - date, reviewer, rating, comment
    # make a list and append reviews for upto 200 pages and 
    count = start # number of pages
    
    reviewers = []
    base_url = url
    
    
    # loop here
    while (count <= pages):
        #driver.close()
        url = f"{base_url}&page={count}"    
        driver.get(url)
        #driver.switch_to.window(driver.window_handles[0]) 
        
        reviews = []
        reviews = driver.find_element(By.CSS_SELECTOR, ".ZfJD76NR7i4- .WG-kJ5LdIoM- ._5nr3E4B6niQ-").find_elements(By.CSS_SELECTOR, ".PzNNARxpE3A- .afkKaa-4T28-") 
    
        # extract useful data
        for review in reviews:
            rating_elm = review.find_element(By.CSS_SELECTOR, ".tSiVMQB9es0-")
            rating = float(driver.execute_script("return arguments[0].textContent;", rating_elm).strip())
            comment = review.find_element(By.CSS_SELECTOR, "._6rFG6U7PA6M- span")
            date = review.find_element(By.CSS_SELECTOR, ".iLkEeQbexGs-")
            name = review.find_element(By.CSS_SELECTOR, ".Ez4i-VmIBvE- p")
            reviewers.append({'Reviewer Name': name.text, 'Rating': rating, 'Comment': comment.text, 'Date': date.text})
    
        # move to next page
        count += 1 
    
    df = pd.DataFrame(reviewers)
    df.to_csv(f"{name_of_restaurant}.csv", index = False)

    driver.quit()

    return name_of_restaurant


# MODULE 2 - PROMPT ENGINEERING

def ask(message, sys_message,
         model="llama3-8b-8192"):

    # Construct the messages list for the chat
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": message}
    ]

    # Send the messages to the model and get the response
    response = client.chat.completions.create(model=model, messages=messages)

    # Return the content of the model's response
    return response.choices[0].message.content


# format the analysis as a dictionary
def format(str, reviewer, rating, date):
    
    index = str.find('review_text')
    start = str.find(" \"", index)
    end = str.find(",\n", start)
    review = str[start+2:end-1]

    # food_comment
    index = str.find('category', end)
    start = str.find(" \"", index)
    end = str.find(",\n", start)
    food_category = str[start+2:end-1]
    index = str.find('\"comment\"', end)
    start = str.find(" \"", index)
    end = str.find("\"\n", start)
    food_comment = str[start+2:end]

    # staff_comment
    index = str.find('category', end)
    start = str.find(" \"", index)
    end = str.find(",\n", start)
    staff_category = str[start+2:end-1]
    index = str.find('\"comment\":', end)
    start = str.find(" \"", index)
    end = str.find("\"\n", start)
    staff_comment = str[start+2:end]

    return {'Reviewer': reviewer, 'Rating': rating, "Date": date, 'Review': review, "Food": {"Sentiment": food_category, "Comment": food_comment}, "Staff": {"Sentiment": staff_category, "Comment": staff_comment}}
    

def llm_analysis(file_path, system_message):
    df = pd.read_csv(f"{file_path}")
    
    analysis = []
    batch = []
    
    for row in range(1, 31):
        batch.append(df.iloc[row-1, 2])
        if (row%30 == 0):
            batch_str = "---".join(batch)
            print(batch_str)
            llm_response = ask(batch_str, system_message)
            batch = []
            print(llm_response)
            time.sleep(30)
    
            temp = llm_response.split('---')

            count2 = 30
            for count in temp:
                # also send reviewer name, date, rating 
                analysis.append(format(count, df.iloc[row-count2, 0], df.iloc[row-count2, 1], df.iloc[row-count2, 3]))
                count2 -= 1
    
    return analysis


def toJson(analysis, restaurant):
    file = open(f'Review_Analysis_{restaurant}.json', 'w') 
    
    json.dump(analysis, file, indent = 4)


# Main 

os.environ['GROQ_API_KEY'] = 'your_api_key_here' # replace with your own key

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_message = """
You are a highly capable assistant trained to analyze customer reviews. Your task is to:
1. Extract and categorize comments about food quality as "positive", "negative", or "neutral".
2. Extract and categorize comments about staff/service as "positive", "negative", or "neutral".
3. Exclude irrelevant comments (e.g., ambiance, location) and ensure they don't appear in the food or staff categories.
4. Ensure no personal information (PI) of the reviewer is included.
5. You will be provided with the reviews in batches of 30. For each batch, individual reviews will be separated using the delimmeter '---'. Process each individual review in a batch separately.
6. Don’t return the output as a single list. Instead, output each review’s JSON block individually and separate each with --- exactly. Do not wrap them in brackets or commas. Return raw JSON objects only.
7. Provide the output in the following JSON format:

{
    "review_text": "Review text goes here.",
    "food_comments": {
        "category": "positive/negative/neutral",
        "comment": "Specific food-related comment here"
    },
    "staff_comments": {
        "category": "positive/negative/neutral",
        "comment": "Specific staff-related comment here"
    }
}

**Example Review and Expected Output:**

Review Text:  
"The food was absolutely delicious, the chicken was tender and flavorful. However, the staff was not very friendly. The waiter seemed disinterested in helping us. The atmosphere was pleasant, but the service left a lot to be desired.---Amazing pizza and pasta! The staff was kind and attentive, making our experience delightful. A truly wonderful dinner."

Expected Output:
{
    "review_text": "The food was absolutely delicious, the chicken was tender and flavorful. However, the staff was not very friendly. The waiter seemed disinterested in helping us. The atmosphere was pleasant, but the service left a lot to be desired.",
    "food_comments": {
        "category": "positive",
        "comment": "The food was absolutely delicious, the chicken was tender and flavorful."
    },
    "staff_comments": {
        "category": "negative",
        "comment": "The staff was not very friendly. The waiter seemed disinterested in helping us."
    }
}
---
{
    "review_text": "Amazing pizza and pasta! The staff was kind and attentive, making our experience delightful. A truly wonderful dinner.",
    "food_comments": {
        "category": "positive",
        "comment": "Amazing pizza and pasta!"
    },
    "staff_comments": {
        "category": "positive",
        "comment": "The staff was kind and attentive, making our experience delightful."
    }
}

The above Expected Output is how you are going to generate response. Deliver the response in that exact format as I need it stored as a json file. If there are no comments on any of the categories (food_comments or staff_comments), leave the fields for that category blank.
Now, analyze the following review and categorize the comments about food and staff in the same way.

"""