from flask import Flask, render_template, redirect, abort, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user

from data import db_session, User, Department, Jobs

from forms import LoginForm, DepartmentForm, JobsForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    title = "Сайт"
    if not current_user.is_authenticated:
        return render_template("base.html", title=title)
    else:
        db = db_session.create_session()
        job = db.query(Jobs).all()
        return render_template("works.html", jobs=job, title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            hashed_password=form.password.data
        )
        db.add(user)
        db.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == form.email.data).first()
        if user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(int(user_id))


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db = db_session.create_session()
    department = db.query(Department).filter(Department.id == id).first()
    if department:
        db.delete(department)
        db.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm()
    if request.method == "GET":
        db = db_session.create_session()
        department = db.query(Department).filter(Department.id == id).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db = db_session.create_session()
        department = db.query(Department).filter(Department.id == id).first()
        if department:
            department.chief = form.chief.data
            department.title = form.title.data
            department.members = form.members.data
            department.email = form.email.data
            db.commit()
        return redirect('/')
    return render_template('add_department.html', form=form,
                           title="Редактирование департамента")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db = db_session.create_session()
    job = db.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db.delete(job)
        db.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db = db_session.create_session()
        job = db.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db = db_session.create_session()
        job = db.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db.commit()
        return redirect('/')
    return render_template('add_jobs.html',
                           form=form,
                           title="Редактирование работы")


@app.route('/departments', methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        department = Department()
        department.chief = form.chief.data
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        db.add(department)
        db.commit()
        return redirect('/')
    return render_template('add_department.html',
                           form=form,
                           title="Создание департамента")


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db.add(job)
        db.commit()
        return redirect('/')
    return render_template('add_jobs.html', form=form, title="Создание работы")


@app.route('/works_department')
@login_required
def str_2():
    db = db_session.create_session()
    departments = db.query(Department).all()
    return render_template("departments.html", departments=departments)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
