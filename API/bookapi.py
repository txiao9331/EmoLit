from flask import Flask, abort, request, render_template
import pymysql
import os
import math
from collections import defaultdict
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/choice_books',
    api_url='/static/bookapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)

def create_db_conn():
    db_conn = pymysql.connect(host="localhost"
                            , user="root"
                            , password=os.getenv('mysql_xt')
                            , database="littmental" 
                            , cursorclass=pymysql.cursors.DictCursor)
    return db_conn

@app.route('/v1')
def index():
    return render_template('index.html')



def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}

def get_last_page(query,page_size):
    db_conn=create_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(query)    
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    db_conn.close()
    return last_page   
