from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = 'mongodb+srv://dcode:Tat1pet@cluster0.l5w5iei.mongodb.net/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.get_database('Cluster0')

records = db.users
dcQuiz = db.dc_quiz
marvelQuiz = db.marvel_quiz


def existsByEmail(email):
    emailFound = records.find_one({"email": email})

    if emailFound:
        return True

    return False


def registerUser(user):
    records.insert_one(user)
    user = records.find_one({"email": user['email']})

    if user:
        return True

    return False


def getUserByEmail(email):
    return records.find_one({"email": email})


def getUserScores(email):
    return db.scores.find({"email": email})


def fetchQuestions(universe):
    if universe == 'dc':
        return dcQuiz.find()
    else:
        return marvelQuiz.find()


def storeUserScore(email, universe, score):
    user_score = {
        "email": email,
        "universe": universe,
        "score": score,
        "quizDate": datetime.today()
    }
    print(datetime.today())
    db.scores.insert_one(user_score)
    return True


'''
Add questions for marvel here
'''
# def addQuestions():
#     documents = [
#         {
#             '_id': 2,
#             'question': '"Which city does Batman primarily protect in the DC universe?"',
#             'option_a': 'Gotham City',
#             'option_b': 'Metropolis',
#             'option_c': 'Star City',
#             'option_d': 'Central City',
#             'correct_answer': 'Gotham City'
#         },
#         {
#             '_id': 3,
#             'question': 'Which supervillain is featured as the main antagonist in "Suicide Squad" (2016)?',
#             'option_a': 'The Joker',
#             'option_b': 'Lex Luthor',
#             'option_c': 'Darkseid',
#             'option_d': 'Enchantress',
#             'correct_answer': 'Enchantress'
#         },
#         {
#             '_id': 4,
#             'question': 'Who is the arch-nemesis of The Flash?',
#             'option_a': 'Captain Cold',
#             'option_b': 'Reverse Flash',
#             'option_c': 'Grodd',
#             'option_d': 'Deathstroke',
#             'correct_answer': 'Reverse Flash'
#         },
#         {
#             '_id': 5,
#             'question': 'What is the name of the mystical island where Wonder Woman was born and raised?',
#             'option_a': 'Atlantis',
#             'option_b': 'Themyscira',
#             'option_c': 'Krypton',
#             'option_d': 'Lian Li',
#             'correct_answer': 'Themyscira'
#         },
#         {
#             '_id': 6,
#             'question': 'Which actor plays the role of Aquaman in the DC Extended Universe (DCEU)?',
#             'option_a': 'Henry Cavill',
#             'option_b': 'Jason Momoa',
#             'option_c': 'Chris Hemsworth',
#             'option_d': 'Ezra Miller',
#             'correct_answer': 'Jason Momoa'
#         },
#
#         {
#             '_id': 7,
#             'question': 'In the DC TV show "Titans," who leads the team of young superheroes?',
#             'option_a': 'Nightwing',
#             'option_b': ' Red Hood',
#             'option_c': 'Robin',
#             'option_d': 'Cyborg',
#             'correct_answer': 'Nightwing'
#         },
#         {
#             '_id': 8,
#             'question': 'Who is the main villain in the DC movie "Man of Steel" (2013)?',
#             'option_a': 'Lex Luthor',
#             'option_b': 'General Zod',
#             'option_c': 'Doomsday',
#             'option_d': 'Brainiac',
#             'correct_answer': 'General Zod'
#         },
#         {
#             '_id': 9,
#             'question': 'Who is the fastest man alive in the DC universe?',
#             'option_a': 'Kid Flash',
#             'option_b': 'Jay Garrick',
#             'option_c': 'Barry Allen',
#             'option_d': 'Wally West',
#             'correct_answer': 'Barry Allen'
#         },
#
#         {
#             '_id': 10,
#             'question': 'Who is the arch-enemy of the Justice League and often depicted as a highly intelligent alien with advanced technology?',
#             'option_a': 'Sinestro',
#             'option_b': 'Darkseid',
#             'option_c': 'Ra\'s al Ghul',
#             'option_d': 'Steppenwolf',
#             'correct_answer': 'Darkseid'
#         },
#
#         {
#             '_id': 11,
#             'question': 'What is the name of the secret organization that recruits villains to undertake dangerous missions in "Suicide Squad"?',
#             'option_a': 'A.R.G.U.S',
#             'option_b': 'H.I.V.E.',
#             'option_c': 'Justice League',
#             'option_d': 'Star Labs',
#             'correct_answer': 'A.R.G.U.S'
#         },
#
#         {
#             '_id': 12,
#             'question': 'Who is the main antagonist in the DC movie "Justice League" (2017) and "The Snyder Cut" ('
#                         '2021)?',
#             'option_a': 'Steppenwolf',
#             'option_b': 'Ares',
#             'option_c': 'Doomsday',
#             'option_d': 'Darkseid',
#             'correct_answer': 'Steppenwolf'
#         },
#
#         {
#             '_id': 13,
#             'question': 'Who played the role of Harley Quinn in the DC movie "Birds of Prey" (2020)?',
#             'option_a': 'Margot Robbie',
#             'option_b': 'Anne Hathaway',
#             'option_c': 'Emma Stone',
#             'option_d': 'Kate Winslet',
#             'correct_answer': 'Margot Robbie'
#         },
#
#         {
#             '_id': 14,
#             'question': 'In the TV show "The Flash," what is the name of Barry Allen\'s love interest and a reporter?',
#             'option_a': 'Caitlin Snow',
#             'option_b': 'Iris West',
#             'option_c': 'Felicity Smoak',
#             'option_d': 'Lana Lang',
#             'correct_answer': 'Iris West'
#         },
#
#         {
#             '_id': 15,
#             'question': 'Which DC movie centers around the character Arthur Fleck, a failed stand-up comedian who '
#                         'becomes the iconic villain Joker?',
#             'option_a': 'The Dark Knight',
#             'option_b': 'Joker',
#             'option_c': 'Batman Begins',
#             'option_d': 'Suicide Squad',
#             'correct_answer': 'Joker'
#         },
#
#         {
#             '_id': 16,
#             'question': 'Which member of the Justice League can communicate with marine life and breathe underwater?',
#             'option_a': 'Aquaman',
#             'option_b': 'Green Lantern',
#             'option_c': 'Martian Manhunter',
#             'option_d': 'Cyborg',
#             'correct_answer': 'Aquaman'
#         },
#
#         {
#             '_id': 17,
#             'question': 'Which character, also known as Billy Batson, transforms into a superhero by saying the word '
#                         '"Shazam"?',
#             'option_a': 'Green Arrow',
#             'option_b': 'Shazam',
#             'option_c': 'Blue Beetle',
#             'option_d': 'Captain Cold',
#             'correct_answer': 'Shazam'
#         },
#
#         {
#             '_id': 18,
#             'question': 'Who is the iconic arch-nemesis of Batman, known for his eerie white skin and green hair?',
#             'option_a': 'The Penguin',
#             'option_b': 'Two-Face',
#             'option_c': 'The Riddler',
#             'option_d': 'The Joker',
#             'correct_answer': 'The Joker'
#         },
#
#         {
#             '_id': 19,
#             'question': 'In the DC TV series "Arrow," what is Oliver Queen\'s superhero alter ego?',
#             'option_a': 'Speedy',
#             'option_b': 'Arsenal',
#             'option_c': 'Green Arrow',
#             'option_d': 'Red Arrow',
#             'correct_answer': 'Green Arrow'
#         },
#
#         {
#             '_id': 20,
#             'question': 'Which DC movie features a group of supervillains recruited to perform black ops missions for '
#                         'the government?',
#             'option_a': 'Justice League Dark',
#             'option_b': 'Suicide Squad',
#             'option_c': 'Watchmen',
#             'option_d': 'V for Vendetta',
#             'correct_answer': 'Suicide Squad'
#         },
#
#         {
#             '_id': 21,
#             'question': 'Who is the leader of the Justice League?',
#             'option_a': 'Superman',
#             'option_b': 'Batman',
#             'option_c': 'Wonder Woman',
#             'option_d': 'Green Lantern',
#             'correct_answer': 'Batman'
#         },
#
#         {
#             '_id': 22,
#             'question': 'Who is Batman\'s loyal butler, who also provides technological support and guidance?',
#             'option_a': 'Alfred Pennyworth',
#             'option_b': 'Lucius Fox',
#             'option_c': 'Thomas Wayne',
#             'option_d': 'Commissioner Gordon',
#             'correct_answer': 'Alfred Pennyworth'
#         },
#
#         {
#             '_id': 23,
#             'question': 'Which supervillain is known for his incredible intelligence and battles Batman using his '
#                         'mind and technology?',
#             'option_a': 'The Riddler',
#             'option_b': 'Bane',
#             'option_c': 'Ra\'s al Ghul',
#             'option_d': 'Scarecrow',
#             'correct_answer': 'The Riddler'
#         },
#
#         {
#             '_id': 24,
#             'question': 'Who is the Amazonian princess and founding member of the Justice League who wields a magical '
#                         'Lasso of Truth?',
#             'option_a': 'Supergirl',
#             'option_b': 'Black Canary',
#             'option_c': 'Wonder Woman',
#             'option_d': 'Catwoman',
#             'correct_answer': 'Wonder Woman'
#         },
#
#         {
#             '_id': 25,
#             'question': 'Who is the master assassin and leader of the League of Assassins, often portrayed as a foe '
#                         'of Batman?',
#             'option_a': 'Deathstroke',
#             'option_b': 'Ra\'s al Ghul',
#             'option_c': 'Deadshot',
#             'option_d': 'Bane',
#             'correct_answer': 'Ra\'s al Ghul'
#         }
#     ]
#
#     db.dc_quiz.insert_many(documents)
#
#
# addQuestions()
