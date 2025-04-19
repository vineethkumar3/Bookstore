from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy credentials
USERNAME = 'admin'
PASSWORD = 'password123'

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    books = [
        {"id": 1, "title": "Atomic Habits", "image": "https://m.media-amazon.com/images/I/81eB+7+CkUL.jpg"},
        {"id": 2, "title": "Rich Dad Poor Dad", "image": "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg"},
        {"id": 3, "title": "The Alchemist", "image": "https://m.media-amazon.com/images/I/71aFt4+OTOL.jpg"},
        {"id": 4, "title": "Harry Potter", "image": "https://m.media-amazon.com/images/I/81iqZ2HHD-L.jpg"},
        {"id": 5, "title": "To Kill a Mockingbird", "image": "https://m.media-amazon.com/images/I/710jnzKlDTL.jpg"},
        {"id": 6, "title": "Think and Grow Rich", "image": "https://m.media-amazon.com/images/I/81WcnNQ-TBL.jpg"},
        {"id": 7, "title": "The Power of Now", "image": "https://m.media-amazon.com/images/I/71UwSHSZRnS.jpg"},
        {"id": 8, "title": "The Subtle Art...", "image": "https://m.media-amazon.com/images/I/91uwocAMtSL.jpg"},
        {"id": 9, "title": "Ikigai", "image": "https://m.media-amazon.com/images/I/71KilybDOoL.jpg"}
    ]

    return render_template('home.html',books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == USERNAME and pwd == PASSWORD:
            session['user'] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
