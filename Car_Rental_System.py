from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from pymongo import MongoClient


app = Flask(__name__)


# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['car_rental_system']
collection = db['bookings']
cars_collection = db['cars']  


@app.route('/cancel_booking/<car_number>', methods=['DELETE'])
def cancel_booking(car_number):
    result = collection.delete_one({'car_number': car_number})
    filter = {'indian_car_number': car_number}
    update = {'$set': {'status': 'not booked'}}
    cars_collection.update_one(filter, update)
    
    if result.deleted_count > 0:
        return jsonify({'success': True, 'message': 'Booking canceled successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Booking not found.'}), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        car_number = request.form['car-number']
        renting_date = request.form['renting-date']
        return_date = request.form['return-date']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        phone = phone[:10]
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({'success': False, 'message': 'Invalid phone number.'}), 400
        
        # Save data to MongoDB
        booking = {
            'car_number': car_number,
            'renting_date': renting_date,
            'return_date': return_date,
            'name': name,
            'email': email,
            'phone': phone
        }
        collection.insert_one(booking)


        # Update car status to 'booked' in MongoDB
        filter = {'indian_car_number': car_number, 'status': 'not booked'}
        update = {'$set': {'status': 'booked'}}
        update_result = cars_collection.update_one(filter, update)


        # Check if the car status was updated successfully
        if update_result.modified_count == 0:
            print(f"Car with number {car_number} is already booked or not found.")


        return redirect(url_for('index'))


    latest_bookings = collection.find().sort('_id', -1).limit(5)
    bookings_data = [{
        'car_number': booking['car_number'],
        'renting_date': booking['renting_date'],
        'return_date': booking['return_date'],
        'name': booking['name'],
        'email': booking['email'],
        'phone': booking['phone']
    } for booking in latest_bookings]


    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <link href='ico/favicon.ico' rel='icon'>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Car Rental System</title>
        <style>
            body {
                font-family: 'Times New Roman', Times, serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }
            header {
                background-color: rgba(211, 211, 211, 0.7);
                color: Black;
                text-align: center;
                padding: 20px;
                font-size: 32px;
                position: relative;
                z-index: 2;
            }
            nav ul {
                list-style: none;
                overflow: hidden;
                position: relative;
                z-index: 2;
            }
            nav ul li {
                float: left;
                margin-right: 20px;
            }
            nav ul li a {
                display: block;
                padding: 10px 20px;
                color: white;
                text-decoration: none;
                font-size: 18px;
                background-color: rgba(68, 68, 68, 0.2);
                border-radius: 8px;
                transition: background-color 0.3s;
            }
            nav ul li a:hover {
                background-color: rgba(85, 85, 85, 0.2);
            }
            main {
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
                position: relative;
                z-index: 2;
            }
            section {
                margin-bottom: 30px;
                padding: 20px;
                background-color: rgba(249, 249, 249, 0.2);
                border-radius: 4px;
                font-size: 20px;
                opacity: 0.9;
            }
            footer {
                background-color: rgba(51, 51, 51, 0.2);
                color: white;
                text-align: center;
                padding: 10px;
                position: fixed;
                bottom: 0;
                width: 100%;
                border-top: 1px solid rgba(68, 68, 68, 0.2);
                font-size: 16px;
                z-index: 2;
            }
            video#background-video {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                z-index: 1;
                opacity: 0.5;
            }
            .button-17 {
                align-items: center;
                appearance: none;
                background-color: #fff;
                border-radius: 24px;
                border-style: none;
                box-shadow: rgba(0, 0, 0, .2) 0 3px 5px -1px,rgba(0, 0, 0, .14) 0 6px 10px 0,rgba(0, 0, 0, .12) 0 1px 18px 0;
                box-sizing: border-box;
                color: #3c4043;
                cursor: pointer;
                display: inline-flex;
                fill: currentcolor;
                font-family: "Google Sans",Roboto,Arial,sans-serif;
                font-size: 14px;
                font-weight: 500;
                height: 48px;
                justify-content: center;
                letter-spacing: .25px;
                line-height: normal;
                max-width: 100%;
                overflow: visible;
                padding: 2px 24px;
                position: relative;
                text-align: center;
                text-transform: none;
                transition: box-shadow 280ms cubic-bezier(.4, 0, .2, 1),opacity 15ms linear 30ms,transform 270ms cubic-bezier(0, 0, .2, 1) 0ms;
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                width: auto;
                will-change: transform,opacity;
                z-index: 0;
            }
            .button-17:hover {
                background: #F6F9FE;
                color: #174ea6;
            }
            .button-17:active {
                box-shadow: 0 4px 4px 0 rgb(60 64 67 / 30%), 0 8px 12px 6px rgb(60 64 67 / 15%);
                outline: none;
            }
            .button-17:focus {
                outline: none;
                border: 2px solid #4285f4;
            }
            .button-17:not(:disabled) {
                box-shadow: rgba(60, 64, 67, .3) 0 1px 3px 0, rgba(60, 64, 67, .15) 0 4px 8px 3px;
            }
            .button-17:not(:disabled):hover {
                box-shadow: rgba(60, 64, 67, .3) 0 2px 3px 0, rgba(60, 64, 67, .15) 0 6px 10px 4px;
            }
            .button-17:not(:disabled):focus {
                box-shadow: rgba(60, 64, 67, .3) 0 1px 3px 0, rgba(60, 64, 67, .15) 0 4px 8px 3px;
            }
            .button-17:not(:disabled):active {
                box-shadow: rgba(60, 64, 67, .3) 0 4px 4px 0, rgba(60, 64, 67, .15) 0 8px 12px 6px;
            }
            .button-17:disabled {
                box-shadow: rgba(60, 64, 67, .3) 0 1px 3px 0, rgba(60, 64, 67, .15) 0 4px 8px 3px;
            }
            .button-56 {
                align-items: center;
                background-color: #fee6e3;
                border: 2px solid #111;
                border-radius: 8px;
                box-sizing: border-box;
                color: #111;
                cursor: pointer;
                display: flex;
                font-family: Inter,sans-serif;
                font-size: 16px;
                height: 48px;
                justify-content: center;
                line-height: 24px;
                max-width: 100%;
                padding: 0 25px;
                position: relative;
                text-align: center;
                text-decoration: none;
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
            }
            .button-56:after {
                background-color: #111;
                border-radius: 8px;
                content: "";
                display: block;
                height: 48px;
                left: 0;
                width: 100%;
                position: absolute;
                top: 0;
                transform: translate(8px, 8px);
                transition: transform .2s ease-out;
                z-index: -1;
            }
            .button-56:hover:after {
                transform: translate(0, 0);
            }
            .button-56:active {
                background-color: #ffdeda;
                outline: 0;
            }
            .button-56:hover {
                outline: 0;
            }
            @media (min-width: 768px) {
                .button-56 {
                    padding: 0 40px;
                }
            }
            #customer-form {
                padding-top: 20px;
                margin-top: 20px;
            }
            /* Add padding and margin to increase distance */
        </style>
    </head>
    <body>
        <video autoplay loop muted id="background-video">
            <source src="{{ url_for('static', filename='background-video.mp4') }}" type="video/mp4">
            Your browser does not support the video tag.
        </video>


        <header>
            <h1>Car Rental System</h1>
        </header>


        <nav>
            <ul>
                <li><a href="/" class="button-17">Home</a></li>
                <li><a href="#about" class="button-17">About</a></li>
                <li><a href="#services" class="button-17">Services</a></li>
                <li><a href="#contact" class="button-17">Contact</a></li>
            </ul>
        </nav>


        <main>
            <section id="services">
                <h2>Our Services</h2>
                <button id="book-car-btn" class="button-56" role="button">Book Your Car</button>
                <button id="see-cars-btn" class="button-56" role="button">See Cars</button>


                <form id="customer-form" style="display: none;" action="/" method="POST">
                    <label for="car-number">Car Number:</label>
                    <input type="text" id="car-number" name="car-number" required><br><br>


                    <label for="renting-date">Renting Date:</label>
                    <input type="date" id="renting-date" name="renting-date" required><br><br>


                    <label for="return-date">Return Date:</label>
                    <input type="date" id="return-date" name="return-date" required><br><br>


                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required><br><br>


                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required><br><br>


                    <label for="phone">Phone:</label>
                    <input type="tel" id="phone" name="phone" required><br><br>


                            <input type="submit" value="Submit" class="button-56">
                </form>
            </section>


            <section id="latest-bookings">
                <h2>Latest Bookings</h2>
                <ul id="bookings-list">
                    {% for booking in bookings_data %}
                    <li>
                        <strong>Car Number:</strong> {{ booking.car_number }}<br>
                        <strong>Renting Date:</strong> {{ booking.renting_date }}<br>
                        <strong>Return Date:</strong> {{ booking.return_date }}<br>
                        <strong>Name:</strong> {{ booking.name }}<br>
                        <strong>Email:</strong> {{ booking.email }}<br>
                        <strong>Phone:</strong> {{ booking.phone }}<br>
                        <button class="button-56" onclick="cancelBooking('{{ booking.car_number }}')">Cancel</button>
                    </li>
                    {% endfor %}
                </ul>
            </section>
                </form>
            </section>


            <section id="car-list" style="display:none;">
                <h2>Available Cars</h2>
                <ul id="car-list-items"></ul>
            </section>
            <section id="about">
                <h2>About Us</h2>
                <p>I am Dixit data science student passionate about technology and innovation. I developed this platform to simplify and enhance the car rental experience.</p>
            </section>


            <section id="contact">
                <h2>Contact Us</h2>
                <p>Email: dixit.txt@gmail.com</p>
                <p>Phone: +91 93180 10365(Dixit)</p>
            </section>
        </main>


        <footer>
            <p>&copy; 2024 Car Rental System. All rights reserved.</p>
        </footer>


