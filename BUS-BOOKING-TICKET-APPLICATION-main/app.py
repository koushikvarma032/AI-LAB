"""
RuleBus - Rule-Based Bus Ticket Booking System
Main Flask Application Controller
"""
import os
import json
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from database.db import (
    init_db, get_all_cities, search_buses, get_bus_by_id, 
    get_booked_seats, save_booking, get_booking_details, 
    get_all_bookings, cancel_booking_in_db
)
from rules.rule_engine import RuleEngine
from rules.fare_rules import FareRules
from rules.seat_rules import SeatRules

app = Flask(__name__)
app.secret_key = 'rulebus_rbp_secret_key_2026'

# Initialize SQLite database on startup
with app.app_context():
    init_db()

@app.context_processor
def inject_today():
    """Injects today's date formatted as YYYY-MM-DD into all Jinja2 templates."""
    return {'today_date': datetime.date.today().strftime('%Y-%m-%d')}

# ==========================================
# 1. Home Page
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# 2. Bus Search & Selection
# ==========================================
@app.route('/search')
def search():
    cities = get_all_cities()
    source = request.args.get('source', '')
    destination = request.args.get('destination', '')
    travel_date = request.args.get('travel_date', datetime.date.today().strftime('%Y-%m-%d'))
    try:
        passengers = int(request.args.get('passengers', 1))
    except ValueError:
        passengers = 1

    buses = []
    searched = False

    if source and destination:
        searched = True
        buses = search_buses(source, destination)

    return render_template(
        'search.html',
        cities=cities,
        buses=buses,
        searched=searched,
        selected_source=source,
        selected_destination=destination,
        selected_date=travel_date,
        selected_passengers=passengers
    )

# ==========================================
# 3. Interactive Seat Selection
# ==========================================
@app.route('/seats/<int:bus_id>')
def select_seats(bus_id):
    bus = get_bus_by_id(bus_id)
    if not bus:
        flash("Selected bus not found.", "danger")
        return redirect(url_for('search'))

    travel_date = request.args.get('travel_date', datetime.date.today().strftime('%Y-%m-%d'))
    try:
        passengers = int(request.args.get('passengers', 1))
    except ValueError:
        passengers = 1

    # Fetch currently booked seats from SQLite for this bus & date
    booked_seats = get_booked_seats(bus_id, travel_date)

    return render_template(
        'seats.html',
        bus=bus,
        travel_date=travel_date,
        required_passengers=passengers,
        booked_seats=booked_seats
    )

# ==========================================
# 4. Passenger Information
# ==========================================
@app.route('/passengers', methods=['POST'])
def passenger_details():
    bus_id = request.form.get('bus_id')
    travel_date = request.form.get('travel_date')
    passengers_count = int(request.form.get('passengers_count', 1))
    selected_seats_str = request.form.get('selected_seats', '')

    bus = get_bus_by_id(bus_id)
    if not bus or not selected_seats_str:
        flash("Invalid seat selection.", "danger")
        return redirect(url_for('search'))

    selected_seats = [s.strip() for s in selected_seats_str.split(',') if s.strip()]

    # Validate selected seat count matches requested count
    if len(selected_seats) != passengers_count:
        flash(f"Please select exactly {passengers_count} seat(s).", "warning")
        return redirect(url_for('select_seats', bus_id=bus_id, travel_date=travel_date, passengers=passengers_count))

    # Evaluate Seat Availability & Conflict Rules using SeatRules
    already_booked = get_booked_seats(bus_id, travel_date)
    available_capacity = bus.get('available_seats', 30) - len(already_booked)
    seat_ok, seat_msg, seat_logs = SeatRules.evaluate_seat_availability(
        len(selected_seats), available_capacity, selected_seats, already_booked
    )
    if not seat_ok:
        flash(seat_msg, "danger")
        return redirect(url_for('select_seats', bus_id=bus_id, travel_date=travel_date, passengers=passengers_count))
    
    return render_template(
        'passenger.html',
        bus=bus,
        travel_date=travel_date,
        selected_seats=selected_seats
    )

# ==========================================
# 5. Live Fare Preview API Endpoint
# ==========================================
@app.route('/api/calculate-fare', methods=['POST'])
def api_calculate_fare():
    data = request.get_json() or {}
    base_fare = float(data.get('base_fare', 500))
    passengers = data.get('passengers', [])
    travel_date = data.get('travel_date', datetime.date.today().strftime('%Y-%m-%d'))

    fare_summary, rule_logs = FareRules.calculate_total_fare(base_fare, passengers, travel_date)

    return jsonify({
        "status": "success",
        "fare_summary": fare_summary,
        "rule_logs": rule_logs
    })

# ==========================================
# 6. Mock Payment & Final Rule Summary Page
# ==========================================
@app.route('/payment', methods=['POST'])
def payment_page():
    bus_id = request.form.get('bus_id')
    travel_date = request.form.get('travel_date')
    selected_seats_str = request.form.get('selected_seats', '')
    selected_seats = [s.strip() for s in selected_seats_str.split(',') if s.strip()]

    bus = get_bus_by_id(bus_id)
    if not bus:
        flash("Bus details not found.", "danger")
        return redirect(url_for('search'))

    # Extract Passenger Details from Form
    passenger_list = []
    for i in range(len(selected_seats)):
        p_name = request.form.get(f'passenger_name_{i}', f'Passenger {i+1}').strip()
        p_age = int(request.form.get(f'passenger_age_{i}', 18))
        p_gender = request.form.get(f'passenger_gender_{i}', 'Other')
        p_phone = request.form.get(f'passenger_phone_{i}', '').strip()

        passenger_list.append({
            'name': p_name,
            'age': p_age,
            'gender': p_gender,
            'phone': p_phone
        })

    # Evaluate Full Booking using Rule Engine
    already_booked = get_booked_seats(bus_id, travel_date)
    rule_eval = RuleEngine.evaluate_full_booking(
        bus=bus,
        requested_seats=selected_seats,
        passenger_list=passenger_list,
        travel_date_str=travel_date,
        already_booked_seats=already_booked,
        payment_successful=True
    )

    if not rule_eval['bookingAllowed']:
        flash(f"Booking Rejected by Rule Engine: {rule_eval['message']}", "danger")
        return redirect(url_for('select_seats', bus_id=bus_id, travel_date=travel_date, passengers=len(selected_seats)))

    return render_template(
        'payment.html',
        bus=bus,
        travel_date=travel_date,
        selected_seats=selected_seats,
        passengers_json=json.dumps(passenger_list),
        fare_summary=rule_eval['fareSummary'],
        rule_summary=rule_eval
    )

