from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)
from appium.options.android import UiAutomator2Options
from time import sleep

def main(target):
    udid = "127.0.0.1:21503"
    appium_port = "4738"
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName=udid,
        udid=udid,
        appPackage='com.zhiliaoapp.musically',
        appActivity='com.ss.android.ugc.aweme.splash.SplashActivity',
        # language='en',
        # locale='US',
        noReset=True,
        newCommandTimeout=3000,
    )

    appium_server_url = f'http://localhost:{appium_port}'

    # Converts capabilities to AppiumOptions instance
    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

    driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)
    driver.implicitly_wait(5)

    # driver.get("https://www.tiktok.com/@realnhlinterviews")
    driver.get(f"https://www.tiktok.com/@{target}")
    
    index = 0
    while True:
        if index > 3:
            return []
        try:
            driver.find_element(AppiumBy.XPATH, value='//*[@resource-id="com.zhiliaoapp.musically:id/d5p"]').click()
        except:
            pass
        try:
            driver.find_element(AppiumBy.XPATH, value='//*[@text="View all"]').click()
            break
        except:
            index += 1
            pass
        


    profile_set = set()
    previous_length = 0
    index = 0

    while True:
        # Locate all profiles on the current screen
        profiles = driver.find_elements(AppiumBy.XPATH, value='//*[@resource-id="com.zhiliaoapp.musically:id/jym"]')
        
        # Add unique profile texts to the set
        for profile in profiles:
            profile_set.add(profile.text)

        if index > 3:
            break
        # Break the loop if no new profiles are added
        if len(profile_set) == previous_length:
            index += 1
            print("No new profiles found. Scrolling stopped.")
        
        
        # Update the previous length
        if len(profile_set) != previous_length:
            previous_length = len(profile_set)
            index = 0
        
        # Perform the scroll
        screen_size = driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.56
        end_x = screen_size['width'] / 2
        end_y = screen_size['height'] * 0.44
        driver.swipe(start_x, start_y, end_x, end_y, 100)
        
        sleep(0.1)  # Add a delay to allow elements to load

    # Convert the set to a list and print the results
    profile_list = list(profile_set)
    print(profile_list)
    print(f"Total unique profiles scraped: {len(profile_list)}")
    return profile_list

# main("maxwell")

