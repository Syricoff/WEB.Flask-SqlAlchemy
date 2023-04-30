from flask import Flask, render_template, redirect, abort, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.reg import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.JobsForm import JobsForm
from forms.dep import DepartmentForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    title = "Сайт"
    return render_template("base.html", title=title)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(user_id))


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            department.chief = form.chief.data
            department.title = form.title.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
        return redirect('/')
    return render_template('add_department.html', form=form, title="Редактирование департамента")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
        return redirect('/')
    return render_template('add_jobs.html', form=form, title="Редактирование работы")


@app.route('/departments',  methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.chief = form.chief.data
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/')
    return render_template('add_department.html', form=form, title="Создание департамента")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_jobs.html', form=form, title="Создание работы")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/Works_department')
@login_required
def str_2():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("Department_log.html", departments=departments)


@app.route('/Works_log')
@login_required
def str_1():
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).all()
    return render_template("Works_log.html", jobs=job)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()