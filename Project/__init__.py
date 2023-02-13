import Employee, Account, Inventory, CreditCardClass, LocationClass
import shelve
import os
from flask_login import LoginManager, login_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash
from Forms import CreateEmployeeForm, RegisterAccountForm, Login, InventoryEdit, CreditCardForm, GymLocationForm
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
        return [item for item in range(r1, r2 + 1)]

    employee_count = createList(1, len(employees_list))

    return render_template('employee_list.html', count=len(employees_list), employees_list=employees_list,
                           employee_count=employee_count)



@app.route('/CreateCreditCard', methods=['GET', 'POST'])
def credit_card_form():
    ccform = CreditCardForm(request.form)
    if request.method == 'POST' and ccform.validate():
        creditcard_dict = {}
        db = shelve.open('credit_card_db.db', 'c')

        try:
            creditcard_dict = db['CreditCard']
        except:
            print("Error in retrieving credit card from credit_card_db.db.")

        for key in creditcard_dict:
            creditcard = creditcard_dict.get(key)
            if creditcard.get_cardnumber() == ccform.cardnumber.data:
                flash("Card Number already exists")
                db.close()
                return render_template('creditCardForm.html', form=ccform)


        creditcard = CreditCardClass.CreditCard(ccform.cardholder.data, ccform.cardnumber.data,
                                                ccform.exp_month.data, ccform.exp_year.data,
                                                ccform.verification.data)

        creditcard_dict[creditcard.get_creditcard_id()] = creditcard
        db['CreditCard'] = creditcard_dict

        db.close()
        # replace get_card_route to the process of payment, once everything completes
        return redirect(url_for('get_card_route'))
    return render_template('creditCardForm.html', form=ccform)

# Retrieve the credit card information
@app.route('/get_card')
def get_card_route():
# create database
    creditcard_dict = {}
    db = shelve.open('credit_card_db.db', 'r')
    creditcard_dict = db['CreditCard']
    db.close()

# insert the data information into the shelves you have created
    creditcard_list = []
    for key in creditcard_dict:
        creditcard = creditcard_dict.get(key)
        creditcard_list.append(creditcard)

    return render_template("retrieveCreditCard.html", count=len(creditcard_list), creditcard_list=creditcard_list)

# update credit card
@app.route('/update_card/<int:id>', methods=["GET", "POST"])
def update_card_route(id):
    update_creditcard_form = CreditCardForm(request.form)
# update the database
    if request.method == 'POST' and update_creditcard_form.validate():
        creditcard_dict = {}
        db = shelve.open('credit_card_db.db', 'w')
        creditcard_dict = db['CreditCard']

        for key in creditcard_dict:
            creditcard = creditcard_dict.get(key)
            if creditcard.get_cardnumber() == update_creditcard_form.cardnumber.data:
                flash("Card Number already exists")
                db.close()
                return render_template('updateCreditCard.html', form=update_creditcard_form)

        creditcard = creditcard_dict.get(id)
        creditcard.set_cardholder(update_creditcard_form.cardholder.data)
        creditcard.set_cardnumber(update_creditcard_form.cardnumber.data)
        creditcard.set_exp_month(update_creditcard_form.exp_month.data)
        creditcard.set_exp_year(update_creditcard_form.exp_year.data)
        creditcard.set_verification_code(update_creditcard_form.verification.data)

        db['CreditCard'] = creditcard_dict
        db.close()

        return redirect(url_for("get_card_route"))
    else:
        creditcard_dict = {}
        db = shelve.open('credit_card_db.db', 'r')
        creditcard_dict = db['CreditCard']
        db.close()

        creditcard = creditcard_dict.get(id)
        update_creditcard_form.cardholder.data = creditcard.get_cardholder()
        update_creditcard_form.cardnumber.data = creditcard.get_cardnumber()
        update_creditcard_form.exp_month.data = creditcard.get_exp_month()
        update_creditcard_form.exp_year.data = creditcard.get_exp_year()
        update_creditcard_form.verification.data = creditcard.get_verification_code()


        return render_template("updateCreditCard.html", form=update_creditcard_form)

