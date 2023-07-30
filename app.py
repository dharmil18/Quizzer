import re
import bcrypt
import db
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'sdakjndsahjgbdhgjvdhjvdjdsjkndasjbkjbkdhad'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    if "email" in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        # Perform form validation and display errors
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        name_regex = r'^[A-Za-z]+$'
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        password_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$'

        first_name_error = ''
        last_name_error = ''
        email_error = ''
        password_error = ''
        db_error = ''

        if not re.match(name_regex, first_name):
            first_name_error = 'Please enter a valid first name.'

        if not re.match(name_regex, last_name):
            last_name_error = 'Please enter a valid last name.'

        if not re.match(email_regex, email):
            email_error = 'Please enter a valid email address.'

        if not re.match(password_regex, password):
            password_error = 'Password must be at least 8 characters long and contain at least one number, ' \
                             'one lowercase letter, one uppercase letter, and one special character.'

        if first_name_error or last_name_error or email_error or password_error:
            # Pass errors and form data to the template
            return render_template('signup.html', first_name_error=first_name_error, last_name_error=last_name_error,
                                   email_error=email_error, password_error=password_error,
                                   data=request.form)

        # If all validations pass, handle the signup logic here
        # e.g., add the user to the database, display a success message, etc.
        # For brevity, I'm omitting the actual signup logic here.

        # Redirect to a success page or some other appropriate route
        # return redirect('/signup-success')

        try:
            # Check whether email already exists
            userExists = db.existsByEmail(email)

            if userExists:
                db_error = "User already exists! Try another email."
                return render_template('signup.html', db_error=db_error,
                                       data=request.form)

        except Exception:
            db_error = "Something went wrong! Please try again later."
            return render_template('signup.html', db_error=db_error,
                                   data=request.form)

        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

        newUser = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hashedPassword
        }

        try:
            # Registering user and saving the credentials in the database
            userInfoSaved = db.registerUser(newUser)

            if userInfoSaved:
                return redirect('/login')

            db_error = "Something went wrong! Please try again later."
            return render_template('signup.html', db_error=db_error,
                                   data=request.form)

        except Exception:
            db_error = "Something went wrong! Please try again later."
            return render_template('signup.html', db_error=db_error,
                                   data=request.form)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
