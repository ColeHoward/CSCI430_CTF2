# from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
# from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash
# from .databases import db
# from flask_login import login_user, login_required, logout_user, current_user
# from flask import session
#
# auth = Blueprint('auth', __name__)
# blacklist = []
# MAX_ATTEMPTS = 10
#
#
# @auth.route('/login', methods=['GET'])
# def login():
#     # session.permanent = True
#     # session_attempt = session.get('attempt')
#     # if not isinstance(session_attempt, int):
#     #     session['attempt'] = MAX_ATTEMPTS
#     # client_ip = request.environ.get('REMOTE_ADDR')
#     # if client_ip in blacklist:
#     #     abort(403)
#
#     if request.method == 'GET':
#         username = request.args.get('user')
#         password = request.args.get('pass')
#         user = User.query.filter_by(username=username).first()
#         if user:
#             if check_password_hash(user.password, password):
#                 flash("Logged in successfully!", category="success")
#                 login_user(user, remember=True)  # stays until webserver is restarted
#                 return redirect(url_for('views.home'))
#         else:
#             flash("Incorrect username or password. Try again.", category="error")
#             # session_attempt = session.get('attempt')
#             # session_attempt -= 1
#             # session['attempt'] = session_attempt
#
#         # if session_attempt == 1:
#         #     flash('This is your last attempt, if incorrect, %s will be blocked, Attempt %d of 10' % (
#         #         client_ip, session_attempt),
#         #           'error')
#         # elif session_attempt == 0:
#         #     flash('Out of attempts. %s is officially blocked.' % client_ip,
#         #           'error')
#         #     session['attempt'] = MAX_ATTEMPTS
#         #     session.permanent = False
#         #     blacklist.append(client_ip)
#         # else:
#         #     flash('Invalid login credentials, Attempts %d of 10' % session_attempt, 'error')
#
#     return render_template('login.html', user=current_user)
#
#
# @auth.route('/logout')
# @login_required  # ensures we can't access this route unless the user is logged in
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))
#
#
# @auth.route('/register', methods=['GET'])
# def signup():
#     # make sure to encrypt usernames
#     if request.method == "GET":
#         username = request.args.get('user')
#         password = request.args.get('pass')
#
#         user = User.query.filter_by(username=username).first()
#         if user:
#             flash("This username already exists. Try again.", category="error")
#         elif password is not None:
#             new_user = User(username=username, password=generate_password_hash(password,method='sha256'), balance=0,
#                             action_type='deposit')
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account created!', category='success')
#             login_user(current_user, remember=True)  # stays until webserver is restarted
#             return redirect(url_for('auth.login'))
#     return render_template('sign_up.html', user=current_user)
