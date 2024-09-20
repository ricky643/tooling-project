from flask import Flask, request, jsonify
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

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Route to process user JSON data
@app.route("/authenticate", methods=["POST"])
def userJson():

    # gets the body of the request
    #data = request.get_data()

    #print(data)
    
    #fstring example: f"{username}_token"

    #retrieve post data
    #look at the reques , how to retrive value from x--form format

    form_data = request.form
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)


    #api_token = f"{username}_token"
    Eleos_Platform_Key = request.headers.get('Eleos-Platform-Key')
    print("This is the key: ", Eleos_Platform_Key)
    user = users_collection.find_one({"username": username, "password": password})

    #if user has data, python automatically does a boolean evaluation

    #add full name
    #Get array of objects 
    if user and Eleos_Platform_Key:
        #retrieves all needed fields using a jsonify dictionary, provided a default value if field is missing
        return jsonify({
            "username": user.get('username'),
            "api_token": user.get('api_token'),  
            "dashboard_code": user.get('dashboard_code', 'default_dashboard_code'),  
            "menuCode": user.get('menu_code', 'default_menuCode'),  
            "full_name": user.get('full_name', 'default_name'),
            "Eleos-Platform-Key": user.get('Eleos-Platform-Key', 'default_platform_key')
        })
    #otherwise throws an error if either the platform key is incorrect
    elif not Eleos_Platform_Key:
        return jsonify({'result': 'Failure', 'message': 'Invalid platform key'}), 401
    else:
        # Or if user is not found or password is incorrect, return an error
        return jsonify({'result': 'Failure', 'message': 'Invalid username or password'}), 401

#deals with verifying user exists
#defines route user can access when get request is made
@app.route("/authenticate/<api_token>", methods =['GET'])
def authenticate(api_token):
    #expecting a / parameter
    Eleos_Platform_Key = request.headers.get('Eleos-Platform-Key')
    #api_token = request.args.get('api_token')
    

    #checks if token is in mongoDB
    user = users_collection.find_one({"api_token": api_token})

    #if user has data, python automatically does a boolean evaluation
    if user:
        if Eleos_Platform_Key:
            return jsonify({
                #checks username value in dictionary , retrieves value, and stores it in username
                #have to return full name, api token, dashboard, menu code
                
                "username": user['username'],
                "full_name": user['full_name'],
                "dashboard_code": user['dashboard_code'],
                "menuCode": user ['menu_code']
            })
    #else returns 401 error
        else: 
            return jsonify({"error": "Platform Key failed to authenticate"}), 401
    else: jsonify({"error": "No user found"}), 404

@app.route("/loads", methods=['GET'])
def userLoad():
    # Get API token and username from query parameters
    print(request.headers)
    # api_token = request.args.get('api_token')
    # username = request.args.get('username')

    # Authenticate the user using the API token
    # user = users_collection.find_one({"api_token": api_token})

    # Retrieve the token from the headers
    
    initial_token_header = request.headers.get("Authorization")
    Eleos_Platform_Key = request.headers.get('Eleos-Platform-Key')
    print("Platform key: ", Eleos_Platform_Key)
    #splits the string when it detects an '=', creates list of 2 elemements,
    #specify second element
    user_token = initial_token_header.split("=", 1)[1]
    print("user_token: ", user_token)

    

    # Split/pop to get the last value, test with Postman, set up all the headers
    # Eleos says they're going to send to me

    # Check if the token string is found and corresponds to the user

    user_loads = loads_list.find_one({"user_token": user_token})


    if user_loads:
        if Eleos_Platform_Key:
        # Prepare the load data to return
        # Take what data returned in Postman, put into json.loads
        # Log into the app, the load you made there should show up
            load_data = [{
                "id": user_loads.get('id', 'default_id'),   
                "display_identifier": user_loads.get('display_identifier', 'default_display'),
                "sort": user_loads.get('sort', 'default_sort'),
                "order_number": user_loads.get('order_number', 'default_order'),
                "load_status": user_loads.get('load_status', 'default_status'),
                "load_status_label": user_loads.get('load_status_label', 'default_load_status_label'),
                "active": user_loads.get('active', 'default_active'),
                "current": user_loads.get('current', 'default_current')
            }]
            return jsonify(load_data), 200
        else:
        # If no loads are found for the user
            return jsonify({"error": "Invalid Platform Key"}), 401
    # If the user token is not valid or user not found
    else: 
        return jsonify({"error": "No load found for user"}), 404



if __name__ == '__main__':
    # Looks for http traffic on port 8000 via running the flask app
    #PORT = int(os.environ.get('PORT', 8000))
    #app.run(host='0.0.0.0', port=PORT, debug=False)
     app.run(host='0.0.0.0', port=8000, debug=True)
