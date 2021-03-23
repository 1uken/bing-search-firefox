# Bing Search Python Script for Firefox Desktop/Mobile
# Requires Selenium - pip install selenium
# Requires Firefox Gecko Webdriver - https://github.com/mozilla/geckodriver/releases
# Note: The webdriver requires Microsoft Visual Studio redistributable runtime - 
# https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

import time
import random
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as ex

# Write a message to timestamped log file
def printLog(message):
    my_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    file_name = os.path.splitext(os.path.basename(__file__))[0] + '.log'
    with open(file_name, 'a+') as logfile:
        logfile.write(my_timestamp + "\t" + message + '\n')
        print(my_timestamp + "\t" + message)

# Attempt to quit the web driver and close all child windows
def closeWebDriver():
    try:
        driver.quit()
    except NameError:
        printLog("Cannot close webdriver instance; does not exist. Skipping...")
        pass

# Gracefully exit the script
def exitScript(sec=10):
    printLog("Exiting script in {0} seconds...\n".format(sec))
    time.sleep(sec)
    closeWebDriver()
    exit()

# Handle exception and log where it occured, then exit the script
def handleException(e, phase):
    printLog("EXCEPTION: " + str(type(e)))
    printLog(str(e))
    printLog("Error occurred during {0}!".format(phase))
    exitScript()

# Create web driver instance and handle exceptions; uses recursion; limit 3 tries
def createWebDriverRecursive(profile, driver_path, attempt=3):
    if (attempt > 0):
        try:
            return webdriver.Firefox(firefox_profile=profile, executable_path=driver_path)
        except Exception as e:
            printLog("EXCEPTION: " + str(type(e)))
            printLog(str(e))
            printLog("Reloading webdriver in 5 seconds...")
            time.sleep(5)
            closeWebDriver()
            return createWebDriverRecursive(profile, driver_path, attempt - 1)
    else:
        raise Exception("All attempts at reloading webdriver failed.")

# Create web driver instance and handle exceptions; limit to 3 tries
def createWebDriver(profile, driver_path, attempt=3):
    while (attempt > 0):
        try:
            return webdriver.Firefox(firefox_profile=profile, executable_path=driver_path)
        except Exception as e:
            printLog("EXCEPTION: " + str(type(e)))
            printLog(str(e))
            printLog("Attempting to reload webdriver in 5 seconds...")
            time.sleep(5)
            closeWebDriver()
            attempt -= 1
            continue
    raise Exception("All attempts at reloading webdriver failed.")

# Retrieves a webpage and handle exceptions; uses recursion; limit 3 tries
def loadWebPageRecursive(url, attempt=3):
    if (attempt > 0):
        try:
            driver.get(url)
        except Exception as e:
            printLog("EXCEPTION: " + str(type(e)))
            printLog(str(e))
            printLog("Reloading webpage in 5 seconds...")
            time.sleep(5)
            loadWebPageRecursive(url, attempt - 1)
    else:
        raise Exception("All attempts at reloading webpage timed out.")

# Retrieves a webpage and handle exceptions; limit to 3 tries
def loadWebPage(url, attempt=3):
    while (attempt > 0):
        try:
            return driver.get(url)
        except Exception as e:
            printLog("EXCEPTION: " + str(type(e)))
            printLog(str(e))
            printLog("Attempting to reload webpage in 5 seconds...")
            time.sleep(5)
            attempt -= 1
            continue
    raise Exception("All attempts at reloading webpage timed out.")


# SCRIPT STARTS HERE
# Load variables from external configuration text/file
try:
    file_name = os.path.splitext(os.path.basename(__file__))[0] + '.config'
    file_path = Path(file_name)

    # Load config file and split text into tokens/words
    with open(file_path, 'r') as config_file:
        list_of_words = config_file.read().split()

    num_loaded = 0
    num_total = 8
    # Look for the settings we care about and try to parse
    for index, word in enumerate(list_of_words):
        if (word == "run_mode" and list_of_words[index + 1] == "="):            # 1
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                run_mode = int(list_of_words[index + 2][1:-1])
                num_loaded += 1
        elif (word == "desktop_search" and list_of_words[index + 1] == "="):    # 2
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                desktop_search = int(list_of_words[index + 2][1:-1])
                num_loaded += 1
        elif (word == "mobile_search" and list_of_words[index + 1] == "="):     # 3
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                mobile_search = int(list_of_words[index + 2][1:-1])
                num_loaded += 1
        elif (word == "profile_path" and list_of_words[index + 1] == "="):      # 4
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                profile_path = Path(list_of_words[index + 2][1:-1])
                num_loaded += 1
        elif (word == "driver_path" and list_of_words[index + 1] == "="):       # 5
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                driver_path = Path(list_of_words[index + 2][1:-1])
                num_loaded += 1
        elif (word == "auto_login" and list_of_words[index + 1] == "="):        # 6
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                auto_login = (list_of_words[index + 2][1:-1] == "True")
                num_loaded += 1
        elif (word == "my_username" and list_of_words[index + 1] == "="):       # 7
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                my_username = list_of_words[index + 2][1:-1]
                num_loaded += 1
        elif (word == "my_password" and list_of_words[index + 1] == "="):       # 8
            if (list_of_words[index + 2][0] == "\"" and list_of_words[index + 2][-1] == "\""):
                my_password = list_of_words[index + 2][1:-1]
                num_loaded += 1
        else:
            pass
    if (num_loaded != num_total):
        raise Exception("Expected {0} settings but {1} were found!".format(num_total, num_loaded))