# delete credit card
@app.route('/deleteCreditCard/<int:id>', methods=['POST'])
def delete_credit_card(id):
    creditcard_dict = {}
    db = shelve.open('credit_card_db.db', 'w')
    creditcard_dict = db['CreditCard']
    creditcard_dict.pop(id)

    db['CreditCard'] = creditcard_dict
    db.close()

    return redirect(url_for('get_card_route'))

@app.route('/gymlocations')
def location_page():
    location_dict = {}
    db = shelve.open('location.db', 'r')
    location_dict = db['GymLocation']
    db.close()

    locations = []
    for key in location_dict:
        location = location_dict.get(key)
        lat = location.get_lat()
        lng = location.get_lng()
        locations.append({'lat': lat, 'lng': lng})

    return render_template('location.html', locations=locations, count=len(locations), location_list=location_dict.values())

@app.route('/createlocations', methods=['GET', 'POST'])
def create_location_page():
    create_location_form = GymLocationForm(request.form)
    if request.method == 'POST' and create_location_form.validate():
        location_dict = {}
        db = shelve.open('location.db', 'c')

        try:
            location_dict = db['GymLocation']
        except:
            print("Error in retrieving GymLocation from location.db.")

        for key in location_dict:
            location = location_dict.get(key)
            if location.get_locationAddress() == create_location_form.locationAddress.data:
                flash("Address already exists")
                db.close()
                return render_template('createLocation.html', form=create_location_form)
            elif location.get_lat() == create_location_form.lat.data and location.get_lng() == create_location_form.lng.data:
                flash("Address and lat and long already exists")
                db.close()
                return render_template('createLocation.html', form=create_location_form)

        location = LocationClass.GymLocation(create_location_form.locationAddress.data, create_location_form.lat.data, create_location_form.lng.data)
        location_dict[location.get_location_id()] = location
        db['GymLocation'] = location_dict

        db.close()

        return redirect(url_for('retrieve_location'))
    return render_template('createLocation.html', form=create_location_form)

@app.route('/retrievelocation')
def retrieve_location():
    location_dict = {}
    db = shelve.open('location.db', 'r')
    location_dict = db['GymLocation']
    db.close()

    location_list = []
    for key in location_dict:
        location = location_dict.get(key)
        location_list.append(location)

    return render_template('retrieveMapLocation.html', count=len(location_list), location_list=location_list)

@app.route('/updatelocation/<int:id>/', methods=['GET', 'POST'])
def update_location(id):
    update_location_form = GymLocationForm(request.form)
    if request.method == 'POST' and update_location_form.validate():
        location_dict = {}
        db = shelve.open('location.db', 'w')
        location_dict = db['GymLocation']


        for key in location_dict:
            location = location_dict.get(key)
            if location.get_locationAddress() == update_location_form.locationAddress.data:
                flash("Address already exists")
                db.close()
                return render_template('updateMapLocation.html', form=update_location_form)
            elif location.get_lat() == update_location_form.lat.data and location.get_lng() == update_location_form.lng.data:
                flash("Address and lat and long already exists")
                db.close()
                return render_template('UpdateMapLocation.html', form=update_location_form)

        location = location_dict.get(id)
        location.set_locationAddress(update_location_form.locationAddress.data)
        location.set_lat(update_location_form.lat.data)
        location.set_lng(update_location_form.lng.data)

        db['GymLocation'] = location_dict
        db.close()

        return redirect(url_for('retrieve_location'))
    else:
        location_dict = {}
        db = shelve.open('location.db', 'r')
        location_dict = db['GymLocation']
        db.close()

        location = location_dict.get(id)
        update_location_form.locationAddress.data = location.get_locationAddress()
        update_location_form.lat.data = location.get_lat()
        update_location_form.lng.data = location.get_lng()

        return  render_template('updateMapLocation.html', form=update_location_form)


@app.route('/deletelocation/<int:id>', methods=['POST'])
def delete_location(id):
    location_dict = {}
    db = shelve.open('location.db', 'w')
    location_dict = db['GymLocation']

    location_dict.pop(id)

    db['GymLocation'] = location_dict
    db.close()

    return redirect(url_for('retrieve_location'))

if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     app.run(debug=True)
