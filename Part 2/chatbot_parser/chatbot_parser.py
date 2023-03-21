# Import the Flask module
from flask import Flask, request, Response, jsonify
import json
import requests

## Create a Flask application object
#app = Flask(__name__)

# @app.route("/message", methods=["POST"])
# def message_parser():
#     input = request.get_json() #get json data 
#     message = input["data"]["message"] # extract message
#     message = message.strip() #delete whitespaces
#     if message[0] == "/": #check if first character is a slash
#         spaces = 0 # initialize to check to see if message has more than one word
#         #iterate through characters until find the first space
#         for i in range(0,len(message)):
#             if message[i] == " ":
#                 is_space = i
#                 spaces += 1 # add one when there's another word
#                 break
#             else:
#                 spaces += 0 # if there's no other words

#         # if there's more than one word
#         if spaces > 0:
#             command = message[1:is_space] #set command to the first word
#             new_message = message[is_space:]#set message to everything following the command

#         # if there's only the command and no message, set message to None
#         else:
#             command = message[1:]
#             new_message = ""

#         # read in json file with key-value store of the command and its server
#         file = open('serverMapping.json')
#         data = json.load(file)
#         file.close()

#         # check if you have a server associated with that command, if yes, 
#         # you create a POST request for the “/execute” endpoint of that server 
#         # and send that API call to it.

#         if command.lower() in data.keys():
#             server_url = data[command.lower()]
#             raw_data = dict()
#             raw_data["data"] = {"command": "shrug", "message": new_message} 
#             r = requests.post(server_url + "/execute", json=raw_data)
#             output = r.json()

#         else:
#             output = jsonify({"data": {"command": command, "message": new_message}}) #output data in json format

#     else:
#         #if there's no slash, there's no command and the message is the entire string
#         output = jsonify({"data": {"command": None, "message": message}})

#     return output


# @app.route("/register", methods=["POST"])
# def register():
#     """
#     allow you to store a Server URL for a particular command

#     when a request is sent to this input, the chatbot parser “registers” that 
#     command and forwards all subsequent requests from the chatbot terminal 
#     who has that command to the server specified

#     """
#     input = request.get_json() #get json data
#     command = input["data"]["command"] # extract command
#     command = command.strip() #delete whitespaces
#     server_url = input["data"]["server_url"] # extract server url
#     server_url = server_url.strip() #delete whitespaces
#     output = jsonify({"data": {"command": command, "message": "saved"}})

#     return output


# # Run the application
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5050)


# Initiating Flask App
app = Flask(__name__)

# Function to read data from file
def getDataFromFile():
    file = open('serverMapping.json')
    data = json.load(file)
    file.close()
    return data

# Write new JSON to file
def writeToFile(quotesData):
    with open("serverMapping.json", "w") as f:
        json.dump(quotesData, f)
        f.close()

# Function that checks if a dedicated server for a command exists
# If it does, handles the nested post call to /execute endpoint
# Else, returns normal message from Assignment 1
def handleByCommand(message, command):
    serverList = getDataFromFile()
    if command not in serverList:
        return createReturnMessage(message, command)
    if serverList[command][-1] != "/":
        urlPath = serverList[command] + "/execute"
    else:
        urlPath = serverList[command] + "execute"
    jsonBody = {"data": {"command": command, "message": message}}
    return requests.post(urlPath, json=jsonBody).json()
    # Function that returns a JSON for command and messaage nested within the "data" key according to the prompt

# Function that handles the creation of the output JSON in the desired format
def createReturnMessage(message, command=None):
    return jsonify({"data": {"command": command, "message": message}})

# Handler for /message endpoint
@app.route("/message", methods=["POST"])
def handleChatbotMessage():
    try:
        # Get message from the incoming JSON which is nested into the "data" key
        chatbotInput = request.get_json()['data']['message']
        # Removing unwanted spaces from the starting and ending of the "message" string
        chatbotInput = chatbotInput.strip(" ")
        # Returning an error if the string was empty
        if len(chatbotInput) == 0 or chatbotInput is None:
            return createReturnMessage("Error: Empty input"), 400
        # Returning the message back if the message didn't have the "/" at the start
        if chatbotInput[0] != "/":
            return createReturnMessage(chatbotInput), 200
        # Splitting /command and message from "/command message"
        messageParts = chatbotInput.split(" ", 1)
        # Getting command from "/command" and assigning message part to a new variable for easier reference
        command, message = messageParts[0][1:], messageParts[1]
        # Handling the case if command or message are emoty or invalid
        if len(command) == 0 or len(message) == 0 or command is None or message is None:
            return createReturnMessage("Error: Invalid input"), 400
        # Returning the final result
        return handleByCommand(message, command)
    except:
        return createReturnMessage("Error: Invalid input"), 400

# Handler for /register endpoint
@app.route("/register", methods=["POST"])
def handleRegisterCall():
    try:
        # Getting the command and the server url from JSON body
        serverCommand, serverURL = request.get_json()['data']['command'], request.get_json()['data'][
            'server_url']
        # Removing any redundant whitespace
        serverURL = serverURL.strip(" ")
        # Checking if command or url are invalid or not
        if serverCommand is None or serverCommand == "" or serverURL is None or serverURL == "":
            return createReturnMessage("Error: Invalid Input"), 400
        # Getting current list of server and url mapping from file
        currentServers = getDataFromFile()
        # Adding/Updating URL for the command
        currentServers[serverCommand] = serverURL
        # Writing to file
        writeToFile(currentServers)
        # Returning the expected "saved" message
        return createReturnMessage("saved", serverCommand)
    except:
        return createReturnMessage("Error: Something went wrong"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)