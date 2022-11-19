from flask import *
from connect import *
import ibm_db
from flask_mail import *

app= Flask(__name__,template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'secret978676756key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vasundrathegreat@gmail.com'
app.config['MAIL_PASSWORD'] = 'yuymjkdkofuohzwa'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        mail=request.form['email']
        password=request.form['password']
        query="insert into users values('"+username+"','"+password+"','"+mail+"')"
        ibm_db.exec_immediate(conn,query)
        print("row entered :('"+username+"','"+password+"','"+mail+"')")
    return redirect(url_for('index'))

@app.route("/login",methods=('GET','POST'))
def loginpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "select COUNT(*) from users where username='"+username+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        
        stmt = ibm_db.prepare(conn,query)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_tuple(stmt)
        if(row[0] == 1 ):
            session['logged_in_username'] = username
            return redirect('home')
    return render_template("index.html")

@app.route("/makerequest",methods=('POST','GET'))
def mreq():
    username = session.get('logged_in_username', None)
    pname=request.form['pname']
    bloodgroup=request.form['bloodgroup']
    pcondition=request.form['pcondition']
    dname=request.form['dname']
    haddress=request.form['haddress']
    aphone=request.form['aphone']
    print("row entered : '"+username+"','"+bloodgroup+"','"+pcondition+"','"+dname+"','"+haddress+"','"+aphone+"'")
    query="insert into requests values('"+username+"','"+bloodgroup+"','"+pcondition+"','"+dname+"','"+haddress+"','"+aphone+"','"+pname+"')"
    ibm_db.exec_immediate(conn,query)
    # query="insert into request values(?,?,?,?,?,?,?)"
    # stmt=ibm_db.prepare(conn,query)
    # ibm_db.bind_param(stmt,1,username)
    # ibm_db.bind_param(stmt, 2,bloodgroup)
    # ibm_db.bind_param(stmt, 3,pcondition)
    # ibm_db.bind_param(stmt, 4, dname)
    # ibm_db.bind_param(stmt, 5, haddress)
    # ibm_db.bind_param(stmt, 6, aphone)
    # ibm_db.bind_param(stmt, 7, pname)
    query="select * from donors where bloodgroup='"+bloodgroup+"'"
    stmt=ibm_db.exec_immediate(conn,query)
    row  = ibm_db.fetch_tuple(stmt)
    arr=[]
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)
    for i in arr:
        msg = Message('Hello', sender = "vasundrathegreat@gmail.com", recipients = [i[4]])
        msg.body = "Hello "+i[6]+" ! \nWe at RED DROPS have the following request and your an elligible donor.\n"+"Patient Name: "+pname+"\n"+"Patient BloodGroup: "+bloodgroup+"\n"+"Patient Condition: "+pcondition+"\n"+"Doctor Name: "+dname+"\n"+"Hospital Address: "+haddress+"\n"+"Attender phone: "+aphone+"\n"
        mail.send(msg)
    return redirect('request')

@app.route("/request")
def req():
    username = session.get('logged_in_username', None)
    query="select * from requests where username='"+username+"'"
    stmt=ibm_db.exec_immediate(conn,query)
    stmt = ibm_db.exec_immediate(conn, query)
    row  = ibm_db.fetch_tuple(stmt)
    arr=[]
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row
    if(arr==[]):
        return render_template('request.html',activereq=0)
    return render_template('request.html',activereq=arr)

@app.route("/donor")
def donor():
    username = session.get('logged_in_username', None)
    query="select * from donors where username='"+username+"'"
    stmt=ibm_db.exec_immediate(conn,query)
    stmt = ibm_db.exec_immediate(conn, query)
    row  = ibm_db.fetch_tuple(stmt)
    arr=[]
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)
    if (arr==[]):
        return render_template('donor.html',don=0)
    return render_template('donor.html',don=arr)

@app.route("/regdonor",methods=('POST','GET'))
def regdonor():
    username = session.get('logged_in_username', None)
    name=request.form['name']
    bloodgroup=request.form['bloodgroup']
    address=request.form['address']
    phone=request.form['phone']
    dob=request.form['dob']
    email=request.form['email']
    query="insert into donors values('"+username+"','"+bloodgroup+"','"+dob+"','"+phone+"','"+email+"','"+address+"','"+name+"')"
    ibm_db.exec_immediate(conn,query)
    return redirect('donor')

@app.route("/home")
def home():
    return render_template("home.html")

if(__name__=='__main__'):
     app.run(debug=True)