# ==========================================
# 7. Process Payment & Persist Booking
# ==========================================
@app.route('/process-payment', methods=['POST'])
def process_payment():
    bus_id = request.form.get('bus_id')
    travel_date = request.form.get('travel_date')
    selected_seats_str = request.form.get('selected_seats', '')
    passengers_json = request.form.get('passengers_json', '[]')
    payment_method = request.form.get('payment_method', 'UPI')

    bus = get_bus_by_id(bus_id)
    selected_seats = [s.strip() for s in selected_seats_str.split(',') if s.strip()]
    passenger_list = json.loads(passengers_json)

    # Re-evaluate Python Rules prior to saving
    already_booked = get_booked_seats(bus_id, travel_date)
    rule_eval = RuleEngine.evaluate_full_booking(
        bus=bus,
        requested_seats=selected_seats,
        passenger_list=passenger_list,
        travel_date_str=travel_date,
        already_booked_seats=already_booked,
        payment_successful=True
    )

    if not rule_eval['bookingAllowed']:
        flash("Booking Failed: Seats no longer available.", "danger")
        return redirect(url_for('search'))

    # Generate Unique Booking ID
    random_num = random.randint(100000, 999999)
    booking_id = f"RB-{random_num}"

    # Prepare Passenger Data with Rule Engine Output
    passengers_to_save = rule_eval['fareSummary']['passenger_details']

    booking_data = {
        'booking_id': booking_id,
        'bus_id': bus_id,
        'travel_date': travel_date,
        'total_amount': rule_eval['fareSummary']['final_total'],
        'status': rule_eval['bookingStatus'],
        'payment_method': payment_method,
        'rule_logs_json': json.dumps(rule_eval['executedRules'])
    }

    # Save to SQLite Database
    success = save_booking(booking_data, passengers_to_save, selected_seats)

    if success:
        flash("Booking confirmed successfully!", "success")
        return redirect(url_for('view_confirmation', booking_id=booking_id))
    else:
        flash("Database error processing booking. Please try again.", "danger")
        return redirect(url_for('search'))

# ==========================================
# 8. Booking Confirmation Ticket
# ==========================================
@app.route('/confirmation/<booking_id>')
def view_confirmation(booking_id):
    booking = get_booking_details(booking_id)
    if not booking:
        flash("Booking ticket not found.", "danger")
        return redirect(url_for('bookings'))

    try:
        rule_logs = json.loads(booking['rule_logs_json']) if booking['rule_logs_json'] else []
    except Exception:
        rule_logs = []

    return render_template(
        'confirmation.html',
        booking=booking,
        rule_logs=rule_logs
    )

# ==========================================
# 9. My Bookings Page
# ==========================================
@app.route('/bookings')
def bookings():
    user_bookings = get_all_bookings()
    return render_template('bookings.html', bookings=user_bookings)

# ==========================================
# 10. Cancellation Refund Evaluation API
# ==========================================
@app.route('/api/evaluate-cancellation', methods=['POST'])
def api_evaluate_cancellation():
    data = request.get_json() or {}
    total_amount = float(data.get('total_amount', 0))
    travel_date = data.get('travel_date', '')
    departure_time = data.get('departure_time', '08:00 AM')

    cancellation_eval = RuleEngine.evaluate_cancellation(total_amount, travel_date, departure_time)

    return jsonify({
        "status": "success",
        "cancellation_eval": cancellation_eval
    })

# ==========================================
# 11. Cancel Booking Action
# ==========================================
@app.route('/cancel-booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = get_booking_details(booking_id)
    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for('bookings'))

    if booking['status'] == 'CANCELLED':
        flash("This booking is already cancelled.", "warning")
        return redirect(url_for('bookings'))

    # Calculate refund using Python Cancellation Rules
    cancellation_eval = RuleEngine.evaluate_cancellation(
        total_amount=booking['total_amount'],
        travel_date_str=booking['travel_date'],
        departure_time_str=booking['departure_time']
    )

    refund_amount = cancellation_eval['refund_amount']
    rule_log = cancellation_eval['rule_logs'][0]

    # Update database status & free up booked seats
    success = cancel_booking_in_db(booking_id, refund_amount, rule_log)

    if success:
        flash(f"Booking {booking_id} cancelled. Refund of ₹{refund_amount:.2f} processed ({cancellation_eval['refund_percentage']}% refund tier).", "success")
    else:
        flash("Failed to process cancellation.", "danger")

    return redirect(url_for('bookings'))

# ==========================================
# 12. "How Rules Work" Educational Page
# ==========================================
@app.route('/rules')
def rules_page():
    return render_template('rules.html')

if __name__ == '__main__':
    print("Starting RuleBus Flask Application on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
