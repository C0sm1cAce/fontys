from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_wtf.csrf import CSRFProtect
from form import CheckoutForm

app = Flask(__name__)
# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Set a secret key for session security
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/houses")
def houses():
    return render_template("houses.html")

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")

@app.route("/confirm", methods=['GET', 'POST'])
def confirm():
    return render_template("confirm.html")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()

    if request.method == 'POST' and form.validate_on_submit():
        print("POSTED!!!!!")
        # Access form data
        name = form.name.data
        email = form.email.data
        address = form.address.data
        checkin_date = form.checkin.data
        checkout_date = form.checkout.data
        card_number = form.cardnumber.data
        expiration_date = form.expiration.data
        cvv = form.cvv.data
        
        try:
            # Store data in the database (you need to modify this part based on your schema)
            conn = sqlite3.connect('hotel.db')
            cursor = conn.cursor()

            # Insert data into Guests table
            cursor.execute("INSERT INTO Guests (name, email, address) VALUES (?, ?, ?)", (name, email, address))
            guest_id = cursor.lastrowid  # Retrieve the ID of the last inserted guest

            # Insert data into Reservations table
            cursor.execute("INSERT INTO Reservations (guest_id, check_in_date, check_out_date) VALUES (?, ?, ?)",
                        (guest_id, checkin_date, checkout_date))

            # Insert data into CreditCard table
            cursor.execute("INSERT INTO CreditCard (guest_id, card_number, expiration_date, cvv) VALUES (?, ?, ?, ?)",
                        (guest_id, card_number, expiration_date, cvv))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            flash(f"Database Error: {str(e)}", 'error')
            
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field '{getattr(form, field).label.text}': {error}", 'error')
                
        # Redirect to a confirmation page or another route
        return redirect(url_for('checkout'))

    # If it's a GET request, render the checkout form
    return render_template("checkout.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)