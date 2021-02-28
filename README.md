# Bing Search Python Script for Firefox Desktop/Mobile

## Purpose:
Automation of Bing searches with the Firefox browser. For educational purposes only.

## Requirements:
1. Python 3+
    * https://www.python.org/downloads/
2. Selenium
    * In your cmd/terminal type "pip install selenium" (run in admin mode)
3. Gecko Webdriver
    * https://github.com/mozilla/geckodriver/releases
    * NOTE: The webdriver may need the Microsoft Visual Studio redistributable runtime
    * https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
    
## Instructions:
1. Make appropriate changes to the "bing-search-firefox.config" file for your enviroment:
    * run_mode : (1) desktop mode, (2) mobile mode, (3) or both
    * profile_path : Firefox profile directory (usually in your home directory) (optional)
    * driver_path : Gecko webdriver binary (should be in root directory)
    * auto_login : Automatically log in to Microsoft account (optional)
    * username : Microsoft account login email/id (optional)
    * password : Microsoft account login password (optional)
2. Run the "bing-search-firefox.py" file.