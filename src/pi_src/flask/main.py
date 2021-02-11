# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import pyrebase
import json, os
import form
import db

# firebaseの設定ファイルを読み込む
with open("FireBaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# @app.route('/')
# def hello():
#     name = "Hoge"
#     #return name
#     return render_template('hello.html', title='flask test', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html",msg="", title="login")

    email = request.form['email']
    password = request.form['password']

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['usr'] = email
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。", title="login")

@app.route("/", methods=['GET'])
def index():
    usr = session.get('usr')
    # ユーザのセッションがない場合ログインページを表示
    if usr == None:
        return redirect(url_for('login'))
    # ログイン済みの場合の表示
    return render_template("index.html", usr=usr, title="RAS")

@app.route('/logout')
def logout():
    del session['usr']
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form_info = form.LoginForm(request.form)
    if request.method == 'POST' and form_info.validate():
        
        try:
            data = [form_info.student_id.data, form_info.user_name.data,
                form_info.full_name.data, form_info.token.data,
                form_info.mac_addr.data, session['usr'] ]
            print(data)
            DB = db.DB()
            DB.sign_up(data)
        except Exception as e:
            print(e)
            flash('ユーザ登録に失敗しちゃった...')
            return redirect(url_for('login'))

        flash('ユーザ登録したよ')
        usr = session.get('usr')
        # ユーザのセッションがない場合ログインページを表示
        if usr == None:
            return redirect(url_for('login'))
        # ログイン済みの場合の表示
        return render_template("index.html", usr=usr, title="RAS")

    return render_template('signup.html', form=form_info, title="ユーザ登録")

if __name__ == "__main__":
    app.run(debug=True,  host='0.0.0.0', port=8080)
