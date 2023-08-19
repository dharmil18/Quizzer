import re
import bcrypt
import db
import json
import logging
import random
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sdakjndsahjgbdhgjvdhjvdjdsjkndasjbkjbkdhad'

user_logged_in = False

# Configure the logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello_world():  # put application's code here
    """
    Route for the home page.

    This function checks if a user is logged in. If the user is not logged in,
    it redirects them to the login page. If the user is logged in, it returns
    a '404' response.

    Returns:
        str or redirect:
        Returns '404' if the user is logged in, otherwise
        redirects to the '/login' page.
    """
    if not user_logged_in:
        return redirect('/login')
    return '404'


@app.route('/home')
def home():
    """
    Route for the home page.

    This function checks if a user is logged in by verifying if the 'email'
    key is present in the session. If the user is logged in, it retrieves
    the user's scores from the database, sorts them by 'quizDateTime' in
    descending order, and selects the top 5 scores to display on the home page.
    It then renders the 'home.html' template, passing the user's email and
    the selected scores as context.

    Returns:
        str or redirect:
        Renders the 'home.html' template with user information and scores if the user is logged in,
        otherwise redirects to the 'login' page.
    """
    if 'email' in session:
        email = session['email']
        user_scores = db.getUserScores(email)

        scores = list(user_scores)

        sorted_scores = sorted(scores, key=lambda x: x['quizDateTime'], reverse=True)
        i = 0

        onlyScores = []

        for score in sorted_scores:
            if i == len(sorted_scores) or i == 5:
                break
            onlyScores.append(score)
            i += 1
        return render_template('home.html', email=email, user_scores=onlyScores)
    else:
        return redirect('login')


@app.route('/dashboard')
def dashboard():
    """
    Route for the dashboard page.

    This function checks if a user is logged in by verifying if the 'email'
    key is present in the session. If the user is logged in, it retrieves
    the user's scores from the database. It then calculates various statistics
    including the highest score, lowest score, average score, and the number of quizzes
    taken. It also sorts the scores by 'quizDateTime' in descending order and renders
    the 'dashboard.html' template, passing user information and calculated statistics
    as context.

    Returns:
        str or redirect:
        Renders the 'dashboard.html' template with user information and
        calculated statistics if the user is logged in, otherwise redirects to the 'login'
        page.
    """
    if 'email' in session:
        email = session['email']
        scores = db.getUserScores(email)

        scores = list(scores)

        if len(scores) != 0:

            # Extract scores from the data
            score_values = [entry['score'] for entry in scores]

            # Calculate highest score
            highest_score = max(score_values)

            # Calculate lowest score
            lowest_score = min(score_values)

            # Calculate average score
            average_score = round((sum(score_values) / len(score_values)), 2)

            sorted_scores = sorted(scores, key=lambda x: x['quizDateTime'], reverse=True)

            for score in sorted_scores:
                print(score)

            return render_template('dashboard.html', email=email, user_scores=sorted_scores,
                                   highest_score=highest_score,
                                   lowest_score=lowest_score, average_score=average_score, numOfQuiz=len(score_values))
        else:
            return render_template('dashboard.html', email=email)
    else:
        return redirect('login')


# Route to handle the quiz
@app.route('/quiz')
def quiz():
    """
    Route for the quiz page.

    This function checks if a user is logged in by verifying if the 'email'
    key is present in the session. If the user is logged in, it retrieves
    a selected 'universe' and 'email' from the request arguments, fetches
    a set of questions related to the specified universe from the database,
    selects 5 random questions from the retrieved set, and converts them to
    JSON format. Finally, it renders the 'quiz.html' template, passing the
    JSON-encoded questions, user's email, and selected universe as context.

    Returns:
        str or redirect:
        Renders the 'quiz.html' template with the selected
        questions, user information, and universe if the user is logged in,
        otherwise redirects to the 'login' page.
    """
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
    """
    Route for storing a user's quiz score.

    This function handles POST requests to store a user's quiz score in the database.
    It retrieves the user's email, selected universe, quiz score, and current date and time
    from the form data sent with the request. It then calls the 'storeUserScore' function
    from the database module to store the score information. Finally, it returns a response
    indicating that the score has been stored successfully.

    Returns:
        str: A message indicating that the score has been stored successfully.
    """
    email = request.form.get('email')
    universe = request.form.get('universe')
    score = int(request.form.get('score'))
    quizDateTime = datetime.now()

    db.storeUserScore(email, universe, score, quizDateTime)

    return "Score stored successfully"  # You can return any response you want here


@app.route('/login', methods=['GET'])
def login():
    """
    Route for displaying the login page.

    This function handles GET requests to display the login page. It renders
    the 'login.html' template, allowing users to log in.

    Returns:
        str: The rendered login page.
    """
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def signup():
    """
     Route for displaying the signup page.

     This function handles GET requests to display the signup page. It renders
     the 'signup.html' template, allowing users to sign up for the application.

     Returns:
         str: The rendered signup page.
     """
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    """
    Route for user registration.

    This function handles POST requests for user registration. It performs form validation,
    checking the first name, last name, email, and password fields for validity. If there
    are any validation errors, it returns the 'signup.html' template with error messages.
    If the provided email already exists in the database, it displays an error message.
    If registration is successful, it hashes the user's password, stores the user's information
    in the database, and redirects the user to the login page.

    Returns:
        str or redirect:
        Renders the 'signup.html' template with error messages or redirects
        to the login page upon successful registration.
    """
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
    """
     Route for user authentication.

     This function handles POST requests for user authentication. It performs form validation,
     checking the email and password fields for validity. If there are any validation errors,
     it returns the 'login.html' template with error messages. If authentication is successful,
     it sets the user's email in the session and redirects the user to the home page.

     Returns:
         str or redirect:
         Renders the 'login.html' template with error messages or redirects
         to the home page upon successful authentication.
     """
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
    """
    Route for checking if a user is logged in.

    This function checks if a user is logged in by verifying if the 'email' key is present
    in the session. If the user is logged in, it retrieves the user's email and renders
    the 'home.html' template with the email as context. If the user is not logged in,
    it redirects them to the login page.

    Returns:
        str or redirect:
        Renders the 'home.html' template with the user's email if the user
        is logged in, otherwise redirects to the login page.
    """
    if 'email' in session:
        email = session['email']
        return render_template('home.html', email=email)

    else:
        return redirect(url_for('login'))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    """
     Route for user logout.

     This function handles GET and POST requests for user logout. If the user is currently
     logged in (indicated by the presence of the 'email' key in the session), it removes
     the 'email' key from the session, effectively logging the user out, and then renders
     the 'login.html' template. If the user is not logged in, it still renders the 'login.html'
     template.

     Returns:
         str:
         Renders the 'login.html' template, regardless of the user's login status.
     """
    if "email" in session:
        session.pop("email", None)
        return render_template("login.html")
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
