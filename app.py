from website.models import User
import hashlib
from website.databases import db
from flask import render_template, flash, jsonify, redirect, url_for, request, make_response
from flask_mail import Mail, Message
import json
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website.app_creation import app
import os

# THIS IS THE GOOD VERSION
mail = Mail(app)
app.secret_key = 'dxJO>BQ,7FXsw^s[t*8mC`<&]o|d@F'


# User.query.filter(User.email.endswith("@usc.edu")).all()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in request.cookies:
            return func(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        username = request.args.get('user')
        password = request.args.get('pass')
        if not username:
            return render_template('login.html')
        user = User.query.filter_by(username=username).first()
        if user:
            cipher = hashlib.md5()
            cipher.update(password.encode('utf8'))
            if user.password == cipher.hexdigest():
                flash("Logged in successfully!", category="success")
                user.is_authenticated = True
                db.session.commit()
                resp = make_response(redirect(url_for('success')))
                resp.set_cookie('user_id', value=str(user.id))
                return resp

        elif username is not None:
            flash("Incorrect username or password. Try again.", category="error")
            return make_response(redirect(url_for('fail')))

    return render_template('login.html')


@app.route('/logout')
def logout():
    cookie = request.cookies.get('user_id')
    print("cookie: " + str(cookie))
    if cookie:
        user = User.query.filter_by(id=cookie).first()
        print("User: " + str(user))
        user.is_authenticated = False
        db.session.commit()
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('user_id', value='')

    return resp


@app.route('/register', methods=['GET'])
def signup():
    if request.method == "GET":
        username = request.args.get('user')
        password = request.args.get('pass')
        user = None
        if username:
            user = User.query.filter_by(username=username).first()
        if user:
            flash("This username already exists. Try again.", category="error")
        elif password is not None:
            cipher = hashlib.md5()
            cipher.update(password.encode('utf8'))
            new_user = User(username=username, password=cipher.hexdigest(), balance=0,
                            action_type='deposit')
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    cookie = request.cookies.get('user_id')
    if not cookie or cookie == '':
        return redirect(url_for('login'))
    resp = make_response(render_template('home.html'))
    resp.set_cookie('user_id', value=cookie, max_age=1500, samesite='Lax')
    return resp


@app.route('/success', methods=['GET'])
def success():
    cookie = request.cookies.get('user_id')
    if not cookie or cookie == '':
        return redirect(url_for('login'))
    resp = make_response(render_template('success.html'))
    resp.set_cookie('user_id', value=cookie)
    return resp


@app.route('/fail', methods=['GET', 'POST'])
def fail():
    return make_response(render_template('fail.html'))


@app.route('/update-content', methods=['GET', 'POST'])
def update_content():
    cookie = request.cookies.get('user_id')
    user = User.query.filter_by(id=int(cookie)).first()
    print('update content')
    message = json.loads(request.data)
    content_type = message['content_type']
    user.action_type = content_type
    db.session.commit()
    return jsonify({})


@app.route('/manage', methods=['GET'])
def manage():
    cookie = request.cookies.get('user_id')
    user = User.query.filter_by(id=cookie).first()
    if not user:
        return redirect(url_for('login'))
    if not user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "GET":
        action = request.args.get('action')
        amount = request.args.get('amount')
        # handle balance and close
        resp = None
        if action and not amount:
            if action == 'balance':
                user.action_type = 'balance'
                print("balance=" + str(user.balance))
                resp = make_response(render_template('manage.html', user=user))
                resp.set_cookie('user_id', value=str(user.id))
            elif action == 'close':
                user.action_type = 'close'
                resp = make_response(close_account())

        # handle deposit and withdrawal
        elif action and amount:
            if action == 'deposit' and int(amount) > 0:
                current_balance = user.balance
                new_balance = current_balance + int(amount)
                user.balance = new_balance
                user.action_type = 'balance'
                db.session.commit()
                print('balance=' + str(new_balance))
                resp = make_response(render_template('manage.html', user=user))
                resp.set_cookie('user_id', value=str(user.id), max_age=1500, samesite='Lax')
            elif action == 'withdraw' and int(amount) > 0:
                current_balance = user.balance
                if int(amount) > current_balance:
                    flash('Your account does not have sufficient funds to complete this withdrawal', category='error')
                    resp = make_response(render_template('manage.html', user=user))
                    resp.set_cookie('user_id', value=str(user.id))
                else:
                    new_balance = current_balance - int(amount)
                    user.balance = new_balance
                    print('balance=' + str(new_balance))
                    user.action_type = 'balance'
                    db.session.commit()
                    resp = make_response(render_template('manage.html', user=user))
                    resp.set_cookie('user_id', value=str(user.id))
            else:
                flash('Please enter a value greater than zero', category='error')
                resp = make_response(render_template('manage.html'))
        else:
            resp = make_response(render_template('manage.html', user=user))
            resp.set_cookie('user_id', value=str(user.id))
    return resp


@app.route('/close-account')
def close_account():
    cookie = request.cookies.get('user_id')
    User.query.filter_by(id=cookie).delete()
    db.session.commit()

    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('user_id')

    return resp


# @app.route('/reset', methods=['GET'])
# def reset():
#     if request.method == "GET":
#         username = 'root'
#         password = request.args.get('pass')
#
#         user = User.query.filter_by(username=username).first()
#         if password is not None:
#             user.password = generate_password_hash(password, method='md5')
#             db.session.commit()
#             flash('Password Updated!', category='success')
#             return redirect(url_for('login'))
#     return render_template('reset_token.html')


# where the user enters their email in to get a form sent to it
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    print('here1')
    if request.method == 'GET':
        print('here2')
        cookie = request.cookies.get('user_id')
        if cookie:
            print('here3')
            user = User.query.filter_by(id=int(cookie)).first()
            if user and user.is_authenticated:
                print('here4')
                resp = make_response(redirect(url_for('manage')))
                resp.set_cookie('user_id', value=str(user.id))
                return resp
        username = request.args.get('user')
        user = User.query.filter_by(username=username).first()
        if user:
            print('here5')
            send_reset_email(user)
            return redirect(url_for('login'))
        elif username and username != '':
            print('here6')
            flash('No account is registered under that email. Please make an account.', category='error')
            return redirect(url_for('signup'))
    print('here7')
    return render_template('reset_request.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        user = verify_reset_token(token)
        if user is None:
            flash('Your token is invalid or has expired', category='error')
            return render_template('reset_token.html')
        elif user.is_authenticated:
            resp = make_response(redirect(url_for('manage')))
            resp.set_cookie('user_id', value=str(user.id))
            return resp
        elif user:
            new_pass = request.args.get('pass')
            if new_pass:
                cipher = hashlib.md5()
                cipher.update(new_pass.encode('utf8'))
                user.password = cipher.hexdigest()
                db.session.commit()
                flash('Your password has successfully been reset', category='success')
                return redirect(url_for('login'))
    return render_template('reset_token.html')


def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    user = User.query.filter_by(id=user_id).first()
    return user


def send_reset_email(user):
    token = user.get_reset_token()
    message = "To reset your password, visit the following link:\n" + url_for('reset_password', token=token,
                                                                              _external=True) + \
              "\n\nIf you did not make this request, please ignore this email. "
    email = user.username + "@usc.edu"
    command = 'echo %s | mail -s “Password Reset Request” %s' % (message, email)
    os.system(command)


# only if we execute this file, and did not import it, should the app be run
if __name__ == '__main__':
    app.run(port=8080)

    #  ssl_context='adhoc'
