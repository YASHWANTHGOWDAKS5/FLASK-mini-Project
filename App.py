from flask import render_template, redirect,flash, url_for, jsonify
from flask_wtf import FlaskForm
from pymongo.common import validate_string_or_none
from sqlalchemy.orm import declarative_base, sessionmaker
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from sqlalchemy import create_engine, Column, Integer, String
import re
from werkzeug.security import generate_password_hash
from flask import Flask

app= Flask(__name__)
app.config['SECRET_KEY'] = 'JaiBajarangi@25'

class Form(FlaskForm):
    Name=StringField('Name',validators=[DataRequired(),Length(max=20,min=5)])
    Age=IntegerField('Age',validators=[DataRequired()])
    Gender=StringField('Gender',validators=[DataRequired('Male' or 'Female')])
    email=StringField('Email',validators=[DataRequired("Enter you'r Correct Email"),])
    Phone=IntegerField('Phone',validators=[DataRequired('Enter your Phone Number')])
    Password=PasswordField('Password',validators=[DataRequired('Enter your Password')])
    submit = SubmitField('Sign Up')
engine= create_engine('mysql+pymysql://root:@localhost/LoginPage_Data')
Base=declarative_base()

class LoginForm(Base):
    __tablename__='LoginForm_Data'
    id=Column(Integer,primary_key=True,autoincrement=True)
    Name = Column(String(20))
    Age = Column(Integer)
    Gender = Column(String(10))
    email = Column(String(20))
    Phone = Column(Integer)
    Password = Column(String(20))
    Hash_PassKey=Column(String(200))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session= Session()
print("Connectin Established sir.")

@app.route('/',methods=['GET','POST'])
def signup():
    form=Form()
    if form.validate_on_submit():
        name = form.Name.data
        age = form.Age.data
        gender = form.Gender.data
        email = form.email.data
        phone = form.Phone.data
        password = form.Password.data
        hash_PassKey = generate_password_hash(password)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        add_obj=LoginForm(Name=name,Age=age,Gender=gender,email=email,Phone=phone,Password=password, Hash_PassKey=hash_PassKey)
        if re.match(email_pattern,add_obj.email):
            flash(f'Hello {add_obj.Name} you have registered properly by sankeths program and little help of YashuGowda')
            session.add(add_obj)
            session.commit()
            flash('Your data saved successfully bro.')
            return redirect(url_for("signup"))
        else:
            flash('Invalid formate or empty field please check you buffur....')
    return render_template('Signup.html',form=form)



class admin(FlaskForm):
    UserName = StringField('Name', validators=[DataRequired(), Length(max=20, min=5)])
    pass_key = PasswordField('Password', validators=[DataRequired()])


@app.route('/admin', methods=['GET','POST'])
def admin_log():
    adminform = admin()
    if adminform.validate_on_submit():
        username = adminform.UserName.data
        pass_key = adminform.pass_key.data
        if username in ['Yashwanth Gowda KS', 'Sanketh HN'] and pass_key == 'bajarangi@123':
            data_all = session.query(LoginForm).all()
            return render_template('admin_dashboard.html', data=data_all)
        else:
            flash("Invalid Admin Credentials")
    return render_template('admin.html', form=adminform)


@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = session.query(LoginForm).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        flash("User deleted successfully ✅")
    return redirect(url_for('admin_log'))




@app.route('/data',methods=['GET','POST'])
def Data():
    data_all=session.query(LoginForm).all()
    result = [{"id": s.id, "name": s.Name, "Age": s.Age,'Gender':s.Gender,"email":s.email,"phone":s.Phone,"password":s.Password} for s in data_all]
    return render_template('data.html',data=result)

if __name__=='__main__':
    app.run(debug=True)
