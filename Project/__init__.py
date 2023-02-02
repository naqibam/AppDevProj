import Employee
import Account
import Inventory
import shelve
import os
from flask_login import LoginManager, login_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash
from Forms import CreateEmployeeForm, RegisterAccountForm, Login, InventoryEdit
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


# noinspection PyPep8Naming
@app.route('/Cart')
def Cart():
    return render_template('cart.html')


@app.route('/Edit/<int:id>/', methods=['GET', 'POST'])
def Edit(id):
    update_employee_form = CreateEmployeeForm(request.form)
    if request.method == 'POST' and update_employee_form.validate():
        employees_dict = {}
        db = shelve.open('employee.db', 'w')
        employees_dict = db['Employees']

        employee = employees_dict.get(id)
        employee.set_first_name(update_employee_form.first_name.data)
        employee.set_last_name(update_employee_form.last_name.data)
        employee.set_gender(update_employee_form.gender.data)
        employee.set_position(update_employee_form.position.data)
        employee.set_NRIC(update_employee_form.NRIC.data)

        db['Employees'] = employees_dict

        db.close()
        return redirect(url_for('employee_list'))
    else:
        employees_dict = {}
        db = shelve.open('employee.db', 'r')
        employees_dict = db['Employees']
        db.close()

        employee = employees_dict.get(id)
        update_employee_form.first_name.data = employee.get_first_name()
        update_employee_form.last_name.data = employee.get_last_name()
        update_employee_form.gender.data = employee.get_gender()
        update_employee_form.position.data = employee.get_position()
        update_employee_form.NRIC.data = employee.get_NRIC()

    return render_template('edit_info.html', form=update_employee_form)


@app.route('/Forgot')
def Forgot():
    return render_template('forgot_pass.html')


@app.route('/Login', methods=['POST'])
def Login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('home'))
        flash('Invalid email address or Password.')
    return render_template('login_page.html', form=form)


@app.route('/AccountRegister', methods=['POST', 'GET'])
def AccountRegister():
    create_account_form = RegisterAccountForm()
    if create_account_form.validate_on_submit():
        user = User(username=create_account_form.username.data, email=create_account_form.email.data)
        user.set_password(create_account_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html', form=create_account_form)


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    create_employee_form = CreateEmployeeForm(request.form)
    if request.method == 'POST' and create_employee_form.validate():
        employees_dict = {}
        db = shelve.open('employee.db', 'c')

        try:
            employees_dict = db['Employees']
            employee_count = 0
            for key in employees_dict:
                employee_count += 1

        except:
            print("Error in retrieving Employees from employee.db.")
            employee_count = 0

        employee = Employee.Employee(create_employee_form.first_name.data,
                                     create_employee_form.last_name.data,
                                     create_employee_form.gender.data,
                                     create_employee_form.position.data,
                                     create_employee_form.NRIC.data)
        employees_dict[employee.get_employee_id() + employee_count] = employee
        db['Employees'] = employees_dict

        db.close()

        return redirect(url_for('employee_list'))
    return render_template('register_info.html', form=create_employee_form)


@app.route('/Inventory')
def Inventory():
    return render_template('home.html')


@app.route('/InventoryEdit', methods=['GET', 'POST'])
def Inventory_Edit():
    form_inv_edit = InventoryEdit()
    if request.method == 'POST' and form_inv_edit.validate():
        image = form_inv_edit.image.data
        image_name = image.filename
        image.save(os.path.join(app.instance_path, 'image', image_name))
        inv_dict = {}
        db = shelve.open('inv.db', 'c')

        try:
            inv_dict = db['Inventory']

        except:
            print("Error in retrieving Inventory from inv.db")

        inventory = Inventory.Inventory(form_inv_edit.name.data, form_inv_edit.name.data, form_inv_edit.name.data)
        db['Inventory'] = inv_dict
        inv_dict[inventory.get_inventory_id()] = inventory

        db.close()

        return redirect(url_for('home'))
    return render_template('inv_edit.html', form=form_inv_edit)


@app.route('/EmployeeList')
def employee_list():
    employees_dict = {}
    db = shelve.open('employee.db', 'r')
    try:
        employees_dict = db['Employees']
    except:
        print("Error in retrieving Employees from employee.db.")
    employees_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
    def createList(r1, r2):
        return [item for item in range(r1, r2+1)]

    employee_count = createList(1, len(employees_list))

    return render_template('employee_list.html', count=len(employees_list), employees_list=employees_list, employee_count=employee_count)


if __name__ == '__main__':
    app.run()
