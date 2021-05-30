#pip dependencies are "pip install flask" and "pip install flask-restful"

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
import pymongo
from dotenv import load_dotenv
from textblob import TextBlob
import os
import time


def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
  return  TextBlob(text).sentiment.polarity

# Create two new columns 'Subjectivity' & 'Polarity

def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'


load_dotenv()
#Standard minimal Restful Api initialization of Flask library
#https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
application= app = Flask(__name__)
api = Api(app)

#DATABASE_URL=f'mongodb+srv://NodeJs:{os.environ.get("password")}@sentiment.6g24c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' # get connection url from environment
DATABASE_URL=f'mongodb+srv://NodeJs:NodeJs@sentiment.6g24c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' # get connection url from environment
        
client=pymongo.MongoClient(DATABASE_URL) # establish connection with database
mongo_db=client.myFirstDatabase
collection=mongo_db.sentiment

          

#Flask argument parser for taking json input. 
users_put_args = reqparse.RequestParser()

# Parsed name and surnamed is required for the insertion.
users_put_args.add_argument("name",type=str,help="Name of the user",required=True)
users_put_args.add_argument("surname",type=str,help="SURName of the user",required=True)
users_put_args.add_argument("email",type=str,help="Email of the user")

# User dictionary. Stores index:key pairs for userid and sub-info.

#The main building block provided by Flask-RESTful are resources.
# Resources are built on top of Flask pluggable views, 
# giving you easy access to multiple HTTP methods just by defining methods on your resource.
class PositivityAccount(Resource):

    # GET METHOD, uses http id for looking at the userid.
    # READ's Users dict for get method.
    def get(self,accName):
        print(accName)
        # Looks for id in the Users dict, if not found abort the program.
        res = collection.find_one({"acc":accName},{"tweets"})
        if not res: 
            #abort(404,message=" Account  not found. ERROR 404")
            # procces _id 
            os.system("node Retweet.js "+accName)
            while(not res):
                # for not to send request to mongoDb constantly
                time.sleep(1)
                res = collection.find_one({"acc":accName},{"tweets"})
      
        # if there aint no such an url eror
        #if id not in Users:
        #    abort(404,message=" User not found. ERROR 404")
        
        #return is a Python dictionary which is same as JSON.
        
        return  (res["tweets"])
"""
    # POST METHOD, uses http id for looking at the userid.
    # CREATE's Users in the dict with userid.
    def post(self,id):
        # Looks if user exists, aborts if found.
        if id  in Users:
            abort(409,message="User already exists. ERROR 409")
        else:
            args=users_put_args.parse_args()
            Users[id]=args

            #return is a Python dictionary which is same as JSON.
            return Users[id]

    #DELETE METHOD, uses http id for looking at the userid.
    #DELETE'S Users from dict according to their id.
    def delete(self,id):

        # Looks for id in the Users dict, if not found abort the program.
        if id not in Users:
            abort(404,message="User not found, delete request cancelled. ERROR 404")
        else:

            # Deletes user.
            del Users[id]

            # Only signal code is needed for confirmation since indexed dictionary is deleted.
            return "",200
    #PUT METHOD, uses http id for looking at the userid.
    #REPLACE'S  current user with diffrent user preserving the userid.
    def put(self,id):
        # Looks for id in the Users dict, if not found abort the program.
        if id not in Users:
            abort(404,message="User not found, update request cancelled. ERROR 404")
        else:
            #Deletes current user, then creates new user with parsed info.
            del Users[id]
            args=users_put_args.parse_args()
            Users[id]=args

            #return is a Python dictionary which is same as JSON.
            return Users[id]

    def patch(self,id):

        ##PATCH METHOD, uses http id for looking at the userid.
        #UPDATE'S  current user information with requested.
        if id not in Users:
            abort(404,message="User not found, update request cancelled. ERROR 404")
        else:
            args=users_put_args.parse_args()
            Users[id]=args
            return Users[id]

"""
#Routed into resource
api.add_resource(PositivityAccount , "/PositivityAccount/<accName>")

@app.route('/')
def home():
    return jsonify("Welcome")
    
    
    
    
if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host = 'docker-tw.herokuapp.com', port = port)
    
    
    

