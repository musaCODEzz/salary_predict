from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

# Replace with your path to chromedriver.exe
path = "C:/Users/MUSA-PC/Desktop/data_project/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Target URL for data scientist jobs
web = "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
driver.get(web)

careers = []  # List to store job listing elements

# Wait for job listings to load
wait = WebDriverWait(driver, 10)
careers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'JobsList_jobListItem__wjTHv')]")))

Company_name = []
Company_location = []
Company_salary = []

for career in careers:
    try:
        # Extract company name
        company_name_element = career.find_element(by='xpath', value='.//div[contains(@class, "EmployerProfile_profileContainer__VjVBX")]')
        Company_name.append(company_name_element.text.strip())
    except NoSuchElementException:
        Company_name.append('N/A')
    
    try:
        # Extract company location
        company_location_element = career.find_element(by='xpath', value='.//div[contains(@class, "JobCard_location__rCz3x")]')
        Company_location.append(company_location_element.text.strip())
    except NoSuchElementException:
        Company_location.append('N/A')
    
    try:
        # Extract salary with wait for dynamic content within the context of the current career element
        salary_element = WebDriverWait(career, 10).until(
            EC.presence_of_element_located((By.XPATH, './/div[contains(@class, "JobCard_salaryEstimate__arV5J")]'))
        )
        Company_salary.append(salary_element.text.strip())
    except (NoSuchElementException, TimeoutException):
        Company_salary.append('N/A')

# Create pandas dataframe and save to CSV
df = pd.DataFrame({'Company Name': Company_name, 'Company Location': Company_location, 'Estimated Salary': Company_salary})
df.to_csv('salary.csv', index=False)

driver.quit()
