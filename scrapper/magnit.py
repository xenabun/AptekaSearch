import apteka_core as scrapper
import requests
from bs4 import BeautifulSoup
import re
import csv

## MAGNIT

file_name = '../data/magnit.csv'
shop = 'Магнит'
url = 'https://apteka.magnit.ru'
MAGNIT_page_url = '?page={}'
MAGNIT_categories = {
	'Дермакосметика': '/catalog/ukhod/dermacosmetika',
	'Для пищеварения': '/catalog/lekarstva/zheludok_kishechnik_pechen',
	'Витамины и БАД': '/catalog/vitaminy_i_bad',
}

scrapper.clear_file(file_name)

def MAGNIT_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=scrapper.headers)
	soup = BeautifulSoup(response.content, "html.parser")
	
	pagination = soup.select_one('nav[class="catalog-pagination"]')
	
	last_page_button = pagination.find('div').select_one('a:nth-last-child(2)')
	last_page_span = last_page_button.select_one('span[class="pl-button__title"]')
	last_page_text = last_page_span.text
	last_page = int(last_page_text)
	
	return last_page

def MAGNIT_scrape_product_info(product, category):
	name_tag = product.select_one('p[class*="product-card__title"]')
	price_tag = product.select_one('span[class*="product-price__current"]')
	old_price_tag = product.select_one('span[class*="product-price__previous"]')
	link_tag = product.find('a', href=True)
	image_tag_container = product.select_one('div[class="product-card__img"]')
	image_tag = image_tag_container.find('img', src=True)

	name = name_tag.text.strip()
	price = float(''.join(re.findall(r'\d+\.?\d*', price_tag.text)))
	old_price = old_price_tag != None and float(''.join(re.findall(r'\d+\.?\d*', old_price_tag.text))) or price
	link = url + link_tag['href']
	image_url = image_tag['src']

	data = [shop, category, name, price, old_price, link, image_url]

	return data

def MAGNIT_scrape():
	i = 1
	for category, category_url in MAGNIT_categories.items():
		max_page = MAGNIT_get_max_pagination(category_url)

		for cur_page in range(1, max_page + 1):
			soup = scrapper.get_dynamic_soup(
				url + category_url + MAGNIT_page_url.format(cur_page),
				'img[loading="eager"][class="custom-image__image"]'
			)
			prod_list_container = soup.select_one('ul[class="product-list"]')
			product_list = prod_list_container and prod_list_container.find_all('li')
			if not product_list: continue

			for product in product_list:
				print(f"{shop}-{category} [{cur_page}/{max_page}]: #{i}")
				i += 1
				data = MAGNIT_scrape_product_info(product, category)

				with open(file_name, 'a', encoding='utf-8', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(data)

MAGNIT_scrape()
