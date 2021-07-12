from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)

#Create db model
class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	#Create a function to return a string when we add something
	def __repr__(self):
		return '<name %r>' % self.id

subcribers = []

@app.route('/')
def index():
	title = "Taufik's Portfolio"
	return render_template("index.html", title=title)

@app.route('/about')
def about():
	names = ["John", "Mary", "Wes", "Sally"]
	return render_template("about.html", names=names)

@app.route('/subcribe')
def subcribe():
	title = "Subcribe My News Letter"
	return render_template("subcribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	email = request.form.get("email")

	subject = "Flask Subscribe"
	body = "You have been subscribed to my email newsletter"
	message = 'Subject: {}\n\n{}'.format(subject, body)
	server = smtplib.SMTP("smtp.mail.com", 587)
	server.set_debuglevel(1)
	server.starttls()
	server.login("my-mail@mail.com ", "mypassword") 
	server.sendmail("my-mail@mail.com", email, message)
	server.quit()

	if not first_name or not last_name or not email:
		error_statement = "All Form Fields Required..."
		return render_template("subcribe.html",
			error_statement=error_statement,
			first_name=first_name,
			last_name=last_name,
			email=email,
			title="Subcribe My News Letter")

	subcribers.append(f"{first_name} {last_name} | {email}")

	title = "Thank You"
	return render_template("form.html", title=title, first_name=first_name, last_name=last_name, email=email, s=subcribers)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
	title = "My Friends List"

	if request.method == "POST":
		friend_name = request.form.get('name') #or request.form['name']
		new_friend = Friends(name=friend_name)

		#push to database
		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was an error adding your friend..."
		#return "You clicked the button"

	else:
		friends = Friends.query.order_by(Friends.date_created)
		return render_template("friends.html", title=title, friends=friends)