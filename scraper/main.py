from __future__ import annotations
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scraper.scraper.spiders.form4Spider import Form4Spider
from scraper import spider_config
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import pandas as pd
import requests
import time
from utils import utils
import warnings
warnings.filterwarnings("ignore")


BASE_URL = "https://www.sec.gov/Archives/edgar/data"

def call_scraper(start_urls:list)->None:
    """
    calls scrapy based form4Spider to:
    - crawl submission folder links,
    - scrape form4 information
    - store the xml parsed data in /data/form4.csv 
    """
    configure_logging()
    settings = get_project_settings()
    settings.set('FEEDS', spider_config.feed_custom_settings)
    runner = CrawlerRunner(settings)
    d = runner.crawl(Form4Spider, start_urls = start_urls)
    d.addBoth(lambda _:reactor.stop())
    reactor.run()

def get_all_submission_info(cik:str)->pd.DataFrame:
    """
    retrieves submission folder names from {base_url}/{cik} link
    """
    url = f"{BASE_URL}/{cik}"
    response = None
    print(f"getting folder's detail for {cik} using link: {url}")
    try: 
        response = requests.get(
            url,
            headers = {
                'Connection': 'close',
                'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            }
        )
        submission_table = pd.read_html(response.text)[0]
    except:
        print(f"status code:{response.status_code}. Please try after sometime")
    return submission_table


def get_start_urls(cik:str, folder_names:list)->str:
    return [f"{BASE_URL}/{cik}/{int(name):018d}" for name in folder_names]


def main(ciks:list, month:list, year:list)->None:
    """
    return name of the folders to be parsed by scrapper for getting form4 links
    """
    print(ciks)
    print(year)
    print(month)
    start_urls = []
    for cik in ciks:
        print(f"scraping list of folders for:{cik}")
        submission_table = get_all_submission_info(cik)
        sub_table_processed = utils.preprocess_table(submission_table)
        name_list = utils.filter_folder_name(sub_table_processed, year, month)
        start_urls.extend(get_start_urls(cik, name_list))
        time.sleep(0.2)
    print(len(start_urls))
    call_scraper(start_urls)


if __name__ == "__main__":
    params = utils.read_params("params.yml")
    main(**params)