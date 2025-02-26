import csv
import json
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def wait_for_full_text(driver, locator, timeout=30, poll_interval=1):
    """
    Poll the element's innerText until it stops changing or until timeout.
    The locator should be a tuple, e.g. (By.XPATH, 'your_xpath_here').
    """
    prev_text = ""
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            element = driver.find_element(*locator)
            current_text = element.get_attribute("innerText")
        except StaleElementReferenceException:
            time.sleep(poll_interval)
            continue

        if current_text == prev_text and current_text.strip() != "":
            return current_text
        prev_text = current_text
        time.sleep(poll_interval)
    return prev_text

def extract_json(text):
    """
    Extract the JSON substring from the text.
    """
    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return text.strip()

def open_perplexity_and_search(query):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Not using headless mode to reduce detection risk.
    driver = uc.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    
    driver.get("https://www.perplexity.ai/")
    time.sleep(5)  # Allow time for pop-ups or CAPTCHA challenges

    try:
        search_box_locator = (By.XPATH, '//textarea[@placeholder="Ask anything..."]')
        search_box = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(search_box_locator)
        )

        # Retry logic in case the search box goes stale.
        attempts = 0
        while attempts < 3:
            try:
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                break  # Exit loop if successful.
            except StaleElementReferenceException:
                attempts += 1
                search_box = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(search_box_locator)
                )
                time.sleep(1)
        else:
            raise Exception("Unable to interact with the search box after multiple attempts.")

        # Define locator for the answer container.
        answer_locator = (By.XPATH, '//div[contains(@class, "prose") and contains(@class, "text-pretty")]')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(answer_locator)
        )
        
        # Wait until the answer text stops updating.
        full_text = wait_for_full_text(driver, answer_locator, timeout=30, poll_interval=1)
        json_output = extract_json(full_text)
        return json_output
    except Exception as e:
        print("An error occurred:", str(e))
        return None
    finally:
        time.sleep(5)
        driver.quit()

def main():
    input_csv = "input.csv"   # CSV file containing company names (with header "company_name")
    output_csv = "output.csv" # CSV file to write results

    # Prepare the output CSV file with headers.
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "source_company", 
            "investment_company", 
            "CEO_name", 
            "CEO_linkedin",
            "average_check_size",
            "investment_received",
            "description"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
    # Read input CSV and process each company name.
    with open(input_csv, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = row["company_name"]
            # Inject the company name into the search prompt.
            prompt = (
                f"Please search for the latest 5 investments made by '{company}' in the mental health space; "
                "for each investment, provide the following details: Company Name, CEO Name, CEO LinkedIn URL, "
                "average check size of the VC, the investment the company received, and a brief description of what the company does. "
                "Return your answer as structured JSON in the following format: "
                '{"investments": [{"company_name": "Example Company", "CEO_name": "John Doe", "CEO_linkedin": "https://www.linkedin.com/in/example", "average_check_size": "amount", "investment_received": "investment amount", "description": "Brief description of the company’s focus and product."}, ...]} '
                "ensuring exactly 5 investment objects and that all provided information is current and accurate."
            )
            print(f"Processing company '{company}' with prompt:\n{prompt}\n")
            json_output = open_perplexity_and_search(prompt)
            
            if json_output is None:
                print(f"No output for {company}.")
                continue

            # Parse the JSON output.
            try:
                data = json.loads(json_output)
                investments = data.get("investments", [])
            except Exception as e:
                print(f"Error parsing JSON for company {company}: {e}")
                continue
            
            # Append each investment to the output CSV.
            with open(output_csv, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                    "source_company", 
                    "investment_company", 
                    "CEO_name", 
                    "CEO_linkedin",
                    "average_check_size",
                    "investment_received",
                    "description"
                ])
                for inv in investments:
                    writer.writerow({
                        "source_company": company,
                        "investment_company": inv.get("company_name", ""),
                        "CEO_name": inv.get("CEO_name", ""),
                        "CEO_linkedin": inv.get("CEO_linkedin", ""),
                        "average_check_size": inv.get("average_check_size", ""),
                        "investment_received": inv.get("investment_received", ""),
                        "description": inv.get("description", "")
                    })

if __name__ == "__main__":
    main()
