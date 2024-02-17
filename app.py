from flask import Flask,render_template,request,flash,redirect,url_for

app=Flask(__name__)
app.secret_key='key'
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://root:21951A67B9@cluster0.twkxqsh.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server     
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

db=client['go-mechanic']
garages=db['garages']
#rendering login page on arrival
@app.route('/')
@app.route('/login')
def login():
    return render_template('loginPage.html')

@app.route('/auth',methods=['POST','GET'])
def auth():
    if request.method=='POST':
        email=request.form['email']
        psw=request.form['psw']
        if email=='admin@gmail.com' and psw=='admin@123':
            data=garages.find({'city':'Hyderabad'})
            flash('You have logged in sucessfully!!','info')
            return render_template('adminHomePage.html',name='Admin',data=data)
    else:
        flash('Invalid Response','info')
        return redirect(url_for('login'))
    
@app.route('/logout',methods=['POST','GET'])
def logout():
    flash('Logout succesfully!!','info')
    return redirect(url_for('login'))

@app.route('/load',methods=['POST','GET'])
def load():
    if request.method=='POST':
        city=request.form['citySelector']
        data=garages.find({'city':city})
        return render_template('adminHomePage.html',name='Admin',data=data)
    else:
        flash('Incorrect Response','info')
        return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')