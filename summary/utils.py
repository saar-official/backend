from random import random
import requests
from .models import Summary
import json


def scrape_data_from_url(url, headers):
    """
    function to call the scrape data service and pull out the press release as text
    returns: `text`
    """
    SCRAPER_SERVICE_URL = "http://localhost:8002/api/v1/scraper/scrape"
    data = {"link": url}
    res = requests.post(url=SCRAPER_SERVICE_URL, data=json.dumps(
        data, indent=2), headers=headers)
    response = res.json()
    print("scraping done")
    return response


def fetch_summary_and_key_highlights(text, headers):
    """
    function to fetch the summary and key highlights from the press release text
    returns: `summary, highlights`
    """
    ML_SERVICE_URL = "http://localhost:8000/api/v1/summary/summarise"
    data = {"text": text}
    res = requests.post(url=ML_SERVICE_URL, data=json.dumps(
        data, indent=2), headers=headers)
    summary, highlights = res.json()['summary'], res.json()['highlights']
    print("summarization done")
    return (summary, highlights)


def check_if_text_already_exists(text: str):
    queryset = Summary.objects.filter(text=text)
    if queryset.exists():
        return queryset[0]
    else:
        return False
