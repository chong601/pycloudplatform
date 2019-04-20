from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired,NumberRange,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import re
#from ..models import Department, Role

class ModifyVMForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    vCPUs = IntegerField('CPU Core Count', validators=[DataRequired(),NumberRange(min=1,max=16,message="CPU Core Count should be between %(min)s core to %(max)s cores")])
    RAMSize = IntegerField('RAM Size (MB)', validators=[DataRequired(),NumberRange(min=1024,max=8192,message="RAM size should be between %(min)s MB to %(max)s MB")])
    submit = SubmitField('Submit')

class DeleteVMForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    pleasedeletemyvm = StringField('', validators=[DataRequired(),Regexp(r'[a-zA-Z0-9-_]+',flags=re.IGNORECASE|re.MULTILINE,message='Accepted characters are letters, numbers, dashes (-) and underscores (_)')])
    submit = SubmitField('Submit')

class SetUpVMForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    newVMName=StringField('Name', validators=[DataRequired(),Regexp(r'[a-zA-Z0-9-_]+',flags=re.IGNORECASE|re.MULTILINE,message='Accepted characters are letters, numbers, dashes (-) and underscores (_)')])
    vCPUs = IntegerField('CPU Core Count', validators=[DataRequired(),NumberRange(min=1,max=16,message="CPU Core Count should be between %(min)s core to %(max)s cores")])
    RAMSize = IntegerField('RAM Size (MB)', validators=[DataRequired(),NumberRange(min=1024,max=8192,message="RAM size should be between %(min)s MB to %(max)s MB")])
    submit = SubmitField('Submit')

class CreateSnapshotForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    snapshotName=StringField('Name', validators=[DataRequired(),Regexp(r'[a-zA-Z0-9-_]+',flags=re.IGNORECASE|re.MULTILINE,message='Accepted characters are letters, numbers, dashes (-) and underscores (_)')])
    submit = SubmitField('Submit')
    
class SetTemplateForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    snapshotName=BooleanField('Set as template?')
    submit = SubmitField('Submit')


class SampleForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
