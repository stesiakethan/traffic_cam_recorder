from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import requests
from string import Template

url_template = Template("https://fl511.com/cctv?start=0&length=10&order%5Bi%5D=1&order%5Bdir%5D=asc&search=$name")

#Main function. run_time_seconds is used to specify the length that the program extracts the live feed from the browser session.
def live_video_scraper(camera_name , run_time_seconds):
    #Setting up the session
    url = url_template.substitute(name=camera_name.replace(" " , "+"))
    capabilities = DesiredCapabilities.CHROME
    #Lets us collect the performance log from the browser session
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    #Keeps the browser open after program quits
    options.add_experimental_option("detach", True)
    #Makes us look less like a bot
    options.add_argument('--disable-blink-features=AutomationControlled')
    #Makes it so no browser window pops up when the program runs
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options , service=Service(ChromeDriverManager().install()) , desired_capabilities=capabilities)
    
    #Opening web page and starting the stream
    driver.get(url)
    time.sleep(3)
    play_button = driver.find_element(By.XPATH, "//*[contains(@id, 'showVideo')]")
    play_button.click()
    
    #Setting a timer for the while loop that extracts the live feed
    flag = time.time() + run_time_seconds

    #Used to format the network response into JSON
    def process_browser_log_entry(entry):
        response = json.loads(entry['message'])['message']
        return response

    #Using this list to collect .ts url's from the performance log in the below while loop
    url_list = []

    #Using this list to keep track of which .ts files we've downloaded
    downloaded_urls = []

    #Constructing the file name to save the video footage to, making sure it's always unique
    filename = f"{url.split('search=' , 1)[1]} - {time.time()}"

    #Compiles an mpeg file from the stream of .ts files we collect from the performance log
    #Got most of the code for this function from https://medium.com/swlh/scraping-live-stream-video-with-python-b7154b1fedde
    def ts_downloader(ts_link):
        content = requests.get(ts_link , stream=True , verify=False)
        if content.status_code == 200:
            with open(f"Video/{filename}.mpeg" , "ab") as f:
                for chunk in content.iter_content(chunk_size=1024):
                    f.write(chunk)
            downloaded_urls.append(ts_link)
        else:
            print("Unexpected status code")

    #Extracting the video feed from the browser session
    while time.time() < flag:
        #Gets performance log from browser session
        browser_log = driver.get_log('performance') 
        #Creates a json log for all events from the performance log
        events = [process_browser_log_entry(entry) for entry in browser_log]
        for event in events:
            #Checks if the event contains a video file download URL
            try:
                if ".ts" in event["params"]["request"]["url"]:
                    #Formats the download url
                    link = (event["params"]["request"]["url"])[:(event["params"]["request"]["url"]).index(".ts") + len(".ts")]
                    #Checks if we've already collected the URL from a different event
                    if url not in url_list:
                        url_list.append(link)
                    else:
                        pass
                else:
                    pass
            except KeyError:
                pass

        #Downloading the .ts video files
        for link in url_list:
            if link not in downloaded_urls:
                ts_downloader(link)
            else:
                pass

        time.sleep(1)

    print(downloaded_urls)

    #Quits the session
    driver.quit()


#Uncomment this command and specify which camera to record along with the amount of seconds you want to record for. You can use either the description1
#or description2 values from the camera_list JSON file, or simply find a camera's name you want to record on fl511.com
#Footage will be saved to the "Video" folder within the program's files.
#live_video_scraper("304-CCTV", 60)