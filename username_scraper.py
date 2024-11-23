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
        noReset=True,
        newCommandTimeout=3000,
    )

    appium_server_url = f'http://localhost:{appium_port}'
    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    driver.implicitly_wait(5)

    driver.get(f"https://www.tiktok.com/@{target}")
    
    # Navigate to the desired page
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
    clicked_profiles = set()  # Set to track clicked profiles
    previous_length = 0
    index = 0
    
    username_list = []

    while True:
        # Locate all profiles on the current screen
        profiles = driver.find_elements(AppiumBy.XPATH, value='//*[@resource-id="com.zhiliaoapp.musically:id/jym"]')

        for profile in profiles:
            profile_text = profile.text

            # Skip if the profile was already clicked
            if profile_text in clicked_profiles:
                continue

            # Add profile to the main set and click
            profile_set.add(profile_text)
            clicked_profiles.add(profile_text)

            try:
                profile.click()  # Click the profile
                profile_username = driver.find_element(AppiumBy.XPATH, value='//*[@resource-id="com.zhiliaoapp.musically:id/lsp"]').text
                print(profile_username)
                username_list.append(profile_username)
                driver.back()  # Navigate back
                sleep(1)  # Allow some time to return to the list
            except Exception as e:
                print(f"Error clicking profile {profile_text}: {e}")
        
        if index > 3:
            break

        # Break if no new profiles are found
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
        start_y = screen_size['height'] * 0.85
        end_x = screen_size['width'] / 2
        end_y = screen_size['height'] * 0.15
        driver.swipe(start_x, start_y, end_x, end_y, 500)
        
        sleep(0.1)  # Add a delay to allow elements to load

    username_list = list(set(username_list))
    print(username_list)
    print(f"Total unique profiles scraped: {len(username_list)}")
    return username_list

# main("maxwell")

