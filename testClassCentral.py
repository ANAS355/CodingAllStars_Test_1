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


class PageTester:

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
    
    def test_images(self):
        pass