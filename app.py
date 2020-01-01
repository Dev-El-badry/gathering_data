from flask import Flask, render_template, url_for, redirect, request, session, flash
from forms import SignForm, RegisterForm
from flask_jsglue import JSGlue
from Project import Project
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_bcrypt import Bcrypt
import json
#from flask.ext.bcrypt import Bcrypt



base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
jsglue = JSGlue(app)
app.config['SECRET_KEY'] = 'mykey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
#setup database
db = SQLAlchemy(app)

#Migrate
migrate = Migrate(app, db)
user_data = dict()
global seller_search

@app.route('/', methods=['GET', 'POST'])
def index() :
    group_id = session.get('group_id') # return 0 OR 1

    if session.get('IS_LOGIN') == False or session.get('IS_LOGIN') is None :
        return redirect(url_for('signIn'))

    if request.method == 'POST' :
        num = _get_num_times()
        if num > 0 :
            seller_search = request.values.get('word_search')
            pro = Project(seller_search)
            update_times()
            return 'well done'
       
    return render_template('search_items.html', group_id=group_id)

def isset(var) :
    return var in locals() or var in globals()

#login
@app.route('/login', methods=['GET', 'POST'])
def signIn() :
    if session.get('IS_LOGIN') :
        return redirect(url_for('index'))
    form = SignForm()
    if form.validate_on_submit() :
        email = form.email.data
        password = form.password.data
        
        result = login(email, password)
        if result :
            flash("لقد تم تسجيل الدخول")
            return redirect(url_for('index'))
        else :
            flash("ادخل الايميل و كلمة السر الصحيحة")
            return redirect(url_for('signIn'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout() :
    session['IS_LOGIN'] = False
    return redirect(url_for('signIn'))





@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard() :
    #chk_is_login
    if session['IS_LOGIN'] == False :
        return redirect(url_for('signIn'))

    #chk_if_is_admin
    res_chk = _chk_if_is_admin()
    if res_chk == False :
        return redirect(url_for('signIn'))

    form = RegisterForm()
    if request.method == 'POST' :
        if request.values.get('user_id') != '' :
            user_id = request.values.get('user_id')
            
            username = form.username.data
            email = form.email.data
            group_id = form.group_id.data
            times = form.times.data

            data = {'username': username, 'email': email, 'group_id': group_id, 'times': times}
            result = update_user_val(user_id, data)
            if result :
                flash('Successfully Updated Account')
                return redirect(url_for('dashboard'))
        
        else :
            if form.validate_on_submit() :
                username = form.username.data
                email = form.email.data
                password = form.password.data
                group_id = form.group_id.data
                times = form.times.data
            
                pwd_hash = hashed_password(password)
                res = add_new_record(username, email, pwd_hash, group_id, times)
                if res :
                    flash('Successfully Added New Account')
                    return redirect(url_for('dashboard'))


    users = all_users()
    return render_template('dashboard.html', form=form, users=users)

@app.route('/update_user', methods=['GET', 'POST']) 
def update_user() :
   
    if request.method == 'POST' :
        id_post = request.values.get('id_post')
        
        user = _get_user_by_id(id_post)
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['group_id'] = user.group_id
        user_data['times'] = user.times
        
        user_json = json.dumps(user_data)
        return user_json
    # return 'sdfsdf'

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user() :
    if request.method == 'POST' :
        user_id = request.values.get('user_id')
        
        if user_id :
            
            res = _del_user(user_id)
            if res :
                flash('Successfully Delete Account')
                return redirect(url_for('dashboard'))
        else :
            return False

    return False

#Hashed Password
def hashed_password (pwd) :
    pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
    return pw_hash

def chk_if_password_right(pw_hashed, pwd) :
    result = bcrypt.check_password_hash(pw_hashed, pwd)
    return result

#save data in session
def save_in_session(id, username, email, group_id,times) :
    session['IS_LOGIN'] = True
    session['id'] = id
    session['username'] = username
    session['email'] = email
    session['group_id'] = group_id
    session['times'] = times


class User(db.Model) :
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    psasword = db.Column(db.String)
    email = db.Column(db.String)
    group_id = db.Column(db.Integer)
    times = db.Column(db.Integer)
    

    def __init__(self, username, psasword, email, group_id, times) :
        self.username = username
        self.psasword = psasword
        self.email = email
        self.group_id = group_id
        self.times = times

    def __repr__(self) :
        return f"username: {self.username} and email: {self.email} and password: {self.psasword} and group_id: {self.group_id} and times : {self.times}"

def login(email, password) :
    
    chk_mail = User.query.filter_by(email=email)
    

    if chk_mail.scalar() is not None :
        pwd_hashed = chk_mail.first().psasword
        res = chk_if_password_right(pwd_hashed, password)
        if res :
            username = chk_mail.first().username
            email = chk_mail.first().email
            id = chk_mail.first().id
            group_id = chk_mail.first().group_id
            times = chk_mail.first().times
            save_in_session(id, username, email, group_id, times)
            return True
        else :
            return False
    else :
        return False

def all_users() :
    users = User.query.all()
    return users

def add_new_record(username, email, password, group_id, times) :
    user = User(username, password, email, group_id, times)
    db.session.add(user)
    db.session.commit()
    return True

#get data by id
def _get_user_by_id(id) : 
    user = User.query.get(id)
    return user

def _del_user(user_id) :
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return True

def update_user_val(id, data) :
    #note data: username, email, password
    user = User.query.get(id)
    user.username = data['username']
    user.email = data['email']
    user.group_id = data['group_id']
    user.times = data['times']
    db.session.add(user)
    db.session.commit()
    return True
    
def _chk_if_is_admin() :
    user = User.query.filter_by(id = session.get('id')).scalar()
    if user :
        return True
    else :
        return False
def update_times() :
    id = session.get('id')
    user = User.query.get(id)
    user.times = user.times - 1
    db.session.add(user)
    db.session.commit()
    return True
 
#get times
def _get_num_times() :
    id = session.get('id')
    user = User.query.get(id)
    times = user.times
    return times

if __name__ == '__main__':
    app.run(debug=True)


# db.drop_all()
# db.create_all()