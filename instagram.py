from flask import *
import random
import time
import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys



class DownloadInsta:
    def __init__(self,url,loc):
        self.url = url
        self.loc = loc

        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        self.username = os.environ.get("INSTA_USER_NAME")
        self.password = os.environ.get("INSTA_PASS")
        
        # instagram's video src doesn't work on PC normally. Video has 'blob:https://...' link format
        # but using mobile emulator, link has normal form ('https://...')

        mobile_emulation = {
            "deviceName": "iPhone X"
        }  # choose device to emulate

        # define a variable to hold all the configurations we want
        chrome_options = webdriver.ChromeOptions()

        # add the mobile emulation to the chrome options variable
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        

        # create driver, pass it the path to the chromedriver file and the special configurations you want to run
        # path = join(dirname(__file__), 'chromedriver')
        print(os.environ.get("CHROMEDRIVER_PATH"))
        self.browser = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            options=chrome_options)

    def close_browser(self):
        self.browser.close()  # close browser
        self.browser.quit()  # (just in case)

    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self,username, password):

        try:
            # self.username = username
            # self.password = password
            # open website
            self.browser.get('https://www.instagram.com/accounts/login/?next=%2F&source=mobile_nav')
            time.sleep(random.randrange(2, 4))
            print(self.browser.title)
            # find username input
            user_input = self.browser.find_element_by_name('username')
            # clear the field (just in case)
            user_input.clear()
            # write the username
            user_input.send_keys(username)

            time.sleep(random.randrange(2, 4))
            # find password input
            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            # write the password
            password_input.send_keys(password)
            
            time.sleep(random.randrange(2, 4))
            # send the complete authorization form
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)
        # if smth went wrong, close the browser
        except Exception as ex:
            print(ex)
            self.close_browser()

    def get_link(self, url):
        if url[0:25] == "https://www.instagram.com":
            url_1 = url.split("/")[-2]
            print(url_1)
            if len(url_1) >= 20:
                print("Error: This is a privet account")
                username = self.username
                password = self.password
                self.login(username, password)
                return True
            return True            
        else:
            print('Error: Check url')
            return False

    def download_videos(self):
        try:
            post_url = self.url
            self.browser.get(post_url)
            if self.browser.title == "Login • Instagram":
                username = self.username
                password = self.password
                self.login(username, password)
                self.browser.get(post_url)

            print(self.browser.title)
            time.sleep(4)
            video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"

            if self.xpath_exists(video_src):
                video_src_url = self.browser.find_element_by_xpath(video_src).get_attribute("src")

                # save video
                name_full = video_src_url.split("/")[-1]
                self.name = name_full.split("?")[-2]
                print(self.loc)
                video = requests.get(video_src_url, stream=True)
                name = current_app.root_path + "/static/insta_videos/" + self.name
                print(name)
                with open(name, "wb") as video_file:
                    for chunk in video.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            video_file.write(chunk)

                self.close_browser()
                print(f"{self.name} successfully saved!")
                return "success", self.name
            else:
                print('Error: There is no video')
                    
                self.close_browser()
                return "error", "Error: Didn't get download link"
                

            
            
        except Exception as ex:
            print(ex)
            self.close_browser()
            return "error", "Error: Didn't get download link"



def main():
    url = str(input("Enter url : "))
    parser = DownloadInsta()
    parser.download_videos(url)


if __name__ == "__main__":
    main()



