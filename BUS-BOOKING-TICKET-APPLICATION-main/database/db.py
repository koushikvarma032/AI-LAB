import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db_connection():
    """Establishes and returns a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database tables and seeds initial sample bus data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Buses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT UNIQUE NOT NULL,
            bus_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            duration TEXT NOT NULL,
            bus_type TEXT NOT NULL,
            total_seats INTEGER NOT NULL DEFAULT 30,
            available_seats INTEGER NOT NULL DEFAULT 30,
            base_fare REAL NOT NULL
        )
    ''')

    # 2. Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT UNIQUE NOT NULL,
            bus_id INTEGER NOT NULL,
            travel_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            payment_method TEXT,
            created_at TEXT NOT NULL,
            rule_logs_json TEXT,
            refund_amount REAL DEFAULT 0.0,
            FOREIGN KEY (bus_id) REFERENCES buses (id)
        )
    ''')

    # 3. Passengers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            base_fare REAL NOT NULL,
            discount_amount REAL NOT NULL DEFAULT 0.0,
            discount_reason TEXT,
            final_fare REAL NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES bookings (booking_id)
        )
    ''')

    # 4. Booked Seats Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booked_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id INTEGER NOT NULL,
            travel_date TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            booking_id TEXT NOT NULL,
            FOREIGN KEY (bus_id) REFERENCES buses (id),
            FOREIGN KEY (booking_id) REFERENCES bookings (booking_id)
        )
    ''')

    conn.commit()

    # Seed default sample buses if table is empty
    cursor.execute('SELECT COUNT(*) FROM buses')
    if cursor.fetchone()[0] == 0:
        sample_buses = [
            ('RB-101', 'Gujarat Travels', 'Ahmedabad', 'Rajkot', '08:00 AM', '01:00 PM', '5.0 hrs', 'AC Seater (2+2)', 30, 30, 500.0),
            ('RB-102', 'Eagle Express', 'Ahmedabad', 'Rajkot', '10:00 PM', '03:00 AM', '5.0 hrs', 'AC Sleeper (2+1)', 30, 30, 600.0),
            ('RB-201', 'Deccan Travels', 'Mumbai', 'Pune', '07:00 AM', '10:30 AM', '3.5 hrs', 'AC Seater (2+2)', 30, 30, 400.0),
            ('RB-202', 'Western Star', 'Mumbai', 'Pune', '02:00 PM', '05:30 PM', '3.5 hrs', 'Luxury Sleeper (2+1)', 30, 30, 450.0),
            ('RB-301', 'Green Line Travels', 'Bangalore', 'Chennai', '06:00 AM', '01:00 PM', '7.0 hrs', 'AC Multi-Axle', 30, 30, 750.0),
            ('RB-401', 'Pink City Deluxe', 'Delhi', 'Jaipur', '06:30 AM', '12:00 PM', '5.5 hrs', 'AC Seater (2+2)', 30, 30, 550.0),
            ('RB-501', 'Coastal Connect', 'Hyderabad', 'Vijayawada', '08:30 AM', '02:30 PM', '6.0 hrs', 'AC Sleeper (2+1)', 30, 30, 650.0),
        ]
        cursor.executemany('''
            INSERT INTO buses (bus_number, bus_name, source, destination, departure_time, arrival_time, duration, bus_type, total_seats, available_seats, base_fare)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_buses)
        conn.commit()

    conn.close()

def get_all_cities():
    """Returns a list of unique source and destination cities for search dropdowns."""
    conn = get_db_connection()
    sources = [row['source'] for row in conn.execute('SELECT DISTINCT source FROM buses').fetchall()]
    destinations = [row['destination'] for row in conn.execute('SELECT DISTINCT destination FROM buses').fetchall()]
    conn.close()
    all_cities = sorted(list(set(sources + destinations)))
    return all_cities

def search_buses(source, destination):
    """Searches buses matching source and destination."""
    conn = get_db_connection()
    query = 'SELECT * FROM buses WHERE LOWER(source) = LOWER(?) AND LOWER(destination) = LOWER(?)'
    buses = conn.execute(query, (source, destination)).fetchall()
    conn.close()
    return [dict(b) for b in buses]

def get_bus_by_id(bus_id):
    """Fetches single bus details by ID."""
    conn = get_db_connection()
    bus = conn.execute('SELECT * FROM buses WHERE id = ?', (bus_id,)).fetchone()
    conn.close()
    return dict(bus) if bus else None

def get_booked_seats(bus_id, travel_date):
    """Returns list of seat numbers already booked for a specific bus on a travel date."""
    conn = get_db_connection()
    query = '''
        SELECT bs.seat_number 
        FROM booked_seats bs
        JOIN bookings b ON bs.booking_id = b.booking_id
        WHERE bs.bus_id = ? AND bs.travel_date = ? AND b.status = 'CONFIRMED'
    '''
    rows = conn.execute(query, (bus_id, travel_date)).fetchall()
    conn.close()
    return [r['seat_number'] for r in rows]

def save_booking(booking_data, passenger_list, seat_numbers):
    """Persists booking, passengers, and booked seats into SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert Booking
        cursor.execute('''
            INSERT INTO bookings (booking_id, bus_id, travel_date, total_amount, status, payment_method, created_at, rule_logs_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_data['booking_id'],
            booking_data['bus_id'],
            booking_data['travel_date'],
            booking_data['total_amount'],
            booking_data['status'],
            booking_data['payment_method'],
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            booking_data['rule_logs_json']
        ))

        # Insert Passengers
        for idx, p in enumerate(passenger_list):
            cursor.execute('''
                INSERT INTO passengers (booking_id, seat_number, name, age, gender, phone, base_fare, discount_amount, discount_reason, final_fare)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                booking_data['booking_id'],
                seat_numbers[idx],
                p['name'],
                p['age'],
                p['gender'],
                p['phone'],
                p['base_fare'],
                p['discount_amount'],
                p['discount_reason'],
                p['final_fare']
            ))

            # Insert Booked Seat record if CONFIRMED
            if booking_data['status'] == 'CONFIRMED':
                cursor.execute('''
                    INSERT INTO booked_seats (bus_id, travel_date, seat_number, booking_id)
                    VALUES (?, ?, ?, ?)
                ''', (
                    booking_data['bus_id'],
                    booking_data['travel_date'],
                    seat_numbers[idx],
                    booking_data['booking_id']
                ))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Database error saving booking: {e}")
        return False
    finally:
        conn.close()

