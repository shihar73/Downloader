from selenium import webdriver
import pickle5 as pickle
from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import urlparse
import json
import insta_log


class DownloadInsta:
    def __init__(self, url, loc): 
        self.url = url
        self.loc = loc


    def dw_vid(self, url, root):
        try:
            name = urlparse(url).path[-25:]
            self.name = name
            resource = urllib.request.urlopen(url)

            if root:
                f_name = root + name
            else:
                f_name = name

            output = open(f_name, "wb")
            output.write(resource.read())
            output.close
            print(f_name, 'download successful')
            return "successful"
        except:
            print("Error: Download Failed check url or location")
            return "error"


    def download(self):
        try:
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)
            driver.get('https://www.instagram.com/')
            try:
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
            except:
                print("get cookies")
                log = insta_log.cookies()
                log.get_cookie()
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)

            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            main_data = json.loads(soup.find("body").text)
            data = main_data['graphql']['shortcode_media']

            is_video = data['is_video']

            if is_video:
                dw_url = data['video_url']
                msg = self.dw_vid(dw_url, self.loc)
                driver.quit()
                if msg == "error":
                    print("Error: Download failed")
                    return "error", "Error: Download failed"

                return "success", self.name
            else:
                dw_url = data['display_url']
                msg =self.dw_vid(dw_url, self.loc)
                driver.quit()
                if msg == "error":
                    print("Error: Download failed")
                    return "error", "Error: Download failed"
                
                return "success", self.name
        except:
            print("Error: Didn't get download link")
            driver.quit()
            return "error", "Error: Didn't get download link"


    
def main():
    loc =str(input("Enter location (Default : /root/Downloads/): "))
    url = str(input("Enter url : "))
    dw = DownloadInsta(url, loc)
    dw.download()

if __name__ == "__main__":
    main()
