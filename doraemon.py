
from selenium import webdriver
from bs4 import BeautifulSoup
from database import Database

class Scrape:
	def __init__(self):
		chromeOptions = webdriver.ChromeOptions()
		prefs = {'profile.managed_default_content_settings.images':2}
		chromeOptions.add_experimental_option("prefs", prefs)
		chromeOptions.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
		self.driver = webdriver.Chrome(chrome_options=chromeOptions)
		self.url_home = "https://doraemon.fandom.com/wiki/Category:Gadgets"

	def getGadgetList(self):
		url = self.url_home
		db = Database()
		column = ('gadget_name','url_detail','detail')
		while True:
			try:
				self.driver.get(url)
				soup = BeautifulSoup(self.driver.page_source, 'html.parser')
				gadgetList = soup.find_all('a', attrs={'class':'category-page__member-link'})
				for gadget in gadgetList:
					data_insert = []
					gadget_name = gadget.get('title')
					url_detail = "https://doraemon.fandom.com"+gadget.get('href')

					print("Getting "+gadget_name+" data")
					detail = str(self.getDetail(url_detail))
					rowData = (gadget_name, url_detail, detail)
					data_insert.append(rowData)
					insert = db.insert_into("gadget", column, data_insert)
				next_button = soup.find('a', attrs={'class':'category-page__pagination-next wds-button wds-is-secondary'})
				next_url = next_button.get('href')
				url = next_url
			except Exception as e:
				print(e)
				print("Finish")
				self.driver.quit()
				break


	def getDetail(self, url_detail):
		self.driver.get(url_detail)
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		all_text = soup.find(id="mw-content-text")
		return all_text

scrape = Scrape()
scrape.getGadgetList()