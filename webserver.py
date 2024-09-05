from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from bson.objectid import ObjectId 

app = Flask(__name__)


uri = "mongodb+srv://ricardovarona:Floppa63@tooling.uxyx6.mongodb.net/"

client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged deployment successfully")
except Exception as fail:
    print(fail)


db = client['tooling']
users_collection = db['project']
loads_list = db["loads"]





# Route for the homepage
#route(/) decorator applied to the hello() function, meaning that the function will handle requests to the root URL ’/’
@app.route("/", methods=["GET"])
def hello():
    #test text to see that html server is online
    return "Hello, World"

# Route to process user JSON data
@app.route("/processUserJson", methods=["POST"])
def userJson():

    data = request.get_json()
    
    #retrieve post data
    username = data.get('username')
    password = data.get('password')

    #just have the api token be the username+ incremented number
    api_token = data.get('ddb56eb8-1b39-11e5-9c63-f9bd05003d3f')
    #dashboardCode = 
    #menuCode

    #dictionary used to store needed user information within the db
    user_data = {
        "username": username,
        "password": password,
        "api_token": api_token

    }

    #inserts a document into mongoDB collection
    users_collection.insert_one(user_data)

    #declare
    #api code    
    #dashboard code
    #menu code
    
    return jsonify({'result': 'Success', 'username': username, 'password': password, 'api_token': api_token})



#deals with verifying user exists
#defines route user can access when get request is made
@app.route("/authenticate", methods =['GET'])
def authenticate():

    api_token = request.args.get('api_token')

    #checks if token is in mongoDB
    user = users_collection.find_one({"api_token": api_token})

    #if user has data, python automatically does a boolean evaluation
    if user:
        #will then return 
        return jsonify({
            #checks username value in dictionary , retrieves value, and stores it in username
            "username": user['username']
        })
    #else returns 401 error
    else: 
        return jsonify({"error": "failed"}), 401
    
@app.route("/loads", methods=['GET'])
def userLoad(): 
    api_token = request.args.get('api_token')

    #Authenticate the user using the API token
    user = users_collection.find_one({"api_token": api_token})

    if user:
        #Gets the user's ID from the project collection
        user_id = user['_id']

        #Finds the user's loads in the loads collection using the user_id
        user_loads = loads_list.find_one({"user_id": ObjectId(user_id)})

        if user_loads:
            #load data to return
            load_data = {
                "id": user_loads.get('id', 'default_id'),   
                "display_identifier": user_loads.get('display_identifier', 'default_display'),
                "sort": user_loads.get('sort', 'default_sort'),
                "order_number": user_loads.get('order_number', 'default_order'),
                "load_status": user_loads.get('load_status', 'default_status'),
                "load_status_label": user_loads.get('load_status_label', 'default_load_status_label'),
                "active": user_loads.get('active', 'default_active'),
                "current": user_loads.get('current', 'default_current')
            }
            return jsonify(load_data)
        else:
            return jsonify({"error": "No loads found for the user"}), 404
    else:
        return jsonify({"error": "User not found"}), 401
    

if __name__ == '__main__':
    # Looks for http traffic on port 8000 via running the flask app
    PORT = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
