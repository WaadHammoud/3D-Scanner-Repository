from selenium import webdriver
from selenium.webdriver.common.by import By
from socket import *

class ChromiumService(self, driver):
    
    def __init__(self, driver):
        self.driver = webdriver.Chrome(driver) #Set path to webdriver (Example: driver = "/usr/lib/chromium-browser/chromedriver")
    
    #Open to specified webpage
    def Open(self, url):
        # Implicit wait
        self.driver.implicitly_wait(0.5)
        # Maximize browser
        self.driver.maximize_window()
        # Launch URL
        self.driver.get(url)
        
    #Upload file to webpage
    def Upload(self, filePath):
        # Identify Choose file button and send filePath to it
        self.driver.find_element(By.NAME, 'uploadedFile').send_keys(filePath)
        # Click Upload Button
        self.driver.find_element(By.NAME, "uploadBtn").click()
    
    def Close(self):
        # Close browser
        self.driver.quit()
