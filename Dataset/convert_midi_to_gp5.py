from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib
import os

def convert_dir_to_gp5(out_dir):
	driver = webdriver.Chrome()
	driver.get("http://tabplayer.online/")
	input = driver.find_element_by_tag_name("input")
	for file in os.listdir(out_dir):
		if ".gp5" in file:
			input.send_keys(os.path.abspath(out_dir + file))
			time.sleep(2)
			download= driver.find_element_by_id("downloader-mid").get_attribute("href")
			link = out_dir + file[:-4] + ".mid"
			urllib.urlretrieve(download,link)
			#Delete gp5
			os.remove(out_dir + file)