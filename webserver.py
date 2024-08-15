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

    username = data.get('username')
    password = data.get('password')

    return jsonify({'result': 'Success', 'username': username, 'password': password})


if __name__ == '__main__':
    # Looks for http traffic on port 8000 via running  the flask app
    PORT = 8000 
    app.run(port=PORT, debug=True)