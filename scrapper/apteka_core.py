import requests
from bs4 import BeautifulSoup
import re
import csv
from playwright.sync_api import sync_playwright, expect

headers = {
	'User-Agent':
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

def clear_file(file_name):
	with open(file_name, 'w', encoding='utf-8', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Магазин', 'Категория', 'Название', 'Цена', 'Цена без скидки', 'Ссылка', 'Изображение'])

def get_dynamic_soup(url: str, selector: str|None = None) -> BeautifulSoup:
	with sync_playwright() as p:
		browser = p.chromium.launch()#headless=False)
		page = browser.new_page()
		page.goto(url, wait_until="domcontentloaded")

		if selector:
			page.evaluate("""() => {
				document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
					//const image = img;// as HTMLImageElement;
					img.setAttribute('loading', 'eager'); // Force eager loading
					//const source = image.src;
					//image.src = '';  // Reset src to reload the image
					//image.src = source; // Set src back to original
				})
			}""")

			try:
				lazy_images = page.locator(selector)
				for lazy_image in lazy_images.all():
					lazy_image.scroll_into_view_if_needed()
					expect(lazy_image).to_have_js_property('complete', True)
					expect(lazy_image).not_to_have_js_property('naturalWidth', 0)

				page.wait_for_selector(selector)
			except:
				pass

		soup = BeautifulSoup(page.content(), "html.parser")
		browser.close()
		return soup
