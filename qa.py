from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://192.168.43.251:5000/login")

driver.find_element_by_class_name("input is-large").send_keys("C:/Users/rizky/Big_Project")