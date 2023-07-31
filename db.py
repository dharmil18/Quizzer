from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://dcode:Tat1pet@cluster0.l5w5iei.mongodb.net/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.get_database('Cluster0')

records = db.users


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


# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
