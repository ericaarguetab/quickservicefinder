from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signIn")
        return f(*args, **kwargs)
    return decorated_function

def user_isowner(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_owner") is False:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def getSubsector(idsubsector):
    con = mysql.connect()
    cursor = con.cursor()

    cursor.callproc('subsector_GetSubsector',(idsubsector))
    subsector = cursor.fetchall()

    subsector_dict = []
    for sub in subsector:
        sub_dict = {
            'id': sub[0],
            'sector': sub[1],
            'name': sub[2]}
    subsector_dict.append(sub_dict)

    return jsonify(subsector_dict)