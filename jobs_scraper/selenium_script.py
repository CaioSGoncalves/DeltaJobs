# import web driver
import time
from datetime import datetime
from typing import List, Set

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from parsel import Selector

import config


class Job:
    def __init__(self, job_id: int, job_url: str, description: str, company_name: str, company_url: str, address: str):
        self.id = job_id
        self.url = job_url
        self.description = description
        self.company_name = company_name
        self.company_url = company_url
        self.address = address

        self.collected_date = datetime.utcnow()

    def to_dict(self) -> dict:
        return self.__dict__


def login(driver, email, password):
    driver.get('https://www.linkedin.com/login')

    email_field = driver.find_element_by_id('username')
    email_field.send_keys(email)

    password_field = driver.find_element_by_id('password')
    password_field.send_keys(password)

    # locate submit button by_class_name
    # sign_in_button = driver.find_element_by_class_name('btn__primary--large from__button--floating')
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()

    try:
        skip_button = driver.find_element_by_class_name("secondary-action")
        skip_button.click()
    except NoSuchElementException as e:
        print("No skip buttons")


def is_job_view_url(url: str) -> bool:
    return "/jobs/view" in url


def extract_jobs_urls(driver) -> Set[str]:
    jobs_urls = set()

    root_url = driver.current_url

    for i in range(1, 5):
        try:

            page_urls = [e.get_attribute("href") for e in driver.find_elements_by_tag_name("a")
                         if e.get_attribute("href") and is_job_view_url(e.get_attribute("href"))]
        except StaleElementReferenceException:
            page_urls = [e.get_attribute("href") for e in driver.find_elements_by_tag_name("a")
                         if e.get_attribute("href") and is_job_view_url(e.get_attribute("href"))]

        jobs_urls.update(page_urls)

        next_page = root_url + f"&start={i * 25}"
        driver.get(next_page)

    print("jobs_urls: ", len(jobs_urls))
    return jobs_urls


def extract_job(driver, url) -> Job:
    driver.get(url)
    sel = Selector(text=driver.page_source)

    job_id = int(url.split('/')[5])
    job_url = url
    company_name = str(sel.xpath('//a[@data-control-name="company_link"]/text()')[2].get()).strip()
    company_url = str(sel.xpath('//a[@data-control-name="company_link"]/@href')[0].get())

    element = sel.xpath('//span[@class="jobs-top-card__bullet"]/text()')
    if not element:
        element = sel.xpath('//a[@data-control-name="commute_module_anchor"]/text()')
    address = str(element[0].get()).strip()

    description = ",".join(sel.xpath('//div[@id="job-details"]//descendant::*/text()').extract()).strip()

    return Job(job_id, job_url, company_name, company_url, address, description)


if __name__ == "__main__":

    search_url = "/jobs/search/"

    params = [
        "?keywords=engenheiro%20de%20dados&location=Brazil",
        "?keywords=dataengineer&location=Worldwide"
    ]

    output_file = "jobs.csv"

    driver = webdriver.Chrome()

    email = config.linkedin_email
    password = config.linkedin_password
    login(driver, email, password)

    driver.get("https://www.linkedin.com/jobs/search/?keywords=engenheiro%20de%20dados&location=Brazil")

    jobs_urls = extract_jobs_urls(driver)

    jobs = list()
    for job_url in jobs_urls:
        try:
            job = extract_job(driver, job_url)
            jobs.append(job.to_dict())
        except Exception as e:
            print("error: ", job_url)
            if driver.find_element_by_id("main-frame-error"):
                time.sleep(10)
            pass

    print("collected jobs: ", len(jobs))
    print("x")
