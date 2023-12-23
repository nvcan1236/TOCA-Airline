from app import app, admin
from flask import render_template


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/select-flight')
def select_flight():
    return render_template('select-flight.html')

@app.route('/passenger-info')
def passenger_info():
    return render_template('passenger-info.html')


if __name__ == '__main__':
    app.run(debug=True)
