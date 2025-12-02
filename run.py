from flask import Flask, request

# Сложение: http://127.0.0.1:5000/add?a=1&b=1
# Вычитание: http://127.0.0.1:5000/sub?a=1&b=1
# Умножение: http://127.0.0.1:5000/mult?a=1&b=1
# Деление: http://127.0.0.1:5000/div?a=1&b=1

app = Flask(__name__)

@app.route("/add")
def addition():
	try:
		a = float(request.args.get('a'))
		b = float(request.args.get('b'))
		c = a + b
		return f"{a} + {b} = {c}"
	except Exception as e:
		return f"Произошла ошибка: {e}"

@app.route("/sub")
def subtruction():
	try:
		a = float(request.args.get('a'))
		b = float(request.args.get('b'))
		c = a - b
		return f"{a} - {b} = {c}"
	except Exception as e:
		return f"Произошла ошибка: {e}"

@app.route("/mult")
def multiplication():
	try:
		a = float(request.args.get('a'))
		b = float(request.args.get('b'))
		c = a * b
		return f"{a} * {b} = {c}"
	except Exception as e:
		return f"Произошла ошибка: {e}"

@app.route("/div")
def division():
	try:
		a = float(request.args.get('a'))
		b = float(request.args.get('b'))
		c = a / b
		return f"{a} / {b} = {c}"
	except Exception as e:
		return f"Произошла ошибка: {e}"

if __name__ == '__main__':
	app.run(debug=True)
