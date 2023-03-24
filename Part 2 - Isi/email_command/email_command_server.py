from flask import Flask, request, jsonify
import json
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from worker import sendEmailTask

app = Flask(__name__)

@app.route('/execute', methods = ['POST'])
def send_email():
    input = request.get_json()
    command = input["data"]["command"]
    message = input["data"]["message"]
    spaces = []
    for i in range(0,len(message)):
        if message[i] == " ":
            is_space = i
            spaces.append(is_space)
    to_email = message[0:spaces[0]]
    from_email = "grace_roseman@berkeley.edu"
    subject = message[spaces[0]:spaces[1]]
    body = message[spaces[1]:]

    if not to_email or not subject or not body:
        output = jsonify({"data": {"command": command, "message": "Please fill out all fields to send an email"}})
        response_code = 400           
    else:
        # message = Mail(
        #     from_email=from_email,
        #     to_emails=to_email,
        #     subject=subject,
        #     html_content=body)
        # try:
        #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #     sg.send(message)
        #     response = {"message": "Email was sent"}
        #     output = jsonify({"data": {"command": command, "message": "Email was sent"}})
        #     response_code = 200
        # except Exception as e:
        #     logging.error(e)

        #taskIDs = []
        #emailAsyncTask = sendEmailTask.delay(to_email, body, subject)
        #taskIDs.append(emailAsyncTask.id)

        sendEmailTask.delay(to_email, body, subject)
        output = jsonify({"data": {"command": command, "message": "Email was queued"}})
        response_code = 200
    
    #return {"tasks": taskIDs}
    return output, response_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5052, debug=True) # Running the shrug server on 5052
        