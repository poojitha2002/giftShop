from app import db

class User(db.Model):
	uname=db.Column(db.String(100),nullable=False,unique=True)
	email=db.Column(db.String(100),nullable=False,unique=True,primary_key=True)
	img_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	pswrd=db.Column(db.String(60),nullable=False)

	def __repr__(self):
		return f"User ('{self.uname}','{self.email}','{self.img_file}')"
