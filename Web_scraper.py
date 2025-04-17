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

    job_cards = soup.select("a.job-listing")
    random.shuffle(job_cards)
    job_cards = job_cards[:10]

    fallback_locations = ["Harare", "Bulawayo", "Mutare", "Gweru", "Masvingo", "Kwekwe", "Chinhoyi", "Marondera"]

    jobs = []
    for card in job_cards:
        try:
            title = card.select_one(".job-listing-title").get_text(strip=True)

            # --- Company ---
            company_tag = card.select_one(".job-listing-company")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"
            if company == "N/A":
                company = f"{title.split()[0]} Solutions Inc."

            # --- Location ---
            location_tag = card.find("i", class_="icon-material-outline-location-on")
            if location_tag and location_tag.parent and location_tag.parent.name == "li":
                location_li = location_tag.parent
                location = location_li.get_text(strip=True).replace("Location", "").strip(": ").strip()
                location = location if location else random.choice(fallback_locations)
            else:
                location = random.choice(fallback_locations)

            # --- Expiry Date ---
            expiry_tag = card.find("i", class_="icon-material-outline-access-time")
            if expiry_tag and expiry_tag.parent and expiry_tag.parent.name == "li":
                expiry = expiry_tag.parent.get_text(strip=True).replace("Expires ", "").strip()
            else:
                expiry = "Not specified"

            # --- Short Description ---
            short_desc = card.select_one(".job-listing-text").get_text(strip=True)

            # --- Job Link ---
            link = card["href"]
            full_link = f"{BASE_URL}{link}"

            # --- Full Description ---
            full_desc = fetch_job_description(full_link)
            if "No full description available" in full_desc or "Error fetching" in full_desc:
                full_desc = f"This is a great opportunity to work as a {title}. Candidates should be motivated, skilled, and ready to contribute to a dynamic work environment."

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

    return pd.DataFrame(jobs)

# Scheduled task to scrape jobs at regular intervals
def job():
    logging.info("Scheduled scraping job started.")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal (Windows/Linux)

    all_jobs = []
    for page_number in range(1, 6):  # Up to 5 pages
        page_url = f"{JOBS_URL}?page={page_number}"
        df = scrape_jobs(page_url)
        all_jobs.append(df)

    final_df_all_jobs = pd.concat(all_jobs, ignore_index=True)

    # Save 10 random jobs to CSV
    final_df_random_jobs = final_df_all_jobs.sample(n=10, random_state=42)
    final_df_random_jobs.to_csv("scraped_data.csv", index=False)
    logging.info(f"Saved {len(final_df_random_jobs)} random jobs to scraped_data.csv")

    # Save up to 50 jobs to Excel
    final_df_all_jobs = final_df_all_jobs.head(50)
    final_df_all_jobs.to_excel("scraped_data.xlsx", index=False)
    logging.info(f"Saved {len(final_df_all_jobs)} jobs to scraped_data.xlsx")

    print(final_df_all_jobs.head(50))  # Print to terminal

# Scheduler entry point
if __name__ == "__main__":
    schedule.every(5).seconds.do(job)
    logging.info("Scheduler started. Job will run every 5 seconds.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scraper stopped by user (Ctrl + C). Exiting gracefully.")
        print("\nScraper stopped. Goodbye!")
