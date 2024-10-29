from flask import Flask,request,render_template,render_template,redirect,session
import bcrypt
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Connecting with local database using mysql password
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisnotgood'
username = 'root'
password = 'V@rsha2001'
host = 'localhost'
port = 3306
database = 'milk_data'


# Construct the URI

uri = f'mysql://{username}:{urllib.parse.quote(password)}@{host}:{port}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        userpass = User.query.filter_by(password= password).first()
        # print(user)
        if user:
            session['email'] = user.email
            session['password'] = user.password
            # session['name'] = user.name
            return redirect('/dashboard')
        else:
            return render_template('login.html',error = 'Invalid User')    
          
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session.get('email'):
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user = user)
    return redirect('/login')


class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer,primary_key = True)
    userName = db.Column(db.String(30),nullable = False)
    email = db.Column(db.String(30),unique = True)
    password = db.Column(db.String(10),nullable = False)

    def __init__(self,userId = userId,userName = userName,email = email,password = password):
        self.userId = userId
        self.userName =userName
        self.email = email
        self.password = password

class Orders(db.Model):
    __tablename__ = 'orders'
    orderId = db.Column(db.Integer,primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('user.userId'))
    address = db.Column(db.String(100),nullable = False)
    cellno = db.Column(db.BIGINT,nullable = False)
    salesmanId = db.Column(db.Integer,nullable = False)

    def __init__(self,orderId=orderId,userId = userId,address =address,cellno = cellno,salesmanId = salesmanId ):
        self.orderId = orderId
        self.userId = userId
        self.address = address 
        self.cellno = cellno
        self.salesmanId = salesmanId


@app.route('/register',methods = ['GET','POST'])
def register():
    try:
        if request.method == 'POST':
            if not request.form['email'] or not request.form['name'] or not request.form['password'] :
                return redirect('/register')
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            new_user = User(userName=name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    except Exception as e:
        return f'Error:Email already exist\n{str(e)}'        

    return render_template('register.html')        

@app.route("/orders",methods = ['GET','POST'])
def orders():
    if request.method == 'POST':
        print(request.method)
        if not request.form['userId'] or not request.form['address'] or not request.form['cellno'] or not request.form['salesmanId']:
            return redirect('/orders')
        userId = request.form['userId']
        address = request.form['address']
        cellno = request.form['cellno']
        # print(cellno)
        salesmanId = request.form['salesmanId']
        # print(salesmanId)

        new_order = Orders(userId = userId,address = address,cellno = cellno,salesmanId = salesmanId)
        db.session.add(new_order)
        db.session.commit()
        print("Success")
        return redirect('/dashboard')
    # except Exception as e:
    #     return f'errr:{str(e)}'        
    return render_template('orders.html')
            


    


     

with app.app_context():
    db.create_all()         

         
# from main import app    

if __name__ == '__main__':
    app.run(debug=True)
