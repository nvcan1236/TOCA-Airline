from app import app, admin, dao
from flask import render_template, request


@app.context_processor
def common_response():
    return {
        'airports': dao.get_airports(),
        'ticket_classes': dao.get_ticket_classes()
    }


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/select-flight', methods=['get'])
def select_flight():
    from_code = request.args.get('from-location')
    to_code = request.args.get('to-location')
    quantity = request.args.get('quantity')
    flight_date = request.args.get('flight-date')
    flight = dao.get_flight_by_id(request.args.get('flight'))
    ticket_class = dao.get_ticket_class_by_id(request.args.get('ticket-class'))

    flights = dao.search_flight(from_code, to_code)

    return render_template('select-flight.html',
                           flight_list=flights,
                           quantity=quantity,
                           flight_date=flight_date,
                           flight=flight,
                           ticket_class=ticket_class
                           )


@app.route('/passenger-info')
def passenger_info():
    flight_id = request.args.get('flight')
    flight = dao.get_flight_by_id(flight_id)
    quantity = request.args.get('quantity')
    flight_date = request.args.get('flight-date')
    return render_template('passenger-info.html', flight=flight, quantity=quantity, flight_date=flight_date )


@app.route('/payment')
def payment():
    return render_template('payment.html')


if __name__ == '__main__':
    app.run(debug=True)
