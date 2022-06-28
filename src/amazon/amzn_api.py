import json
import logging
import os

from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI
from utils.formatting import PrettyJSONResponse
import requests

logger = logging.getLogger(__name__)
app = FastAPI(title="Amazon Price Tracker")

api_info = {
    "author": "Kyle McLester",
    "version": "0.1.0",
    "license": "MIT",
    "last_modified": datetime.fromtimestamp(
        os.path.getmtime(__file__)).strftime("%Y-%m-%d %H:%M:%S"),
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    "device-memory": "8",
    "downlink": "10",
    "dpr": "1",
    "ect": "4g",
    "referer": "https://www.amazon.com/",
    "rtt": "50",
    "sec-ch-device-memory": "8",
    "sec-ch-dpr": "1",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-ch-viewport-width": "2560",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": 'ubid-main=135-2000867-1455116; lc-main=en_US; av-timezone=America/New_York; session-id-apay=259-1446920-3405104; x-main="vsFSdRRmUu3M51VdSlTiiH1VXr?Y2xE2VFT7IHj?K?NLYoKpqbFcZDB9OP9V8SU2"; at-main=Atza|IwEBIASMAinSvEzz4n8gtWqYJQa0yNwbdlfV9EYtzhK4xtdZoIoYeivs9KhRXRVTiDpX62Affpy8-0Rkzcqo9yOoTGJQvKFsl-S-YyPE77RWc3oUOo4VNxmw-eYnPxOVZAkldNYGDIDwj6bXmPEhHovIjZIpKPTqgZDGLwZi3M7YUtOFYNdtcl8xmKptfAn-QYI9qoLj69bEiu9MTT7okJhgRnAN; sess-at-main="heHdZomxd1wcxAqMZDG+1ENuu8vE4UCuJRZCDfxHh9Y="; sst-main=Sst1|PQFFmy38eXcmDaLNhHo7C0HQCeP16Y2AqxjeLYPtK3cM98xnaGSDQpAI2ar9Vr6rQev3vKqGoOR84vOO7_Tq2-XJ7FiHFo2BSXDeKj28HJ6cEDpIn3NLI-Wlu4XkvRtboN5BMy44T_wf1-H7KWT-2nfe2zBfPr3c2QCE89zHd2OGzyowX8-zHA0amZ_auEdj7w4qqqgyC2H8KGF0JPIJ5Y88faIbGGCejpwCNIwHbuf_RCt-A5m21mBEtry6CunhYmR6EOWm9n95DMwtdA7qcCv6nPzj5uQvszgrrWp9iQBJ4rk; i18n-prefs=USD; aws-target-data={"support":"1"}; aws-target-visitor-id=1649519454494-237494.34_0; aws-ubid-main=507-7825868-5114761; regStatus=registered; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiYWI5MGQ5Iiwia2V5IjoiTmVLWjFBM1FHa0t2NFBha3E5UUwvY21TQ1FEOGVJOUFScGJVeEUyOGdOamJDOW43WG5uVnZodWEzQkd5Mk56STNpTHR1V2EvMWhYV3FYSmorZHhxSlIvTVVyZXUyYVVhbUNqMWc0Q3I1TTY5YXRUbU5MZSsvNGhxc0FON3RPWmE1dE9Eb2wvclV5SkxvZ3hFMG1YcVBBRWkxN2hMaUxHTmc3dGJhd0tlcG5LeFU4L1JZUUxYY0FHSlgyc2srS3Iwem82YkphV0l3bkJ3MGlLRTY3UWZRSHpKdll4RFlVOHl3ZEkwN3lUc3J5YlVEUnlkUnByTTg2ZkFuV2ZaZDFpSTcxYzRuN1VGNnYxWE5ZWTUrMmp0aHpTaGlFWmhYTlFscWVoTUpLZXJMYldNTnF1MWdvUDRXWTdlVTNMbTR1dmRlZGZ3WnFQNEFKckFydExZdFhSV0FRPT0ifQ==; session-id-time=2082787201l; awsc-color-theme=light; aws-account-alias=386625672301; remember-account=true; awsc-uh-opt-in=optedIn; ubid-acbus=133-5615831-1654422; s_pers= s_fid=0FD0D9D2C5BD46E8-05709DB62D1C5E9D|1813288281073; s_dl=1|1655523681074; gpv_page=US%3ASD%3ASOA-sem|1655523681080; s_ev15=%5B%5B%27SEUSSOAGOOG-BFBA12118B-D%27%2C%271655521881088%27%5D%5D|1813288281088;; session-id=138-1511163-3694249; aws-userInfo={"arn":"arn:aws:iam::386625672301:user/Admin","alias":"386625672301","username":"Admin","keybase":"ET7XD6m/qwCe6LIN2SQtjfOo92EJGhP16AmPj50h0u0\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIzODY2MjU2NzIzMDEiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiRVQ3WEQ2bVwvcXdDZTZMSU4yU1F0amZPbzkyRUpHaFAxNkFtUGo1MGgwdTA9IiwiYXJuIjoiYXJuOmF3czppYW06OjM4NjYyNTY3MjMwMTp1c2VyXC9BZG1pbiIsInVzZXJuYW1lIjoiQWRtaW4ifQ.mI45Zt3CUaqnIBAplos_0VJLhrlAlE2EZEj6RQg_mIYgC1pvF2YlhqbHtSIkhSQ0sTe5Rbaap_bKEfHjbmX2eaLTcAHW6Vj_Q034Owc11XCZiYfc_ZOi9slGpsKORetW; noflush_awsccs_sid=476c9be73aee90dc132b77e6c728f53318ef0b3eaeea2a3751a7e1f192942ae7; aws-signer-token_us-east-1=eyJrZXlWZXJzaW9uIjoia0lYaHRyWi5POFhvLjFneThKS251dnVOMkdmLnNaekYiLCJ2YWx1ZSI6Iml6czBTNE1HeGpkcjFYVEwyY1RlVlF1S1BXZStLTGVwczBSbHBrK1VFa2s9IiwidmVyc2lvbiI6MX0=; skin=noskin; appstore-devportal-locale=en_US; AMCVS_4A8581745834114C0A495E2B@AdobeOrg=1; AMCV_4A8581745834114C0A495E2B@AdobeOrg=-2121179033|MCIDTS|19165|MCMID|78874292570582572690789063218476171692|MCAAMLH-1656450963|7|MCAAMB-1656450963|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1655853363s|NONE|MCAID|NONE|vVersion|5.3.0; s_nr=1655846163812-New; s_lv=1655846163812; s_cc=true; _mkto_trk=id:365-EFI-026&token:_mch-amazon.com-1655846163911-86651; AMCVS_7742037254C95E840A4C98A6@AdobeOrg=1; AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19164|MCMID|79214851861875089580749940602310489095|MCAAMLH-1656451418|7|MCAAMB-1656451418|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1655853818s|NONE|MCAID|NONE|vVersion|4.4.0; aws-mkto-trk=id:112-TZM-766&token:_mch-aws.amazon.com-1654646904429-46811; aws_lang=en; session-token=LM3vfOQmjcfBhO8ZeWoIGWxSCorIDYb7x6+YXRPLNI+Y3fIKYmtuk8Ge7gE1p3Yhiwl64RE7o8iuMgBTqMpbykgTgz7KfPc/7qmjuzbLqY4mnL6cR+T0wFhfUUfF7hxHe0QbDCmeJK8Zf1jkl6cykJq7du/Trf2zz/SNQ3Ttklj9YXq/2kWpReKL+54xj//qGxBxZW2GFTSDMJvcp/DOOWTLobyUojr5RZbJBOGkN6ad9ZjC0EmiP1gk43Ww1aGxXLSAnvaO8C1hPEOsjhBtBQ==; csm-hit=tb:RY0MHYV8GS7FAYVQSPHJ+s-CTRTFFN9328RTTB7CSZT|1655852681412&t:1655852681412&adb:adblk_yes',
}