def get_booking_details(booking_id):
    """Retrieves complete booking details including bus and passenger records."""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, bus.bus_name, bus.bus_number, bus.source, bus.destination, bus.departure_time, bus.arrival_time, bus.bus_type
        FROM bookings b
        JOIN buses bus ON b.bus_id = bus.id
        WHERE b.booking_id = ?
    ''', (booking_id,)).fetchone()

    if not booking:
        conn.close()
        return None

    passengers = conn.execute('''
        SELECT * FROM passengers WHERE booking_id = ?
    ''', (booking_id,)).fetchall()

    conn.close()
    
    booking_dict = dict(booking)
    booking_dict['passengers'] = [dict(p) for p in passengers]
    return booking_dict

def get_all_bookings():
    """Retrieves all user bookings ordered by creation date."""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, bus.bus_name, bus.bus_number, bus.source, bus.destination, bus.departure_time
        FROM bookings b
        JOIN buses bus ON b.bus_id = bus.id
        ORDER BY b.id DESC
    ''').fetchall()
    conn.close()
    return [dict(b) for b in bookings]

def cancel_booking_in_db(booking_id, refund_amount, rule_log_entry):
    """Updates booking status to CANCELLED and removes booked seats."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Update status and refund
        cursor.execute('''
            UPDATE bookings 
            SET status = 'CANCELLED', refund_amount = ? 
            WHERE booking_id = ?
        ''', (refund_amount, booking_id))

        # Delete booked seats so seats become available again
        cursor.execute('''
            DELETE FROM booked_seats WHERE booking_id = ?
        ''', (booking_id,))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error cancelling booking: {e}")
        return False
    finally:
        conn.close()
