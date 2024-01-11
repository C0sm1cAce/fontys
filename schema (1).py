import sqlite3

# Function to create the schema
def create_schema():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Guests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Guests (
            guest_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL CHECK(name NOT LIKE '%[0-9]%'),
            email TEXT NOT NULL CHECK(email LIKE '%@%'),
            address TEXT
        );
    ''')

    # Reservations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            reservation_id INTEGER PRIMARY KEY,
            guest_id INTEGER,
            check_in_date DATE NOT NULL CHECK(check_in_date IS DATE(check_in_date)),
            check_out_date DATE NOT NULL CHECK(check_out_date IS DATE(check_out_date) AND check_out_date >= check_in_date),
            FOREIGN KEY (guest_id) REFERENCES Guests(guest_id)
        );
    ''')

    # CreditCard Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CreditCard (
            credit_card_id INTEGER PRIMARY KEY,
            guest_id INTEGER,
            card_number TEXT NOT NULL CHECK(card_number GLOB '[0-9]*' AND LENGTH(card_number) = 16),
            expiration_date DATE NOT NULL CHECK(expiration_date IS DATE(expiration_date)),
            cvv INTEGER NOT NULL CHECK(cvv >= 000 AND cvv <= 999),
            FOREIGN KEY (guest_id) REFERENCES Guests(guest_id)
        );
    ''')

    conn.commit()
    conn.close()

# Function to populate sample data
def populate_sample_data():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Sample data for Guests table
    cursor.executemany('''
        INSERT INTO Guests (name, email, address) VALUES (?, ?, ?);
    ''', [
        ('Mirza Areeb', 'mirza@anonymous.com', 'Mars'),
        ('Hamza Khattak', 'khattak@anonymous.com', 'Venus')
    ])

    # Sample data for Reservations table
    cursor.executemany('''
        INSERT INTO Reservations (guest_id, check_in_date, check_out_date) VALUES (?, ?, ?);
    ''', [
        (1, '2023-01-01', '2023-01-05'),
        (2, '2023-02-15', '2023-02-20')
    ])

    # Sample data for CreditCard table
    cursor.executemany('''
        INSERT INTO CreditCard (guest_id, card_number, expiration_date, cvv) VALUES (?, ?, ?, ?);
    ''', [
        (1, '1234567890123456', '2025-12-31', 123),
        (2, '9876543210987654', '2024-10-31', 456)
    ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_schema()
    populate_sample_data()
    print("Database schema and sample data created successfully in hotel.db.")
