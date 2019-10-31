from flask import Flask, flash, redirect, render_template, request, session, json, jsonify
from flaskext.mysql import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, user_isowner
from datetime import datetime

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
    return render_template("home.html")

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
                    'responseOwner': session['is_owner']
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
                    'responseOwner': session['is_owner']
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

@app.route('/getSubsector')
def getSubsector():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('subsector_GetSubsector')
    subsector = cursor.fetchall()

    if not len(subsector) > 0:
        return jsonify({
            'responseCode': 500,
            'responseMessage': str(subsector[0]),
            })
   
    con.commit()

    subsector_dict = []
    for sub in subsector:
        sub_dict = {
            'id': sub[0],
            'sector': sub[1],
            'name': sub[2]}
        subsector_dict.append(sub_dict)

    return jsonify({
            'responseCode': 200,
            'responseMessage': 'Datos obtenidos exitosamente',
            'responseObject': subsector_dict
        })

@app.route('/listSubsectors')
def listSubsectors():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('subsector_GetSubsector')
    result = cursor.fetchall() 

    return render_template("listSubsectors.html", result=result)

@app.route('/listServices/<idsubsector>')
def listServices(idsubsector):
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('service_GetServiceBySubsector', [int(idsubsector)])
    result = cursor.fetchall()
    

    return render_template("listServices.html", result=result)

@app.route('/ownerServices')
def ownerServices():
    con = mysql.connect()
    cursor = con.cursor()

    user = session['user_id']

    cursor.callproc('service_GetServiceByOwner', str(user))
    result = cursor.fetchall()

    return render_template("ownerServices.html", result=result)

@app.route('/error')
def error():
     return render_template("error.html")

@app.route('/modal', methods=['GET', 'POST'])
def sendmsg():
    if request.method == "POST":
        customer = session['user_id']
        service = request.form['idservice']
        message = request.form['message']
        isaccepted = None
        date = datetime.now()
        responsemsg = None

        if not message:
            return jsonify({
                'responseCode': 400,
                'responseMessage': 'Enter the required fields!'
                })
        
        con = mysql.connect()
        cursor = con.cursor()

        cursor.callproc('notification_InsertNotification',(customer, service, [message], isaccepted, date, responsemsg))

        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return jsonify({
                'responseCode': 200,
                'responseMessage': 'Mensaje enviado',
            })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': str(data[0]),
                })
        cursor.close()
        con.close()

    else:
        return jsonify({
                'responseCode': 500,
                'responseMessage': 'No se puede realizar esta acción'
                })

@app.route('/modalRequest', methods=['GET', 'POST'])
def sendrequest():
    if request.method == "POST":
        if 'requestCheck' in request.form:
            requestCheck = 1
        else:
            requestCheck = 0

        service = request.form['idnotification']
        message = request.form['message']

        con = mysql.connect()
        cursor = con.cursor()        

        cursor.callproc('notification_UpdateRequest',(service, requestCheck, [message]))
        data = cursor.fetchall()

        if len(data) is 0:
            con.commit()
            return jsonify({
                'responseCode': 200,
                'responseMessage': 'Mensaje enviado',
            })
        else:
            return jsonify({
                'responseCode': 500,
                'responseMessage': str(data[0]),
                })
        cursor.close()
        con.close()

    else:
        return jsonify({
                'responseCode': 500,
                'responseMessage': 'No se puede realizar esta acción'
                })

@app.route('/notificationOwner/<idservice>')
def notificationOwner(idservice):
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('notification_GetPendingNotifications', [int(idservice)])
    result = cursor.fetchall()
    
    return render_template("notificationOwner.html", result=result)

@app.route('/notifications')
def notifications():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('notification_GetAcceptedNotifications')
    accept = cursor.fetchall()

    cursor.callproc('notification_GetDeniedNotifications')
    deny = cursor.fetchall()
    
    return render_template("notifications.html", accept=accept, deny=deny)