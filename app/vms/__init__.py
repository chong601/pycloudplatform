# app/vms/__init__.py

from flask import Blueprint

vms = Blueprint('vms', __name__)

from . import views