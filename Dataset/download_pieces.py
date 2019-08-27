from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import urllib
import urllib2
import os
import ssl
import time
import shutil
import codecs

#name,href,file
midis = []
#number of current file
i=0
#output directory
out_dir = "./clean_dataset/"

#setting up some download options of chrome
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory":out_dir}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

#clearing/creating output directory
if os.path.isdir(out_dir):
	shutil.rmtree(out_dir)
os.mkdir(out_dir)

#Some aux functions
def get_row(elem):
	parent_el = elem.find_element_by_xpath("..")
	if parent_el.tag_name != "tr":
		parent_el = get_row(parent_el)
	return parent_el

def get_most_recent_file(d):
	max_t = -1
	max_file = d + os.listdir(d)[0]
	for file in os.listdir(d):
		file = d+file
		if(os.path.getctime(file) > max_t):
			max_t = os.path.getctime(file)
			max_file = file
	return max_file

#Downloading the dataset

#First website

for page in range(17):
	driver.get("https://folkotecagalega.com/pezas/jotas?b_start:int="+str(page*10))
	elems = driver.find_elements_by_xpath("//a[@href]")
	for elem in elems:
	    if "midi" in elem.get_attribute("href"):
	    	parent_el = elem.find_element_by_xpath("../..")
	    	name = parent_el.find_element_by_tag_name("h2").find_element_by_tag_name("a").get_attribute("text")
	    	link = elem.get_attribute("href")
	    	file = str(i)+".mid"
	    	midis += [[name,link,file]]
	    	print(name)
	    	context = ssl._create_unverified_context()
	    	urllib.urlretrieve(link,out_dir + file, context=context)
	    	i+=1
	
#Second website

driver.get("http://perso.wanadoo.es/marco.velez/repertor/busca/ritmo.htm")
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
	if ".mid" in elem.get_attribute("href"):
		link = elem.get_attribute("href")
		row = get_row(elem)
		name = row.find_elements_by_tag_name("td")[1].find_element_by_tag_name("strong").get_attribute("innerHTML")
		print(name)
		file = str(i)+".mid"
		midis += [[name,link,file]]
		urllib.urlretrieve(link,out_dir + file)
		i+=1


#Third website

driver.get("http://www.gaitagallega.es/repertorio-de-gaita/jotas.html")
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
	if ".mid" in elem.get_attribute("href"):
		link = elem.get_attribute("href")
		row = get_row(elem)
		name = row.find_elements_by_tag_name("td")[0].get_attribute("innerHTML")
		print(name)
		file = str(i)+".mid"
		midis += [[name,link,file]]
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib2.install_opener(opener)
		f = urllib2.urlopen(link)
		local_file = open(out_dir + file, "wb")
		local_file.write(f.read())
		i+=1


#Fourth website

driver.get("https://partiturasgaitagalega.wordpress.com/partituras/partituras-en-do/")
driver.find_element_by_class_name("accept").click()
time.sleep(2)
elems = driver.find_elements_by_xpath("//a[@href]")
current_midis = []
for elem in elems:
	if "www.box.com" in elem.get_attribute("href"):
		name = elem.get_attribute("title")
		file = str(i) + ".gp5"
		link = elem.get_attribute("href")
		current_midis += [[name,link,file]]
		midis += [[name,link,file]]
		i+=1

for name,l,file in current_midis:
	print(name)
	driver.get(l)
	time.sleep(5)
	button = driver.find_element_by_css_selector(".bp-btn.bp-btn-primary")
	button.click()
	#waiting for download
	current_len = len([name for name in os.listdir(out_dir)])
	while len([name for name in os.listdir(out_dir)])==current_len:
		time.sleep(1)
	#renaming the file I downloaded
	new_file = get_most_recent_file(out_dir)
	shutil.move(new_file,out_dir + file)

#Convert gp5 files to MIDI


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


assert len(os.listdir(out_dir))==i
for f in os.listdir(out_dir):
	#check if every midi has reasonable size
	if(os.path.getsize(out_dir + f) < 1000):
		print("small file is" + f)
	#check if every file is named ".mid"
	assert f.endswith(".mid")

f = codecs.open("data_legend.txt","w",encoding="utf-8")

for name,link,file in midis:
	f.write("Name: %s , Link: %s , File: %s \n" % (name,link,file))







