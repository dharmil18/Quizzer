from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://dcode:Tat1pet@cluster0.l5w5iei.mongodb.net/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.get_database('Cluster0')

records = db.users
dcQuiz = db.dc_quiz
marvelQuiz = db.marvel_quiz


def existsByEmail(email):
    """
     Check if a user with the given email address exists in the database.

     This function queries the database to check if a user record with the specified
     email address exists. If a user with the provided email is found in the database,
     it returns True; otherwise, it returns False.

     Args:
         email (str): The email address to check for existence in the database.

     Returns:
         bool: True if a user with the provided email exists in the database, False otherwise.
     """
    emailFound = records.find_one({"email": email})

    if emailFound:
        return True

    return False


def registerUser(user):
    """
    Register a new user by adding their information to the database.

    This function inserts a new user record into the database using the provided 'user'
    dictionary. It then checks if the user has been successfully added to the database
    by querying for a user with the same email address. If a user with the provided email
    is found in the database, it returns True, indicating successful registration; otherwise,
    it returns False.

    Args:
        user (dict): A dictionary containing user information, including first_name, last_name,
                     email, and hashed password.

    Returns:
        bool: True if the user was successfully registered in the database, False otherwise.
    """
    records.insert_one(user)
    user = records.find_one({"email": user['email']})

    if user:
        return True

    return False


def getUserByEmail(email):
    """
    Retrieve a user's information from the database by their email address.

    This function queries the database to retrieve user information for the user
    associated with the provided email address.

    Args:
        email (str): The email address of the user whose information is to be retrieved.

    Returns:
        dict or None: A dictionary containing the user's information (if found) or None
        if no user with the provided email address exists in the database.
    """
    return records.find_one({"email": email})


def getUserScores(email):
    """
    Retrieve a user's quiz scores from the database by their email address.

    This function queries the 'scores' collection in the database to retrieve quiz scores
    associated with the user specified by their email address.

    Args:
        email (str): The email address of the user whose quiz scores are to be retrieved.

    Returns:
        pymongo.cursor.Cursor: A cursor containing quiz scores for the user specified by
        their email address. The cursor can be iterated to access individual score records.
    """
    return db.scores.find({"email": email})


def fetchQuestions(universe):
    """
    Retrieve quiz questions from the database based on the specified universe.

    This function queries the database to retrieve quiz questions based on the specified 'universe.'
    If 'universe' is 'dc,' it fetches questions related to the DC Comics universe; otherwise, it fetches
    questions related to the Marvel Comics universe.

    Args:
        universe (str): The universe for which to retrieve quiz questions ('dc' or 'marvel').

    Returns:
        pymongo.cursor.Cursor: A cursor containing quiz questions for the specified universe.
        The cursor can be iterated to access individual question records.
    """
    if universe == 'dc':
        return dcQuiz.find()
    else:
        return marvelQuiz.find()


def storeUserScore(email, universe, score, quizDateTime):
    """
    Store a user's quiz score in the database.

    This function inserts a user's quiz score information into the 'scores' collection in the database.

    Args:
        email (str): The email address of the user who took the quiz.
        universe (str): The universe for which the quiz score was obtained ('dc' or 'marvel').
        score (int): The user's quiz score.
        quizDateTime (datetime): The date and time when the quiz was taken.

    Returns:
        bool: True if the user's quiz score information was successfully stored in the database,
        False otherwise.
    """
    user_score = {
        "email": email,
        "universe": universe,
        "score": score,
        "quizDateTime": quizDateTime
    }
    db.scores.insert_one(user_score)
    return True
