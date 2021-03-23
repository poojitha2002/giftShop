from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user


app = Flask(__name__)
bootstrap=Bootstrap(app)

app.config['SECRET_KEY']='83789b715daf10d48cbbc952305e03a2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class User(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(50),unique=True)
	password=db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class LoginForm(FlaskForm):
	username=StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
	password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
	remember=BooleanField('remember me')

class RegisterForm(FlaskForm):
	email=StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
	username=StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
	password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])



@app.route("/")
def index():
	return render_template("index.html",title="Get Started")


@app.route("/home")
@login_required
def home():
	return render_template("home.html",title="GS-Home",name=current_user.username)


@app.route('/signup',methods=['GET','POST'])
def signup():
	form=RegisterForm()
	if form.validate_on_submit():
		hashed_password=generate_password_hash(form.password.data,method='sha256')
		new_user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return '<h1>'+'New User has been created'+'</h1>'
		#return '<h1>'+form.username.data+' '+form.email.data+' '+form.password.data+'</h1>'
	return render_template("register.html",form=form,title="Join Now!!")



@app.route("/login",methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password,form.password.data):
				login_user(user,remember=form.remember.data)
				return redirect(url_for('home'))
		return '<h1>Invalid username or password</h1>'
		#return '<h1>'+ form.username.data+' '+form.password.data+'</h1>'

	return render_template("login.html",form=form,title="Login Now!!")


@app.route("/contact-us")
def contactUs():
	return render_template("contact.html",title="Contact Us")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


def about():
	return "About Us";
app.add_url_rule("/about","about",about)
	

'''
@app.route('/admin')
def hello_admin():
	return "Hello admin"
@app.route('/guest/<guest>')
def hello_guest(guest):
	return 'Hello %s as Guest' % guest
@app.route('/user/<name>')
def hello_run(name):
	if name=="admin":
		return redirect(url_for('Hello admin'))
	else:
		return redirect(url_for('hello_guest',guest=name))
@app.route('/muser/<uname>')
def give_message(uname):
	return render_template("message.html",name=uname)

@app.route('/table/<int:num>')
def table(num):
	return render_template('printTable.html',n=num)

@app.route('/success/<name>')
def success(name):
	return 'welcome %s' % name
@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		user=request.form['nm']
		return redirect(url_for('success',name=user))
	else:
		user=request.args.get('nm')
		return redirect(url_for('success',name=user))

'''





if __name__=='__main__':
	app.run(debug=True)