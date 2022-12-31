from flask import Flask,Blueprint,render_template,request,jsonify
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import pickle
import numpy as np
import sklearn
from flask_sqlalchemy import SQLAlchemy
from Model import UserDetails, User

app = Flask(__name__, template_folder='templates')
db = SQLAlchemy(app)

predict_view = Blueprint('prediction', __name__, template_folder="templates")
model = pickle.load(open('model.pkl', 'rb')) # loading the trained model

@predict_view.route('/prediction.enter_details') ## for entering details
def enter_details():
    return render_template('predict.html')

@predict_view.route('/prediction.predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    print(prediction)
    user_data = UserDetails(user_id=current_user.id,user_name=current_user.username,gender=request.form.get('Gender'),married=request.form.get('married'),dependents=request.form.get('dependents'),education=request.form.get('education'),self_employed=request.form.get('self_employed'),
                         applicantincome=request.form.get('applicantincome'),coapplicantincome=request.form.get('coapplicantincome'),loanamount=request.form.get('loanamount'),loan_amount_term=request.form.get('loan_amount_term'),
                         credit_history=request.form.get('credit_history'), property_area=request.form.get('property_area'),applicationStatus=prediction[0])
    db.session.add(user_data)
    db.session.commit()

    if prediction==0:
        return render_template('predict.html', prediction_text='Sorry:( you are not eligible for the loan ')
    else:
        return render_template('predict.html', prediction_text='Congrats!! you are eligible for the loan')

    