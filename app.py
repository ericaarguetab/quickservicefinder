from flask import Flask, flash, redirect, render_template, request, session 
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'quickservicefinder'

mysql.init_app(app)
con = mysql.connect()
cursor = con.cursor()

    #Obtener los datos necesarios para la consulta de insertownerservice

@app.route('/')
def hello_world():
    return render_template("register.html")