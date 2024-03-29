import sqlite3
import os
from FDataBase import FDataBase
from flask import redirect, render_template, Flask, request, flash, abort, \
    url_for, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_login import LoginManager, login_user, login_required, \
    current_user, logout_user
from User import UserInfo
import re
from PIL import Image
import io

# CONFIGURATION
DATABASE = "posts.db"
SECRET_KEY = "2c4d969558ce80c318380969f35ebb"
MAX_CONTENT_LENGTH = 1024 * 1024 * 2
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "posts.db")))
# Длительность сеанса
app.permanent_session_lifetime = timedelta(days=1)
login_manager = LoginManager(app)
login_manager.login_view = 'reg'
login_manager.login_message = 'Нужно войти или зарегистрироваться'
login_manager.login_message_category = 'success'
db = False


@app.route("/")
def handler():
    '''Главная страница'''
    name = 'не авторизован'  # Имя пользователя(User name)
    img = ''
    if 'userID' in session:  # Если открыта сессия
        name = session['userID'][1]
    elif not current_user.is_active:
        logout_user()
    return render_template("index.html", img=img, title="FlaskSite", menu=db.getMenu()[::-1], UserName=name)


@login_manager.user_loader
def load_user(userID):
    return UserInfo(userID, db)


@app.before_request
def establish_connection():
    '''Функция для установления соединения с БД'''
    global db   # доступ к БД через объект FDataFase
    try:
        # обращение к БД, через путь указанный в приложении
        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row  # Вид словарь
        # проверка наличия таблицы
        with app.open_resource("sq_db.sql", mode='r') as file:
            connection.cursor().executescript(file.read())
        connection.commit()  # сохранить изменения
        db = FDataBase(connection)  # установить соединение
    except Exception as error:
        print('Ошибка была обнаружена ', error)


@app.errorhandler(404)
def handle_bad_request(e):
    return '<h1>bad request!</h1>', 400


@app.route('/search_post', methods=["POST"])
def search():
    menu = db.getMenu()
    query = ' +' + fr"{request.form['query']}" + ' +'
    results = []
    for elem in menu:
        title = ' ' + elem['title'] + ' '
        if re.search(query, title, re.I):
            ind = re.search(query, title, re.I)
            title2 = title[:ind.start()]+'<p class="marker">'+\
                        title[ind.start():ind.end()]+'</p>'+\
                        title[ind.end():]

            results.append([title2, elem])
    return render_template('search_res.html', menu=results)


@app.route('/userAva<int:showIm>')
def userAva(showIm=False):
    if showIm:
        ava = db.getAll(showIm)['avatar']
        if not ava:
            with open(app.root_path + "\\static\\images\\default.png", 'rb') as file:
                ava = file.read()
    elif current_user.is_active:
        ava = current_user.getAvatar(app.root_path)
    else:
        with open(app.root_path + "\\static\\images\\default.png", 'rb') as file:
            ava = file.read()
    img = make_response(ava)
    img.headers['Content/type'] = 'image'
    return img


@app.route('/upload', methods=["GET", "POST"])
@login_required
def uploadFile():
    if request.method == 'POST':
        try:
            file = request.files['image']
            if file.filename.rsplit('.')[1] == 'png' or \
               file.filename.rsplit('.')[1] == 'PNG' or \
               file.filename.rsplit('.')[1] == 'jpg' or \
               file.filename.rsplit('.')[1] == 'JPEG':
                img = Image.open(file, mode='r')
                new_img = img.resize((300, 300))
                buf = io.BytesIO()
                new_img.save(buf, format=img.format)
                byte_im = buf.getvalue()
                db.updateUserImg(byte_im, current_user.get_ID())
            else:
                print('Неправильный формат файла')
        except Exception as error:
            print('Ошибка ', error)
    return redirect(url_for('profile'))


@app.route("/add_post", methods=["GET", "POST"])
@login_required
def AddPost():
    if request.method == "POST":
        if db.addContent(request.form, current_user.get_ID()) == 200:
            flash("Пост опубликован", category="success")
        else:
            flash("Ошибка", category="error")
    return render_template("add_menu.html")


@app.route("/edit_post<int:post_id>", methods=["POST", "GET"])
@login_required
def editor(post_id):
    if current_user.is_active and db.getPost(post_id)['authour_id'] == \
     current_user.get_ID():
        if request.method == 'GET':
            menu = db.getContent(post_id)
            return render_template("edit.html", content=menu[-1]["content"], post_num=post_id)
        code = db.edit_post(request.form["new_content"], post_id)
        if code == 200:
            # данные внесены без ошибок код 200
            flash("Правки внесены", category="success")
        else:
            # во время записи произошла ошибка
            flash("Ошибка", category="error")
        menu = db.getContent(post_id)

        return render_template("edit.html", content=menu[-1]["content"], post_num=post_id)
    abort(404)


@app.route("/<int:post_id>")
def showPost(post_id):
    respone = db.getPost(post_id, True)
    if current_user.is_active and db.getPost(post_id)['authour_id'] == \
            current_user.get_ID():
        return render_template("post_skeleton.html", id=respone["id"],
                               content=respone["content"], title=respone["title"], 
                               authour=respone["authour"], views=respone['views'],
                               dataP=respone["dataP"], shI=respone["authour_id"])
    if not respone:
        abort(404)
    return render_template("post_skeleton2.html", id=respone["id"],
                           content=respone["content"], title=respone["title"], 
                           authour=respone["authour"], views=respone['views'],
                           dataP=respone["dataP"], shI=respone["authour_id"])


@app.route("/delete_post<int:post_id>")
@login_required
def delete_post(post_id):
    if current_user.is_active and db.getPost(post_id)['authour_id'] == \
     current_user.get_ID():
        db.deletePost(post_id)
        flash("Статья успешно удалена", 'success')
        return redirect('/')
    abort(403)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('handler'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_active:
        return render_template("Personal Area.html", name=current_user.name, \
            menu=db.getMenu(current_user.get_ID())[::-1])
        # menu=db.getMenu(current_user.get_ID())[::-1])
    return render_template("authorization.html")


@app.route("/reqistration", methods=["GET", "POST"])
def reg():
    session.permanent = True
    if request.method != 'GET':
        if len(request.form['login']) < 4 or len(request.form['password']) < 8:
            flash("Неверно введены данные", category="error")
            return render_template("authorization.html")

        if not db.checkin(request.form['login']):
            psw = generate_password_hash(request.form["password"])
            code = db.newUser(psw, request.form["login"])
            if code == 200:
                session['userID'] = db.getUserId(request.form['login'])
                user = UserInfo(session['userID'][1], db)
                login_user(user)
                flash("Вы успешно зарегистрировались", category="success")
                return redirect(url_for('profile'))
            else:
                flash("Ошибка во время регистрации", category="error")
            return render_template("authorization.html")
        else:
            if check_password_hash(db.returnHsh(request.form["login"]), request.form["password"]):
                session['userID'] = db.getUserId(request.form['login'])
                user = UserInfo(session['userID'][1], db)
                login_user(user)
                flash("Вы вошли в учетную запись", category="success")
                return redirect(url_for('profile'))
            else:
                flash("Неверный пароль", category="error")
                return render_template("authorization.html")
    return render_template("authorization.html")


if __name__ == "__main__":
    app.run(debug=True)
