from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time

# Make sure this path matches where Homebrew installed chromedriver
#check by doing "which chromedriver" on terminal
service = Service("/opt/homebrew/bin/chromedriver")

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

website = 'https://www.basketball-reference.com/'


# Test it out
driver.get(website)
#these all give you the search box–and these things (NAME, ID, XPATH, CLASS_NAME, cssselector) all correspond to the search bar on google.com
#find these labels via inspect
search = driver.find_element(By.NAME, "search")
#clear search bar just in case 
search.clear()



#driver.find_element(By.ID, "search-box")
#driver.find_element(By.XPATH, "//div")
#driver.find_element(By.CLASS_NAME, "btn")
search.send_keys("Philadelphia 76ers")
search.send_keys(Keys.RETURN)

try:
    strong = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="search-item-name"]/strong/a'))
    )

    
except:
    driver.quit()
    exit()

#for XPATH, the format goes from //div/strong/a because <a> is inside of <strong> which is inside <div>
strong= driver.find_element(By.XPATH, '//div[@class="search-item-name"]/strong/a')
print(strong.text)  
#for css_selector it goes div.your-class-name(space)tag within(space)tag within 
strong1= driver.find_element(By.CSS_SELECTOR, 'div.search-item-name strong a')
print(strong1.text)  

link=driver.find_element(By.LINK_TEXT, strong1.text)
try:
    #how to find link
    link = driver.find_element(By.LINK_TEXT, strong1.text)
    print("Link found:", link.get_attribute("href"))
except Exception as e:
    print("Link not found:", e)
    
#driver.page_source gives html of current page
link.click()


dropdown_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.section_heading.assoc_PHI.has_controls div.section_heading_text.sidescroll_note ul li.hasmore'))
)
print("Dropdown element found.")


temp=driver.find_element(By.CSS_SELECTOR,'div.section_heading.assoc_teams_ws_images span.section_anchor')

# Scroll the element into view to ensure it's visible
driver.execute_script("arguments[0].scrollIntoView();", dropdown_element)


driver.execute_script("arguments[0].click();", dropdown_element)

# Wait for the tooltip/dropdown item to be clickable
tooltip = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Get table as CSV')]"))
)
print("Tooltip element found:", tooltip.text)

# Click the tooltip
tooltip.click()
print("Tooltip clicked.")

print(e)
driver.quit()
exit()


csv_text=WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'When using SR data')]"))
).text
print(csv_text)

time.sleep(5)

print(driver.title)




#closes webpage

#driver.forward() driver.back() allows you to go to previous webpage and next webpage