<script>
    document.getElementById("book-car-btn").addEventListener("click", function() {
        document.getElementById("customer-form").style.display = "block";
        document.getElementById("car-list").style.display = "none";
    });


    document.getElementById("see-cars-btn").addEventListener("click", function() {
        fetch("/get_cars")
        .then(response => response.json())
        .then(data => {
            const carList = document.getElementById("car-list-items");
            carList.innerHTML = "";
            data.cars.forEach(car => {
                const li = document.createElement("li");
                li.textContent = car;
                carList.appendChild(li);
            });
            document.getElementById("car-list").style.display = "block";
            document.getElementById("customer-form").style.display = "none";
        });
    });


    function cancelBooking(carNumber) {
        fetch(`/cancel_booking/${carNumber}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Failed to cancel booking.");
            }
        });
    }
</script>
</body>
</html>
    '''
    return render_template_string(html_content, bookings_data=bookings_data)


@app.route('/get_cars', methods=['GET'])
def get_cars():
    cars = cars_collection.find({})
    car_list = []
    for car in cars:
        status = car["status"]
        if (status == "not booked"):
            car_info = f"Car name: {car['car_name']}, Number: {car['indian_car_number']}, rent: {car['rent_price_per_day']}, status: {car['status']}"
            car_list.append(car_info)
    return jsonify({'cars': car_list})
if __name__ == '__main__':
    app.run(debug=True)