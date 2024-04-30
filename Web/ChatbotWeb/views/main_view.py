from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__, url_prefix='/')

