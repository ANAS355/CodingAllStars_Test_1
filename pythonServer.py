from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi 
from dataclasses import dataclass
import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import urllib.parse as parse
import urllib.request
from urllib.request import urlopen as req_url
import string
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from threading import Thread
import pandas as pd
import time
import pyautogui
import ahk
import os
from langdetect import detect

hostName = "localhost"
serverPort = 3000
driver = webdriver.Chrome()
results = []

@dataclass
class TestPage:
    url: str = ""
    status: bool = False
    js_status: bool = False
    img_status: bool = False
    lang: str = ""
    lang_status: bool = False
    inner_status: bool = False
    inner_img_status: bool = False
    inner_lang_status: bool = False
    inner_lang: str = ""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = "<html><head><title>Anas Test</title></head>"
        page += "<p>Request: %s</p>" % self.path
        page += "<body>"
        page += "<p>This is an example web server.</p>"
        page += "<form method='POST' enctype='multipart/form-data' action='/'>"
        page += "<input name='user_urls' type='text'></input>"
        page += "<button type='submit'>Submit</button>"
        page += "</form>"
        page += "</body></html>"
        self.wfile.write(bytes(page, "utf-8"))

    def do_POST(self):
        print("POST called")
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            user_urls = fields.get("user_urls")[0].split("|")
            user_urls_list = [TestPage(url) for url in user_urls]
            print(user_urls_list)
            for url in user_urls_list:
                self.testPage(url)
            self.send_response(301)
            self.send_header("Content-type", "text/html")
            #self.send_header("Location", "/")
            self.end_headers()
            page = "<html><head><title>Anas test</title></head>"
            page += "<p>Request: %s</p>" % self.path
            page += "<body>"
            page += "<p>This is an example web server.</p>"
            page += "<form method='POST' enctype='multipart/form-data' action='/'>"
            page += "<input name='user_urls' type='text'></input>"
            page += "<button type='submit'>Submit</button>"
            page += "<ul>"
            for url in user_urls_list:
                page += f"<li>URl: {url.url}</li>" 
                text = f"lang_test:{url.lang_status}, js_test: {url.js_status}, inner_pages_test: {url.inner_status} "
                page += f"<li>{text}</li>" 
                text = f"page_language: {url.lang}, inner_pages_language: {url.inner_lang},"
                page += f"<li>{text}</li>" 
            page += "</ul>"
            page += "</form>"
            page += "</body></html>"
            self.wfile.write(bytes(page, "utf-8"))
    
    def testPage(self, page):
        driver.get(page.url)
        pages_list = []
        a_elemnts = driver.find_elements(By.TAG_NAME, 'a')
        for a in a_elemnts:
            href = a.get_attribute("href")
            if "www.classcentral.com" in href.split('/'):
                pages_list.append(href)
        # lang
        text = driver.find_element(By.XPATH, "/html/body").text
        page.lang = detect(text)
        print(page.lang)
        if page.lang == "hi":
            page.lang_status = True
        # js
        try:
            pyautogui.click("report.png")
            time.sleep(50)
            pyautogui.click("jsfun.png")
            page.js_status = True
            print(page.js_status)
        except:
            page.js_status = False
            print(page.js_status)

        
        try: 
            for i in range(50, 55):
                driver.get(page.url)
                text = driver.find_element(By.XPATH, "/html/body").text
                page.inner_lang = detect(text)
                print(page.lang)
                if page.inner_lang == "hi":
                    page.inner_lang_status = True
                    page.inner_status = True
                else:
                    page.inner_status = False
                    page.inner_lang_status = False    
                # js
                try:
                    pyautogui.click("report.png")
                    time.sleep(50)
                    pyautogui.click("jsfun.png")
                    page.inner_js_status = True
                except:
                    page.inner_js_status = False
        except:
            page.inner_status = False
            page.inner_lang_status = False
            page.inner_js_status = False

if __name__ == "__main__":       
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")