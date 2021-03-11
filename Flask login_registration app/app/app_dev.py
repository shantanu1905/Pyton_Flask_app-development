from flask import Flask, render_template, request, flash ,redirect ,url_for , session , logging
import sqlite3
from user_agents import parse
from flask_mail import Mail, Message
con=sqlite3.connect('users.db',check_same_thread=False)
cursor=con.cursor()

app = Flask(__name__)
app.config['SECRET_KEY']= 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
app.config['SECRET_KEY']= 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shantanunimkar19@gmail.com'
app.config['MAIL_PASSWORD'] = 'Shant@24x7'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)





@app.route('/register', methods=['GET','POST'])
def register():
    
    msg = None
    if(request.method == 'POST'):
        if(request.form["username"]!="" and request.form["password"]!= "" and request.form["email"]!= ""):
            global username
            username = request.form['username']
            email= request.form['email']
            password= request.form['password']
            cursor.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",(username,email,password) )
            #cursor.execute("INSERT INTO users VALUES('"+username+"','"+email+"', '"+password+"')" )
            msg="Account has created Successfully !!"
            con.commit()
            #con.close()
            
        else:
            msg =" Some thing went wrong "
    return render_template("register.html", msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if(request.method == 'POST'):
        global email
        email=request.form["email"]
        #email=request.form["email"]
        password=request.form["password"]
        cursor.execute("SELECT * FROM users WHERE email ='"+email+"' and password = '"+password+"'" )
        r = cursor.fetchall()
        for i in r:
            if(email == i[2] and password == i[3]):
                session["logedin"]= True
                session["email"]= email
                track()
                
                return redirect(url_for("profile"))
            else:
                msg="please enter valid crediential"
    return render_template("login.html" , msg=msg)

@app.route('/policy' , methods=['GET', 'POST'])
def policy():
    return render_template("policy.html")


@app.route('/logout') 
def logout(): 
    session.clear() 
    return redirect(url_for('login')) 

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/',  methods=['GET', 'POST'])
def index():

    return render_template("index.html" )

def track():
    ip=request.remote_addr
    client_data=request.user_agent.string
    ua_string = client_data
    user_agent = parse(ua_string)

    # Accessing user agent's browser attributes 
    browser=user_agent.browser.family  # returns 'Mobile Safari'
    # Accessing user agent's operating system properties
    os=user_agent.os.family  # returns 'iOS'
    user_agent.os.version_string  # returns '5.1'

    # Accessing user agent's device properties
    dev=user_agent.device.family  # returns 'iPhone'
    dev_b=user_agent.device.brand # returns 'Apple'
    dev_m=user_agent.device.model # returns 'iPhone'

    # Viewing a pretty string version
    print(str(user_agent)) # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"
    msg = Message('Services.io@Auth-Team', sender='shantanunimkar19@gmail.com', recipients=[email])
    msg.html = render_template('email.html', os=os ,ip=ip ,browser=browser ,dev=dev,dev_b=dev_b,dev_m=dev_m)
    mail.send(msg)



if __name__ == '__main__':
    app.run(debug=True)