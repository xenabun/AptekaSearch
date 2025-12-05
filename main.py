from flask import Flask, request, render_template
import pandas as pd
import requests

app = Flask(__name__)

data_path = "data/data.csv"
shops = {'magnit': 'Магнит', 'rigla': 'Ригла', 'aptekaru': 'Аптека Ру'}
categories = {'dermacosmetika': 'Дермакосметика', 'dlapishevoreniya': 'Для пищеварения', 'vitaminiibad': 'Витамины и БАД'}
api_url = "https://maude-wardless-reba.ngrok-free.dev/api/"

# def read_data():
# 	items = pd.read_csv(data_path, skiprows=1)
# 	items.columns = ['shop', 'category', 'name', 'price', 'old_price', 'link', 'image']

# 	return items

# def get_price_range():
# 	items = read_data()
# 	min_price = int(items['price'].min())
# 	max_price = int(items['price'].max())

# 	return [min_price, max_price]

@app.route("/", methods=['GET', 'POST'])
def search_page():
	form_data = request.form
	price_range = [0, 0]
	items = None
	items_amount = 0
	items_show_limit = 100
	exception = None

	try:
		request_url = api_url + 'price_range'
		response = requests.get(request_url)
		data = response.json()
		print(data)
		price_range = [data.min_price, data.max_price]
	except Exception as e:
		exception = str(e)

	if len(form_data) > 0:
		print(form_data)

		try:
			request_url = api_url + 'data?'
			queries = []

			if form_data.get('shop') != 'all':
				queries.append(f'shop={shops[form_data.get('shop')]}')
			if form_data.get('category') != 'all':
				queries.append(f'category={categories[form_data.get('category')]}')
			if len(form_data.get('name')) > 0:
				queries.append(f'name={form_data.get('name')}')
			if form_data.get('discount') == 'on':
				queries.append(f'discount=true')
			queries.append(f'min_price={form_data.get('min_price')}')
			queries.append(f'max_price={form_data.get('max_price')}')

			response = requests.get(request_url + '&'.join(queries))
			items = response.json()
		except Exception as e:
			exception = str(e)

		# items = read_data()

		# if form_data.get('shop') != 'all':
		# 	items = items[items['shop'] == shops[form_data.get('shop')]]
		# if form_data.get('category') != 'all':
		# 	items = items[items['category'] == categories[form_data.get('category')]]
		# if len(form_data.get('name')) > 0:
		# 	items = items[items['name'].str.contains(form_data.get('name'), case=False)]
		# if form_data.get('discount') == 'on':
		# 	items = items[items['price'] < items['old_price']]
		# items = items[items['price'] >= float(form_data.get('min_price'))]
		# items = items[items['price'] <= float(form_data.get('max_price'))]

		# items_amount = len(items)
		# items = list(items.head(items_show_limit).values)

	return render_template('index.html',
						exception=exception,
						items=items,
						items_amount=items_amount,
						items_show_limit=items_show_limit,
						price_range=price_range)
