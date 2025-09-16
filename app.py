from flask import Flask, render_template, request, redirect, url_for, session

from Test.Connectec2 import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERNAME = 'admin'
PASSWORD = 'password123'

# In-memory user store (you can later switch to DB)
users = {
    'admin': {'name': 'Admin', 'email': 'admin@example.com', 'password': 'password123'}
}


@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    books = [
        {"id": 1, "title": "Atomic Habits", "image": "https://m.media-amazon.com/images/I/81eB+7+CkUL.jpg","price":12.99},
        {"id": 2, "title": "Rich Dad Poor Dad", "image": "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg","price":10.99},
        {"id": 3, "title": "The Alchemist", "image": "https://m.media-amazon.com/images/I/71aFt4+OTOL.jpg","price":9.99},
        {"id": 4, "title": "Harry Potter", "image": "https://m.media-amazon.com/images/I/81iqZ2HHD-L.jpg","price":11.99},
        {"id": 5, "title": "To Kill a Mockingbird", "image": "https://m.media-amazon.com/images/I/710jnzKlDTL.jpg","price":12.99},
        {"id": 6, "title": "Think and Grow Rich", "image": "https://m.media-amazon.com/images/I/81WcnNQ-TBL.jpg","price":5.99},
        {"id": 7, "title": "The Power of Now", "image": "https://m.media-amazon.com/images/I/71UwSHSZRnS.jpg","price":15.99},
        {"id": 8, "title": "The Subtle Art...", "image": "https://m.media-amazon.com/images/I/91uwocAMtSL.jpg","price":10.99},
        {"id": 9, "title": "Ikigai", "image": "https://m.media-amazon.com/images/I/71KilybDOoL.jpg","price":6.99}
    ]
    return render_template('home.html', books=books,username=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        pwd = request.form['password']

        #fetching user data from database
        connect_obj=Database()
        user_data=connect_obj.get_user_by_name(email)
        if user_data[3] == str(pwd):
            session.permanent = True
            session['user'] = user_data[1]
            session['cart'] = []
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/update-cart', methods=['POST'])
def update_cart():
    if 'user' not in session:
        return {'status': 'unauthorized'}, 401

    data = request.json
    book_id = int(data['book_id'])
    quantity = int(data['quantity'])

    db = Database()
    user = db.get_user_by_name(session['user'])
    user_id = user[0]

    if quantity > 0:
        db.upsert_cart(user_id, book_id, quantity)
    else:
        db.remove_from_cart(user_id, book_id)

    return {'status': 'updated'}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        connect_obj=Database()
        connect_obj.insert_user(name,email,password)
        # Use email as the unique identifier
        if email in users:
            return render_template('register.html', error="Email already exists!")

        # Store new user
        users[email] = {'name': name, 'email': email, 'password': password}
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('checkout.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
