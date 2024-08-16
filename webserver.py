from flask import Flask, request, jsonify

app = Flask(__name__)

# Route for the homepage
#route(/) decorator applied to the hello() function, meaning that the function will handle requests to the root URL ’/’
@app.route("/", methods=["GET"])
def hello():
    #test text to see that html server is online
    return "Hello Ricardo"

# Route to process user JSON data
@app.route("/processUserJson", methods=["POST"])
def userJson():

    data = request.get_json()
    
    #retrieve post data
    username = data.form.get('username')
    password = data.form.get('password')

    #declare
    #api code    
    #dashboard code
    #menu code
    
    return jsonify({'result': 'Success', 'username': username, 'password': password})

    #user in database in toke
    #or create token when they login each time


if __name__ == '__main__':
    # Looks for http traffic on port 8000 via running  the flask app
    PORT = 8000 
    app.run(host='0.0.0.0', port=PORT, debug=True)