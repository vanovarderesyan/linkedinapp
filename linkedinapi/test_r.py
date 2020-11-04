from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.get("http://example.com/file-upload-page")
driver.find_element_by_id("id-of-uploadfile-element").send_keys("file-path")
driver.find_element_by_id("submit").click()