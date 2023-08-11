import re
import bcrypt
import db
import json
import logging
import random
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'sdakjndsahjgbdhgjvdhjvdjdsjkndasjbkjbkdhad'

user_logged_in = False

# Configure the logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello_world():  # put application's code here
    if not user_logged_in:
        return redirect('/login')
    return '404'


@app.route('/home')
def home():
    if 'email' in session:
        email = session['email']
        user_scores = db.getUserScores(email)

        scores = []
        i = 0

        for score in user_scores:
            if i == 5:
                break
            scores.append(score)
            i += 1
        return render_template('home.html', email=email, user_scores=scores)
    else:
        return redirect('login')


# Route to handle the quiz
@app.route('/quiz')
def quiz():
    if 'email' in session:
        email = session['email']
        universe = request.args.get('universe')
        email = request.args.get('email')
        questions = db.fetchQuestions(universe)

        questions = list(questions)
        random_questions = random.sample(questions, 5)
        json_data = json.dumps(random_questions)

        return render_template('quiz.html', questions=json_data, email=email, universe=universe)
    else:
        return redirect('login')


@app.route('/store_score', methods=['POST'])
def store_score():
    email = request.form.get('email')
    universe = request.form.get('universe')
    score = int(request.form.get('score'))

    db.storeUserScore(email, universe, score)

    return "Score stored successfully"  # You can return any response you want here


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
    if "email" in session:
        return render_template('home.html', email=session['email'])
    if request.method == 'POST':
        # Perform form validation and display errors
        email = request.form.get('email')
        password = request.form.get('password')

        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

        email_error = ''
        password_error = ''
        db_error = ''

        if not re.match(email_regex, email):
            email_error = 'Please enter a valid email address.'

        if password == '':
            password_error = 'Please enter your password!'

        if email_error or password_error:
            # Pass errors and form data to the template
            return render_template('login.html', email_error=email_error, password_error=password_error,
                                   data=request.form)

        else:
            print('In else')
            try:
                user = db.getUserByEmail(email)
                print(user)
                if user is not None:
                    dbPassword = user['password']

                    if bcrypt.checkpw(password.encode('utf-8'), dbPassword):
                        session['email'] = email
                        return redirect('/home')
                    else:
                        db_error = 'Invalid username or password! Try again.'
                        return render_template('login.html', db_error=db_error,
                                               data=request.form)
                else:
                    db_error = 'Invalid username or password! Try again.'
                    return render_template('login.html', db_error=db_error,
                                           data=request.form)
            except Exception:
                db_error = "Something went wrong! Please try again later."
                return render_template('login.html', db_error=db_error,
                                       data=request.form)


@app.route('/logged_in')
def logged_in():
    if 'email' in session:
        email = session['email']
        return render_template('home.html', email=email)

    else:
        return redirect(url_for('login'))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("login.html")
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