except Exception as e:
    handleException(e, "CONFIGURATION")

# Main script functionality loop
login_flag = False
for loop in range(2):
    # Initialization and setup
    try:
        if (run_mode == 1 or run_mode == 3):
            printLog("*** Bing Search Python Script for Firefox Desktop ***")
        elif (run_mode == 2):
            printLog("*** Bing Search Python Script for Firefox Mobile ***")
        else:
            raise Exception("Run mode value is invalid! Must be 1, 2, or 3.")
        
        printLog("Creating profile...")
        profile = webdriver.FirefoxProfile(profile_path)
        # Set user-agent to Edge browser
        profile.set_preference('general.useragent.override', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.48")
        if (run_mode == 2):
            # Set user-agent to Chrome on Android
            profile.set_preference('general.useragent.override', "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36")
        profile.set_preference('dom.webnotifications.enabled', False)
        profile.set_preference('app.update.enabled', False)
        profile.set_preference('geo.enabled', False)
        printLog("Profile created.")
        printLog("Loading webdriver...")
        driver = createWebDriver(profile, driver_path)
        driver.set_page_load_timeout(10)
        printLog("Webdriver loaded.")
    except Exception as e:
        handleException(e, "INITIALIZATION")

    # Microsoft account login/authentication
    if (auto_login == True and login_flag == False):
        try:
            printLog("Opening login page and waiting for 10 seconds...")
            loadWebPage('https://login.live.com/')
            time.sleep(10)
            printLog("Entering username and waiting for 5 seconds...")
            username_element = driver.find_element_by_name('loginfmt')
            username_element.clear()
            username_element.send_keys(my_username)
            username_element.send_keys(Keys.RETURN)
            time.sleep(5)
            printLog("Entering password and waiting for 10 seconds...")
            password_element = driver.find_element_by_name('passwd')
            password_element.clear()
            password_element.send_keys(my_password)
            password_element.send_keys(Keys.ENTER)
            time.sleep(10)
            printLog("Finished login/authentication.")
            login_flag = True   # Set to False to always force login
        except Exception as e:
            handleException(e, "AUTHENTICATION")

    # Auto-search with randomized Bing queries
    try:
        printLog("Opening Bing homepage and waiting for 10 seconds...")
        loadWebPage('https://www.bing.com')
        time.sleep(10)
        printLog("Opening Rewards page and waiting for 10 seconds...")
        loadWebPage('https://account.microsoft.com/rewards/')
        time.sleep(10)

        # Set 'word_path' to path of the word list text file (should be in root directory)
        word_path = Path('.\\10K-english-longwords.txt')
        with open(word_path, 'r') as word_list:
            if (run_mode == 1 or run_mode == 3):
                # Create list for desktop searches
                random_words = random.sample(word_list.read().splitlines(), desktop_search)
            elif (run_mode == 2):
                # Create list for mobile searches
                random_words = random.sample(word_list.read().splitlines(), mobile_search)
            else:
                raise Exception("Run mode value is invalid! Must be 1, 2, or 3.")
        printLog("{0} words selected from {1}".format(len(random_words), word_path))

        url_base = 'https://www.bing.com/search?q='
        for num, word in enumerate(random_words):
            printLog("{0}. URL : {1}".format(str(num + 1), url_base + word))
            loadWebPage(url_base + word)
            try:
                printLog('\t' + driver.find_element_by_tag_name('h2').text)
            except Exception as e:
                printLog("EXCEPTION: " + str(type(e)))
                printLog(str(e))
                printLog("Suppressing exception type...")
            delay = random.randint(5,15)
            printLog("Waiting for {0} seconds...".format(delay))
            time.sleep(delay)
            
        if (run_mode == 1):
            printLog("Desktop searches successfully completed!")
            exitScript()
        elif (run_mode == 2):
            printLog("Mobile searches successfully completed!")
            exitScript()
        elif (run_mode == 3):
            printLog("Desktop searches successfully completed!")
            printLog("Switching to mobile searches in 10 seconds...")
            time.sleep(10)
            closeWebDriver()
            run_mode = 2
        else:
            raise Exception("Run mode value is invalid! Must be 1, 2, or 3.")
    except Exception as e:
        handleException(e, "AUTO-SEARCH")