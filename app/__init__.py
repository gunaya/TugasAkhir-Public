from flask import render_template, request, redirect, flash, url_for, jsonify, Response, Flask
import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import numpy as np
import pymysql

import json, time

UPLOAD_FOLDER_MODEL = 'static/resource/model/'
UPLOAD_FOLDER_CITRA = 'static/resource/citra/'
FOLDER_DATASET = '/static/dataset/training/'

app = Flask(__name__)

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

subscriptions = []
app.config['UPLOAD_FOLDER_MODEL'] = UPLOAD_FOLDER_MODEL
app.config['UPLOAD_FOLDER_CITRA'] = UPLOAD_FOLDER_CITRA
app.config['FOLDER_DATASET'] = FOLDER_DATASET
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_iden_tulisantangan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

if __name__ == "__main__":
    server = WSGIServer(("", 9000), app)
    server.serve_forever()