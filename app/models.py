# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from app import db, login_manager

class templates(UserMixin, db.Model):
    __tablename__ = 'templates'
    id=db.Column(db.Integer, primary_key=True)
    domain_name=db.Column(db.Text)
    snapshot_name=db.Column(db.Text)
    is_snapshot=db.Column(db.Boolean, index=True)
    is_templates=db.Column(db.Boolean, index=True)

class audit_trail(UserMixin, db.Model):
    weekdayname={0:'Monday',1:'Tuesday',2:'Wednesday',
                 3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    __tablename__ = 'audit_trail'
    id=db.Column(db.Integer, primary_key=True)
    datetime=db.Column(db.DateTime, index=True)
    action=db.Column(db.Text)
    location=db.Column(db.Text)
    details=db.Column(db.Text)
    success=db.Column(db.Boolean, index=True)

    def getcurrenttime(self):
        return datetime.datetime.today()
    @property
    def date_time(self):
        today=self.getcurrenttime()
        return today.strftime("%A, %d-%B-%Y, %I:%M:%S %p")

    def get_date(self, userdatetime):
        return 

    def get_weekday(self, userdatetime):
        return

    def get_time(self, userdatetime):
        pass

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)