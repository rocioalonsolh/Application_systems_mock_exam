from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aaldb.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Create some fake user data
def create_fake_users():
    for _ in range(5):
        user = User(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.email(),
            role=fake.random_element(elements=('Admin', 'User'))
        )
        db.session.add(user)
    db.session.commit()

# Route to display users
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Route to add a new user
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        role = request.form['role']

        new_user = User(firstname=firstname, lastname=lastname, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add-user.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_fake_users()
    app.run(port=5001, debug=True)
