 #!/user/bin/python

"""

##################################################
##												##
## 	GRUBHUB SCRAPE: MIN WAGE AND CAL POST		##
## 					PROJECTS					##
##	Chelsea Crain								##
##	12/07/16									##
##												##
## 	This program goes through the list of 		##
## 		neighborhoods and scrapes  				##
##		main pages and menu pages of all 		##
##		all restaurants located in those areas.	##
##												##
##################################################


"""

from __future__ import print_function, division
from lxml import html
import csv, sys
from itertools import izip_longest
from os.path import join, dirname, realpath
import pandas as pd
from os import path
from datetime import date
import os
import time 
import time, os, re, codecs, math, random, csv, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import sys
import uuid


delay = 15

general_path = "F:\\Boulder_Scrapes" 

site_list = ["https://hungrybuffs.com/some/boulder/delivery/all", "https://hungrybuffs.com/some/boulder/takeout/all", "https://orderup.com/some/fort-collins/delivery/all", "https://orderup.com/some/fort-collins/takeout/all"]


def get_done_lists(area, scrape_name):

	path = general_path + "\\Scrape_" + scrape_name
	if not os.path.isdir(path):
		os.makedirs(path)
	# done_zips_name = os.path.join(path, "done_zips_" + area + ".csv")
	done_list_name = os.path.join(path, "done_list_" + area + ".csv")
	
	try:
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		#print(done_list)
	except:
		file = open(done_list_name, 'w')
		file.write("done" + "," + "\n")
		file.close()
		df = pd.read_csv(done_list_name)
		done_list = df['done'].tolist()
		
	# try:
		# df = pd.read_csv(done_zips_name)
		# done_zips = df['done'].tolist()
	# except:
		# file = open(done_zips_name, 'w')
		# file.write("done" + "," + " service notes" + "\n")
		# file.close()
		# df = pd.read_csv(done_zips_name)
		# done_zips = df['done'].tolist()
		
	return done_list, path,  done_list_name
	
def count_letters(zip):

	letters = len(zip) - zip.count(' ')
	
	if letters < 5:
		zip = "0" + str(zip)
	else:	
		zip = str(zip)
		
	print(zip)
	
	return zip

def get_driver():


	opts = Options()

	opts.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
	
	driver = webdriver.Chrome('C:\Program Files (x86)'
				'\Google\Chrome\Application\chromedriver.exe', chrome_options=opts)
	
	
	return driver


		

def get_list(driver):
	
	time.sleep(3)
	
	WebDriverWait(driver, delay).until(
		EC.presence_of_element_located(
		(By.XPATH, '//*[contains(@class,"restaurant-info")]')
		))
	
	url_list = []

	time.sleep(1)
	
	text = driver.find_element_by_xpath('.//html[@class]').text
	text = text.encode('utf-8').strip()
	if "An error occurred" in text: 
		sys.exit()
	
	restaurants_on_page = len(driver.find_elements_by_xpath('//*[contains(@class,"restaurant-info")]'))
			
	i = 0
	while i < (restaurants_on_page):
		url = str(driver.find_elements_by_xpath('//*[contains(@class,"restaurant-info")]//a')[i].get_attribute('href'))
		url_list.append(url)	
		i+=1
	
	url_list = [ el for el in url_list if "yelp.com/biz" not in el]
	
	print("total restaurants: %s" %len(url_list))
	
	return(url_list)

	
def prep_file(path, area):

	output_path = path + "\\menus"
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	id = str(uuid.uuid4())
	print(id)
	# visible_text_file = open(os.path.join(output_path, id + ".txt"), "w")
	html_file = open(os.path.join(output_path, id ), "w")
	
	return  html_file
					
def download_menu_info(driver, url, path, area):

	driver.get(url)
	
	WebDriverWait(driver, delay).until(
		EC.presence_of_element_located(
		(By.CLASS_NAME, "item-title")
		))

	html_file = prep_file(path, area)
	
	visible_text = driver.find_element_by_xpath('.//html[@class]').text
	visible_text = visible_text.encode('utf-8').strip()
	if "An error occurred" in visible_text: # check to make sure connected to internet 
		sys.exit()
	# visible_text_file.write(visible_text)
	# visible_text_file.close()
	
	html_text = driver.page_source
	html_text = html_text.encode('utf-8').strip()
	html_file.write(html_text)
	html_file.close()	


def main(area, scrape_name):

	
	try:	
		done_list, path, done_list_name = get_done_lists(area, scrape_name)
			
		print("Number of menus downloaded: %s" % len(done_list))

		driver = get_driver()
		
		for site in site_list:
			driver.get(site)
			
			print("Starting on site %s" %site)
			
			## GO THROUGH AND MAKE LIST OF ALL RESTAURANT URLS #####
			url_list = get_list(driver)
			random.shuffle(url_list)
		
			print("Starting to save menu info")
				
			## DOWNLOAD INFO FROM ALL RESTAURANT LINKS IN ZIP CODE LIST ####
			for url in url_list:
				if url in done_list:
					print("already got this one")
					continue
				else:
					print(url)
					download_menu_info(driver, url, path, area)
				
				done_list_file = open(done_list_name, 'a')
				done_list_file.write(url + "\n")
				done_list_file.close()
				done_list.append(url)	
				service_status = ""
				

		
		print("ALL DONE!!!!")
			
	except:
		sys.exit()
		
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
	