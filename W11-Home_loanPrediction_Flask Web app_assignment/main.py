from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from predict.predict_views import predict_view
import json
import pandas as pd
from Model import UserDetails, User


app = Flask(__name__, template_folder='templates')
model = pickle.load(open('model.pkl', 'rb')) # loading the trained model

ENV = 'dev'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipanwita123@localhost:3306/login_store'
app.config['SECRET_KEY'] = 'giveanysceretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

## for managing our application and Flask_login to work together
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

## To reload the objects from the user_ids stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

## Create tables in the database
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

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

db.create_all()


## Create a RegisterForm
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


## Create a loginform
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('prediction.enter_details'))
    return render_template('login.html', form=form)


## hashing the password is optional for the learners
@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) ## creates a password hash
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/get_user_count')
def get_user_count():
    return redirect(url_for('user_count'))

# CREATE THE METADATA OBJECT TO ACCESS THE TABLE
@app.route('/user_count')
def user_count():
    result = db.session.query(User).count()
    return jsonify({'Number of registered users': result})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_summary_of_all_user')
def get_all_user_summary():
    df = pd.read_sql_table('user_details',con=db.get_engine())
    result = df.to_json(orient="index")
    return_result = json.loads(result)
    json.dumps(return_result, indent=4)
    return jsonify({'Statistical Summary Of All Registered Users':return_result})


@app.route('/get_percentage_of_approved_loan')
def get_percentage_of_approved_loan():
    approved_count = UserDetails.query.filter(UserDetails.applicationStatus=='1').count()
    total_count = db.session.query(UserDetails).count()
    if(total_count==0):
        approved_percentage=0
    else:
        approved_percentage = (approved_count*100)/total_count
    return jsonify({'Percentage Of Approved Loan': approved_percentage})

# register the blueprints
app.register_blueprint(predict_view)

if __name__ == "__main__":
    app.run(debug=True,port=6622)
    app.config['TEMPLATES_AUTO_RELOAD'] = True