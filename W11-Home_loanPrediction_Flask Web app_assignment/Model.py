from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates')

ENV = 'dev'

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipanwita123@localhost:3306/login_store'
app.config['SECRET_KEY'] = 'giveanysceretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## Create tables in the database
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
db.create_all()

## Create tables in the database
class UserDetails(db.Model, UserMixin):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user_name = db.Column(db.String(20), db.ForeignKey(User.username))
    gender = db.Column(db.String(6), nullable=False)
    married = db.Column(db.String(20), nullable=False)
    dependents = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(20), nullable=False)
    self_employed = db.Column(db.String(10), nullable=False)
    applicantincome = db.Column(db.Integer, nullable=False)
    coapplicantincome = db.Column(db.Integer, nullable=False)
    loanamount = db.Column(db.Integer, nullable=False)
    loan_amount_term = db.Column(db.Integer, nullable=False)
    credit_history = db.Column(db.String(20), nullable=False)
    property_area = db.Column(db.String(20), nullable=False)
    applicationStatus = db.Column(db.String(20), nullable=False)

    def __init__(self, user_name, user_id, gender, married, dependents, education, self_employed, applicantincome, coapplicantincome,
                 loanamount, loan_amount_term, credit_history, property_area, applicationStatus):
        self.user_id = user_id
        self.user_name = user_name
        self.gender = gender
        self.married = married
        self.dependents = dependents
        self.education = education
        self.self_employed = self_employed
        self.applicantincome = applicantincome
        self.coapplicantincome = coapplicantincome
        self.loanamount = loanamount
        self.loan_amount_term = loan_amount_term
        self.credit_history = credit_history
        self.property_area = property_area
        self.applicationStatus = applicationStatus



db.create_all()

