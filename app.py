from flask import Flask, flash, redirect, render_template, request, session, json, jsonify
from flaskext.mysql import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, user_isowner

app = Flask(__name__)
	
app.secret_key = 'QSFEMAB'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'quickservicefinder'

mysql.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registerCustomer', methods=['GET', 'POST'])
def registerCustomer():

    if request.method == "POST":
        name = request.form['cnames']
        surnames = request.form['csurnames']
        sex = request.form['csex']
        phonenumber1 = request.form['cphonenumber1']
        phonenumber2 = request.form['cphonenumber2']
        email = request.form['cemail']
        username = request.form['cusername']
        password = request.form['cpassword']
        confirmpsswd = request.form['cconfirmpsswd'] 

        if not name and not surnames and not sex and not phonenumber1 and not email and not username and not password and not confirmpsswd:
            return jsonify({
                'responseCode': 400,
                'responseMessage': 'Enter the required fields!'
                })

        con = mysql.connect()
        cursor = con.cursor()

        _hashed_password = generate_password_hash(password)
        cursor.callproc('customer_InsertCustomer',(username, _hashed_password, email, name, surnames, sex, phonenumber1, phonenumber2))

        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return jsonify({
                'responseCode': 200,
                'responseMessage': 'Usuario creado exitosamente.',
            })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': str(data[0]),
                })

        cursor.close()
        con.close()
    else:
        return render_template("register.html")

@app.route('/registerOwner', methods=['GET', 'POST'])
def registerOwner():

    if request.method == "POST":
        names = request.form['ownames']
        surnames = request.form['owsurnames']
        sex = request.form['owsex']
        phonenumber1 = request.form['owphonenumber1']
        phonenumber2 = request.form['owphonenumber2']
        email = request.form['owemail']
        username = request.form['owusername']
        password = request.form['owpassword']
        confirmpsswd = request.form['owconfirmation'] 

        if not names and not surnames and not sex and not phonenumber1 and not email and not username and not password and not confirmpsswd:
            return jsonify({
                'responseCode': 400,
                'responseMessage': 'Enter the required fields!'
                })

        con = mysql.connect()
        cursor = con.cursor()

        _hashed_password = generate_password_hash(password)
        cursor.callproc('ownerService_InsertOwnerService',(username, _hashed_password, email, names, surnames, sex, phonenumber1, phonenumber2))

        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return jsonify({
                'responseCode': 200,
                'responseMessage': 'Usuario creado exitosamente.',
            })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': str(data[0]),
                })
        cursor.close()
        con.close()
    else:
        return render_template("register.html")

@app.route('/newService', methods=['GET', 'POST'])
@login_required
@user_isowner
def newService():
    if request.method == "POST":
        idowner = session["user_id"]
        servicename = request.form['servicename']
        servaddress = request.form['servaddress']
        servdescription = request.form['servdescription']
        subsector = request.form['servsubsector']

        if not servicename and not servaddress and not servdescription:
            return jsonify({
                'responseCode': 400,
                'responseMessage': 'Enter the required fields!'
                })

        con = mysql.connect()
        cursor = con.cursor()
        
        cursor.callproc('service_InsertService',(idowner, subsector, servicename, servaddress, servdescription))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return jsonify({
                'responseCode': 200,
                'responseMessage': 'Servicio creado exitosamente.',
            })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': str(data[0]),
                })
        
        cursor.close()
        con.close()
      
    else:
        con = mysql.connect()
        cursor = con.cursor()

        cursor.callproc('subsector_GetSubsector')
        result = cursor.fetchall() 

        return render_template("serviceRegister.html", result=result)

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():

    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']

        if not user and not password:
            return jsonify({
                'responseCode': 400,
                'responseMessage': 'Enter the required fields!'
                })

        con = mysql.connect()
        cursor = con.cursor()

        cursor.callproc('customer_validateCustomer',(user,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),password):
                session['user_id'] = data[0][0]
                session['user_name'] = data[0][2]
                session['is_owner'] = False
                return jsonify({
                    'responseCode': 200,
                    'responseMessage': "Usuario encontrado",
                    })
            else:
                return jsonify({
                    'responseCode': 500,
                    'responseMessage': "Contraseña incorrecta",
                    })
        
        cursor.callproc('ownerservice_validateOwnerService',(user,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),password):
                session['user_id'] = data[0][0]
                session['user_name'] = data[0][2]
                session['is_owner'] = True
                return jsonify({
                    'responseCode': 200,
                    'responseMessage': "Usuario encontrado",
                    })
            else:
                return jsonify({
                    'responseCode': 500,
                    'responseMessage': "Contraseña incorrecta",
                    })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': "Contraseña o usuario incorrecto",
                })

    else:
        return render_template("signIn.html")

@app.route('/logOut', methods=['POST'])
def logOut():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('is_owner', None)
    return redirect('/signIn')