import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
import schedule
import time
import os
import random  # To select random jobs

# --- Logging setup ---
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://vacancymail.co.zw"
JOBS_URL = f"{BASE_URL}/jobs/"

# Fetch job description from the job listing page
def fetch_job_description(job_url):
    try:
        res = requests.get(job_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        desc = soup.select_one(".job-desc")
        return desc.get_text(strip=True) if desc else "No full description available"
    except Exception as e:
        logging.error(f"Error fetching description for {job_url}: {e}")
        return f"Error fetching description: {e}"

# Scrape job listings from a specific page
def scrape_jobs(page_url):
    logging.info(f"Starting job scraping task on {page_url}.")
    try:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logging.error(f"Failed to fetch jobs list from {page_url}: {e}")
        return pd.DataFrame()

    # Extract job cards
    job_cards = soup.select("a.job-listing")
    
    # Randomly shuffle the job cards and select a random sample of jobs
    random.shuffle(job_cards)  # Shuffle the list to randomize the order
    job_cards = job_cards[:10]  # Select top 10 jobs from the page
    
    jobs = []
    for card in job_cards:
        try:
            title = card.select_one(".job-listing-title").get_text(strip=True)
            company_tag = card.select_one(".job-listing-company")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"
            location = card.select_one("li i.icon-material-outline-location-on").find_next("li").text.strip()
            expiry = card.select("li")[1].get_text(strip=True)
            short_desc = card.select_one(".job-listing-text").get_text(strip=True)
            link = card["href"]
            full_link = f"{BASE_URL}{link}"
            full_desc = fetch_job_description(full_link)

            jobs.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Expiry Date": expiry,
                "Short Description": short_desc,
                "Full Description": full_desc,
                "Link": full_link,
                "Scraped On": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            logging.info(f"Scraped job: {title} at {company}")
        except Exception as e:
            logging.error(f"Error parsing job card: {e}")

    # Return the data as a DataFrame
    df = pd.DataFrame(jobs)
    return df

# Scheduled task to scrape jobs at regular intervals
def job():
    logging.info("Scheduled scraping job started.")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal (Windows/Linux)
    
    all_jobs = []  # List to hold all jobs (used for Excel)
    first_10_jobs = []  # List to hold only the first 10 jobs for CSV
    
    # Scrape multiple pages (up to 5 pages, fetching 10 jobs per page)
    for page_number in range(1, 6):  # This loops through 5 pages
        page_url = f"{JOBS_URL}?page={page_number}"
        df = scrape_jobs(page_url)
        all_jobs.append(df)  # Add data to the list for the Excel file
    
    # Combine all job data from multiple pages into one DataFrame for Excel
    final_df_all_jobs = pd.concat(all_jobs, ignore_index=True)
    
    # Save the first 10 random jobs to CSV (for a total of 10 random jobs)
    final_df_random_jobs = final_df_all_jobs.sample(n=10, random_state=42)
    final_df_random_jobs.to_csv("scraped_data.csv", index=False)
    logging.info(f"Saved {len(final_df_random_jobs)} random jobs to scraped_data.csv")

    # Save up to 50 jobs to Excel (but we can limit it to 30 if fewer jobs are scraped)
    final_df_all_jobs = final_df_all_jobs.head(50)  # Limit to a maximum of 50 jobs for Excel
    final_df_all_jobs.to_excel("scraped_data.xlsx", index=False)
    logging.info(f"Saved {len(final_df_all_jobs)} jobs to scraped_data.xlsx")

    print(final_df_all_jobs.head(50))  # Show the jobs in terminal

if __name__ == "__main__":
    # Schedule the scraping job to run every 5 seconds
    schedule.every(5).seconds.do(job)
    logging.info("Scheduler started. Job will run every 5 seconds.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Keep checking every second
    except KeyboardInterrupt:
        logging.info("Scraper stopped by user (Ctrl + C). Exiting gracefully.")
        print("\nScraper stopped. Goodbye!")
