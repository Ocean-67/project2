# Job Scraper Web Scraper 🧑‍💻

This Python-based **web scraper** collects job listings from **[vacancymail.co.zw](https://vacancymail.co.zw)**, extracts job details, and saves the data into both **CSV** and **Excel** files. The script also includes automated scheduling for periodic scraping.

## Features ✨

- **Scrapes job listings** from multiple pages of the website.
- **CSV Output**: Saves **10 random job listings** to `scraped_data.csv`.
- **Excel Output**: Saves up to **50 job listings** to `scraped_data.xlsx`.
- **Automated Scheduling**: Scrapes data every **5 seconds**.
- **Error Logging**: Logs scraping progress and errors into `scraper.log`.
- **Terminal Display**: Shows the scraped job listings in the terminal.

---

## Requirements 🛠

Ensure you have Python 3.6+ and the following libraries installed:

- `requests`  
- `beautifulsoup4`  
- `pandas`  
- `openpyxl`  
- `schedule`

Install them with:

```bash
pip install requests beautifulsoup4 pandas openpyxl schedule
How It Works 🔄
1. Scrape Job Listings:
The scraper collects job data such as:

Job Title

Company Name

Location

Expiry Date

Short Description

Full Description (from detailed job page)

2. Data Saving:
CSV: Saves 10 random job listings in scraped_data.csv.

Excel: Saves up to 50 job listings in scraped_data.xlsx.

3. Automated Scheduling:
The script runs every 5 seconds to scrape and store new job listings.

4. Logging:
All important actions (including errors) are logged in a scraper.log file for easy troubleshooting.

Files 📂
scraped_data.csv: Contains 10 random job listings.

scraped_data.xlsx: Contains up to 50 job listings.

scraper.log: Logs details of the scraper's execution and errors.

Usage 🚀
Clone the repository or download the script (web_scraper.py).

Run the script in your terminal:

bash
Copy
Edit
python web_scraper.py
Outputs:

The script scrapes data from the website and saves 10 job listings in a CSV file (scraped_data.csv).

It also saves up to 50 job listings in an Excel file (scraped_data.xlsx).

Job listings will be printed in the terminal window.

Stopping the Script: To stop the scraper, press Ctrl + C in your terminal. The script will log the event and exit gracefully.

Example Output 📊
CSV Output (scraped_data.csv)

Job Title	Company	Location	Expiry Date	Short Description	Full Description	Link	Scraped On
Electrical Design Engineer	ABC Corp	Harare	2025-04-20	Electrical designs for various projects	Full details...	[link]	2025-04-16 12:59:32
SALES REPS	XYZ Ltd	Bulawayo	2025-04-25	Sales reps needed for retail positions	Full details...	[link]	2025-04-16 12:59:33
Excel Output (scraped_data.xlsx)
Contains up to 50 job listings with the same structure as the CSV output.

Scheduling ⏰
The scraper is scheduled to run every 5 seconds. You can modify this interval in the script:

python
Copy
Edit
schedule.every(5).seconds.do(job)
To change the frequency to every 10 minutes, for example:

python
Copy
Edit
schedule.every(10).minutes.do(job)
Error Handling & Logging 📝
The script includes robust error handling to catch and log errors encountered during scraping. Events such as failed requests or parsing errors are recorded in the scraper.log file.

Sample log entry:
text
Copy
Edit
2025-04-16 13:00:32 - INFO - Scraping started.
2025-04-16 13:00:35 - ERROR - Failed to fetch job description for https://vacancymail.co.zw/jobs/12345: Connection Timeout.
Contributing 💡
Feel free to fork the repository, report issues, or submit pull requests for improvements!

License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Support 🙋‍♂️
If you encounter any issues or have questions, please feel free to open an issue or contact the maintainers.