import os
from datetime import datetime
import requests

import pandas as pd
from fastapi import FastAPI
from formatting import PrettyJSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By

app = FastAPI(title="Builders Auction Tracker")

api_info = {
    "author": "Kyle McLester",
    "version": "0.1.0",
    "license": "MIT",
    "last_modified": datetime.fromtimestamp(
        os.path.getmtime(__file__)).strftime("%Y-%m-%d %H:%M:%S"),
}


class Scraper:
    def __init__(self, URL):
        self.URL = URL
        self.OPTIONS = webdriver.ChromeOptions()
        self.OPTIONS.headless = True
        self.DRIVER_PATH = "/Users/kmclester/Documents/chromedriver"

    def start_chromedriver(self):
        driver = webdriver.Chrome(
            executable_path=self.DRIVER_PATH, options=self.OPTIONS
        )
        driver.get(self.URL)
        return driver

    def get_items_for_sale(self, driver):
        lot_title = driver.find_elements(
            by=By.CSS_SELECTOR, value=".lot-tile-lead-container-header"
        )
        lot_link = driver.find_elements(
            by=By.CSS_SELECTOR, value=".lot-tile-lead-container-header a"
        )
        current_bid = driver.find_elements(
            by=By.CSS_SELECTOR, value=".lot-high-bid")
        time_remaining = driver.find_elements(
            by=By.CLASS_NAME, value="lot-time-left")
        suggested_bid = driver.find_elements(
            by=By.CLASS_NAME, value="TileDisplayMinBid"
        )
        images = driver.find_elements(by=By.CLASS_NAME, value="lot-thumbnail")

        links = [link.get_attribute("href") for link in lot_link][:50]
        titles = [title.text for title in lot_title][:50]
        bids = [bid.text for bid in current_bid][:50]
        time_left = [time.text for time in time_remaining][:50]
        next_bids = [next_bid.text for next_bid in suggested_bid][:50]
        thumbnails = [thumbnail.get_attribute(
            "src") for thumbnail in images][:50]

        df = pd.DataFrame(
            columns=[
                "title",
                "current_bid",
                "suggested_bid",
                "time_remaining",
                "link",
                "thumbnail",
            ]
        )

        df.title = titles
        df.current_bid = bids
        df.suggested_bid = next_bids
        df.time_remaining = time_left
        df.link = links
        df.thumbnail = thumbnails

        return df.T.to_dict()

    def download_images(self, ITEMS):
        [
            open(
                f"./src/images/{key}.jpeg",
                "wb").write(
                requests.get(
                    ITEMS[key]["thumbnail"]).content) for key in ITEMS.keys()]


@app.get("/", response_class=PrettyJSONResponse)
def root():
    return api_info


@app.get("/items-for-sale", response_class=PrettyJSONResponse)
async def items_for_sale():
    scraper = Scraper(
        URL="https://buildersauctioncompany.hibid.com/catalog/378597/40149-charlotte-nc/")
    driver = scraper.start_chromedriver()
    items = scraper.get_items_for_sale(driver)

    driver.quit()
    return items
