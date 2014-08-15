#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import requests
import email
import os
import sys
import json

import ast
import urllib

client_id="62eb59d295fa6e9dd81c636944c457956e8586147d732502767a374275ed9785"
secret_key="e6886536ec7563e0032c7fb81835b356151190fbb6498e2ff9c8cc0811cdcf7c"
shortcode="292902673"
reply_message=urllib.urlencode({"message":"Message Received"})

app = Flask(__name__)
app.debug = True

@app.route("/pykka/send/<mobile_number>-<message>")
def sendSMS(mobile_number, message):
	print("---sendSMS")
	message_id=os.urandom(16).encode("hex")
	payloadDict = {
		"message_type":"SEND",
		"mobile_number":mobile_number,
		"shortcode":shortcode,
		"message_id":message_id,
		"message":message,
		"client_id":client_id,
		"secret_key":secret_key
	}
	#payload = "message_type=SEND&mobile_number="+mobile_number+"&shortcode="+shortcode+"&message_id="+message_id+"&message="+message+"&client_id="+client_id+"&secret_key="+secret_key
	payload = urllib.urlencode(payloadDict)
	r = requests.post("https://post.chikka.com/smsapi/request", data=payload)
	print("---calling post chikka " + r.url)

	try:
		result = r.json()
		#print("---result " , result)
		return json.dumps(result)
	except:
		#print("---error" , sys.exc_info())
		return sys.exc_info()
	#return "hoping this is successful"

#@app.route("/receive/incoming", methods=["POST"])
@app.route("/pykka/receive", methods=["POST"])
def receiveSMS():
	print("---receiveSMS")
	#message_type = request.args.get("message_type")
	#mobile_number = request.args.get("mobile_number")
	#shortcode = request.args.get("shortcode")
	#request_id = request.args.get("request_id")
	#message = request.args.get("message")
	#timestamp = request.args.get("timestamp")

	try:
		print("---request.data " + request.data)
		form = request.form
		formJSON = ast.literal_eval(json.dumps(form))
		print("---request.form ", formJSON)

		message_id=os.urandom(16).encode("hex")
		payloadDict = {
			"message_type":"REPLY",
			"mobile_number":formJSON['mobile_number'],
			"shortcode":formJSON['shortcode'],
			"message_id":os.urandom(16).encode('hex'),
			"message":"Message Received",
			"request_id":formJSON['request_id'],
			"request_cost":"FREE",
			"client_id":client_id,
			"secret_key":secret_key
		}
		payload = urllib.urlencode(payloadDict)
		#payload = "message_type=REPLY&mobile_number="+formJSON['mobile_number']+"&shortcode="+formJSON['shortcode']+"&message_id="+os.urandom(16).encode('hex')+"&"+reply_message+"&request_id="+formJSON['request_id']+"&request_cost=FREE&client_id="+client_id+"&secret_key="+secret_key
		r = requests.post("https://post.chikka.com/smsapi/request", data=payload)
		print("---calling post chikka " + r.url)

		try:
			result = r.json()
			print("---result ", result)
		except:
			print("---inner error ", sys.exc_info())
	except:
		print("---error", sys.exc_info())
	
	#add sqlalchemy here
	#received = SMS(id=request_id, timestamp=timestamp)
	#Session.add(received)
	return "Accepted"

@app.route("/pykka/outgoing", methods=["POST"])
def notify():
	message_type = request.args.get("message_type")
	shortcode = request.args.get("shortcode")
	message_id = request.args.get("message_id")
	status = request.args.get("status")
	credits_cost = request.args.get("credits_cost")
	timestamp = request.args.get("timestamp")

	#add/retrieve from sqlalchemy here
	#notification = SMS(id=message_id, credit_cost=credits_cost, timestamp=timestamp)
	#Session.add(notification)

	return "Accepted"	


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)
