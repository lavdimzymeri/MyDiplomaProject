from email import message
import os
from flask import flash, request
from datetime import datetime
from flask.helpers import url_for
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla.view import ModelView
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, defaultload, lazyload, relationship
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import append_slash_redirect, redirect
from hms import db, login_manager, admin
        
class HMSUser(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=10000)
    
    appointment = db.relationship("Appointment")
    perscription = db.relationship("Perscription")

    def __init__(self,username,name,last_name,password,email, budget=10000):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.budget = budget 
       
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def can_purchase(self, item_obj):
        return  self.budget>=item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

    @staticmethod
    def login_valid(email, password):
        verify_user = HMSUser.query.filter_by(email=email).first()
        if verify_user is not None:
            return (verify_user.password, password)
        return False




class Appointment(db.Model, UserMixin):
    __tablename__="appointments"
    id = db.Column("appointment_id", db.Integer, primary_key=True)
    appointmentdate = db.Column(db.DateTime,unique=False,nullable=False)
    descriptions = db.Column(db.String(80), unique=False, nullable=False)
    zoom_link = db.Column(db.String(255), unique=False, nullable=True)
    hms_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column (db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
    def __init__(self,appointmentdate,descriptions,hms_user_id, doctor_id,zoom_link):
        self.appointmentdate = appointmentdate
        self.descriptions = descriptions
        self.doctor_id = doctor_id
        self.hms_user_id = hms_user_id
        self.zoom_link = zoom_link

class Perscription(db.Model, UserMixin):
    __tablename__='perscriptions'
    id = db.Column(db.Integer, primary_key=True)
    perscriptiondate = db.Column(db.DateTime,unique=False,nullable=False)
    symptoms = db.Column(db.String(255), unique=False, nullable=False)
    medicinerecipe = db.Column(db.String(255), unique=False, nullable=False)
    hms_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,perscriptiondate,symptoms,medicinerecipe,hms_user_id):
        self.perscriptiondate = perscriptiondate 
        self.symptoms = symptoms
        self.medicinerecipe = medicinerecipe
        self.hms_user_id = hms_user_id
        

class Contact(db.Model, UserMixin):
    __tablename__='contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.String(300), unique=True, nullable=False)

    def __init__(self,name,email,message):
        self.name = name 
        self.email = email
        self.message = message


class Doctor(db.Model, UserMixin):
    __tablename__='doctor'
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(80), unique=False, nullable=False)
    appointment = db.relationship("Appointment")
    hms_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hms_user = db.relationship("HMSUser")


    def __init__(self,username,name,last_name,password,email,specialization):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.specialization=specialization

admin.add_view(ModelView(Doctor, db.session))


    
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login'))

admin.add_view(MyModelView(HMSUser, db.session))



@login_manager.user_loader
def load_user(username):
    user = HMSUser.query.filter_by(username=username).first()
    if not user:
        return None
    a = HMSUser(username=user.username, name=user.name, last_name=user.last_name, password=user.password, email=user.email , budget=user.budget) #budget=user.budget
    return a

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('users.login', next=request.endpoint))