class Scraper():
    def __init__(self, url):
        self.url = url
        self.soup = self.create_soup()

    def page_status(self):
        return requests.get(self.url, headers=headers).status_code

    def create_soup(self):
        if self.page_status() == 200:
            data = requests.get(self.url, headers=headers).text
            soup = BeautifulSoup(data, 'html.parser')
        return soup

    def get_title(self):
        return self.soup.find(
            "span", attrs={
                "id": "productTitle"}).text.strip()

    def get_price(self):
        return self.soup.find(
            "span", attrs={
                "class": "a-offscreen"}).text.strip()

    def get_stock_status(self):
        return self.soup.find("div", attrs={"id": "availability"}).text.strip()

    def get_ratings(self):
        return self.soup.find(
            "span", attrs={
                "class": "a-icon-alt"}).text.strip()

    def get_ratings_count(self):
        return self.soup.find(
            "span", attrs={
                "id": "acrCustomerReviewText"}).text.strip()


@app.get("/", response_class=PrettyJSONResponse)
def root():
    return api_info


@app.get("/tracker", response_class=PrettyJSONResponse)
def tracker():
    with open('./src/vars.json', 'r') as f:
        vars = json.loads(f.read())
    scrape = Scraper(url=vars["url"])
    return {
        "product_title": scrape.get_title(),
        "product_price": scrape.get_price(),
        "stock_status": scrape.get_stock_status(),
        "product_rating": scrape.get_ratings(),
        "ratings_count": scrape.get_ratings_count()
    }
