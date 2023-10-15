from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.remote.webelement import WebElement
import re
import time
import os
import sys

def countdown(from_time):
  for remaining in range(from_time, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
    sys.stdout.flush()
    time.sleep(1)

class sub:
    title : str
    downloads : int
    hlink : str
    uploader : str
    count_id : int
    season_ep : str
    COLUMNS = 9

    def __init__(self, element_list : list[WebElement]):
        if len(element_list) != sub.COLUMNS:
            raise("Error, different size of table")
        
        self.title : str = element_list[0].text
        self.downloads : int = int(re.findall("\d+", element_list[4].text)[0])
        self.uploader : str = element_list[8].text
        self.season_ep : str = re.findall("\[S\d+E\d+\]" , self.title.upper())[0]
        self.hlink = element_list[4].find_element(By.TAG_NAME, 'a').get_attribute("href")
        return 
            



def download_season(season_number : int):
  global driver

  SEASON_URL = f"https://www.opensubtitles.org/en/search/sublanguageid-eng/pimdbid-436992/season-{season_number}"
  SUBS_PER_PAGE = 40

  driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe")
  driver.get(SEASON_URL)
  num_subs_in_season = int(driver.find_element(By.XPATH, '//*[@id="msg"]/span[2]/b[3]').text)
  subs_dict : dict[str, sub] = {}
  current_sub : int = 0

  pages_per_season = num_subs_in_season // SUBS_PER_PAGE 
  if num_subs_in_season % SUBS_PER_PAGE != 0:
      pages_per_season += 1

  for page in range(0, pages_per_season):
    if page:
      driver.get(f"{SEASON_URL}/offset-{SUBS_PER_PAGE*page}")
    else:
      driver.get(SEASON_URL)
    
    time.sleep(1)
    mytable = driver.find_elements(By.XPATH,'//*[@id="search_results"]/tbody/tr')
    for row in mytable:
        row_elements = row.find_elements(By.XPATH, ".//td")
        if row_elements:
          if len(row_elements) == sub.COLUMNS:
            current_sub += 1
            temp_sub = sub(row_elements)
            if temp_sub.season_ep in subs_dict:
                subs_dict[temp_sub.season_ep].append(temp_sub)
            else:
                subs_dict[temp_sub.season_ep] = [temp_sub]


  episode_list : list[sub]
  for episode_list in subs_dict.values():
    episode_list.sort(key=lambda x: x.downloads, reverse=True)
    if len(episode_list):
      driver.execute_script(f"window.open('{episode_list[0].hlink}')")

  countdown(20)
  return

def main():
  download_season(3)
  download_season(4)
  download_season(5)
  download_season(6)
  countdown(5)


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(e)