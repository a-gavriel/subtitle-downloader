import winreg
import requests
import zipfile
import shutil
import os



def get_chrome_version()->str:
  access_registry  = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
  access_key = winreg.OpenKey(access_registry,r"SOFTWARE\Google\Chrome\BLBeacon")
  chrome_version : str = winreg.QueryValueEx(access_key,"version")[0]
  return chrome_version

def get_chromedriver_version(chrome_version)->str:
  chrome_version_main : str = chrome_version.split(".")[0]
  http_response = requests.get(f'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{chrome_version_main}')
  chromedriver_version : str = http_response.content.decode("ascii")
  return chromedriver_version


SUBFOLDER = "chromedriver-win64"
CHROMEDRIVER_FILENAME = "chromedriver.exe"


def clean_files(path_to_folder : str, clean_driver : bool)-> None:

  path_to_subfolder = os.path.join(path_to_folder, SUBFOLDER)

  if os.path.exists(path_to_subfolder):
    shutil.rmtree(path_to_subfolder)
  if os.path.exists(path_to_subfolder + ".zip"):
    os.remove(path_to_subfolder + ".zip")

  new_driver_path = os.path.join(path_to_folder, CHROMEDRIVER_FILENAME)
  if clean_driver:
    if os.path.exists(new_driver_path):
      os.remove(new_driver_path)

  return


def extract_and_clean(parent_folder):

  path_to_zip = os.path.join(parent_folder, SUBFOLDER + ".zip")

  with zipfile.ZipFile(path_to_zip) as zf:
    zf.extractall()

  sub_folder = os.path.join(parent_folder, SUBFOLDER)
  driver_path = os.path.join(sub_folder, CHROMEDRIVER_FILENAME)
  new_driver_path = os.path.join(parent_folder, CHROMEDRIVER_FILENAME)
  shutil.move(driver_path, new_driver_path)
  clean_files(parent_folder, False)

  return new_driver_path

def download_driver(chromedriver_version : str, folder_to_download) -> int:
  chromedriver_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chromedriver_version}/win64/chromedriver-win64.zip"
  filename = chromedriver_url.split("/")[-1]
  http_response = requests.get(chromedriver_url)

  if http_response.status_code != 200:
    print("Error fetching URL, http_reponse.status code:", http_response.status_code)
    exit()

  download_path = os.path.join(folder_to_download , filename)

  with open(download_path,'wb') as output_file:
    output_file.write(http_response.content)

  return download_path


def download_chromedriver(path_to_folder : str = "") -> None:

  if (path_to_folder == "") or (not os.path.isdir(path_to_folder)):
    path_to_folder = os.getcwd()

  clean_files(path_to_folder, True)

  chrome_version = get_chrome_version()
  #chrome_version_main : str = chrome_version.split(".")[0]

  chromedriver_version = get_chromedriver_version(chrome_version)
  #chromedriver_version_main : str = chromedriver_version.split(".")[0]

  download_driver(chromedriver_version, path_to_folder)
  path_to_driver : str = extract_and_clean(path_to_folder)
  print(path_to_driver)

  return path_to_driver

if __name__ == "__main__":
  download_chromedriver()