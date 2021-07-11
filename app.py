from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	title = "Taufik's Portfolio"
	return render_template("index.html", title = title)

@app.route('/about')
def about():
	names = ["John", "Mary", "Wes", "Sally"]
	return render_template("about.html", names = names)