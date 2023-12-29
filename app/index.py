from app import app, db, dao, utils, login as app_login
from flask import render_template, request, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from admin import *

@app.context_processor
def common_response():
    return {
        'airports': dao.get_airports(),
        'ticket_classes': dao.get_ticket_classes()
    }


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/select-flight', methods=['get', 'post'])
def select_flight():
    from_code = request.args.get('from-location')
    to_code = request.args.get('to-location')
    quantity = request.args.get('quantity')
    flight_date = request.args.get('flight-date')

    order = session.get('order', {})

    order['from-code'] = from_code
    order['from'] = dao.get_airport_name(from_code)
    order['to-code'] = to_code
    order['to'] = dao.get_airport_name(to_code)
    order['quantity'] = quantity
    order['flight_date'] = flight_date

    session['order'] = order

    flights = dao.search_flight(from_code, to_code)
    flight = dao.get_flight_by_id(request.args.get('flight'))
    ticket_class = dao.get_ticket_class_by_id(request.args.get('ticket-class'))
    if flight or ticket_class:
        session['order']['flight'] = flight.id
        session['order']['ticket-class'] = ticket_class.id

    return render_template('select-flight.html',
                           flight_list=flights, flight=flight, ticket_class=ticket_class)


@app.route('/passenger-info', methods=['post', 'get'])
def passenger_info():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        # is_adult = request.form.get('adult')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        nationality = request.form.get('nationality')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        order = session.get('order', {})
        customers = session.get('customers', [])
        c = {}
        c['name'] = lname + fname
        # c['is_adult'] = is_adult.__eq__('true')
        c['gender'] = gender
        c['dob'] = dob
        c['nationality'] = nationality
        c['phone'] = phone
        c['email'] = email
        c['address'] = address

        if c in customers:
            print('da ton tai')
        else:
            customers.append(c)
            session['customers'] = customers
            print(session)

        # del session['customers']

    return render_template('passenger-info.html')


@app.route('/payment', methods=['post', 'get'])
@login_required
def payment():
    customers = session.get('customers')
    flight = dao.get_flight_by_id(session['order']['flight'])
    ticket_class = dao.get_ticket_class_by_id(session['order']['ticket-class'])

    bill = dao.create_bill(current_user.id)
    for c in customers:
        print(c)
        cus = dao.create_customer(name=c['name'], gender=c['gender'],
                                  nationality=c['nationality'], phone=c['phone'], email=c['email'],
                                  address=c['address'])
        ticket = dao.create_ticket(flight_id=flight.id, ticket_class_id=ticket_class.id, customer_id=cus.id, bill_id=bill.id)
        bill.tong_hoa_don += ticket.tong_tien_ve

    if request.method == 'POST':
        return utils.pay(bill.id)

    payment_status = request.args.get('vnp_TransactionStatus')
    if payment_status is not None:
        status = 'success' if payment_status == '00' else 'fail'
        if status == 'success':
            bill.da_thanh_toan = True
            del session['order']
            del session['customers']

        return redirect(f'/payment_result?status={status}')

    return render_template('payment.html')


@app.route('/payment-result')
def payment_result():
    status = request.args.get('status')
    return render_template('payment-result.html', status=status)

@app_login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/register', methods=['post'])
def register():
    name = request.form.get('name')
    username = request.form.get('username')
    avatar = request.files.get('avatar')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_pw')

    if password == confirm_password:
        dao.create_user(username, email, password, name, avatar)
        return redirect(utils.get_prev_url())


@app.route('/admin/login', methods=['post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.check_user(username=username, password=password)

    if user:
        login_user(user)

    return redirect(utils.get_prev_url())


@app.route('/logout')
def logout():
    logout_user()
    return redirect(utils.get_prev_url())


if __name__ == '__main__':
    app.run(debug=True)
