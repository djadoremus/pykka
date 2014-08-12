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

import MySQLdb
from sqlalchemy import *
from sqlalchemy.engine.reflection import Inspector

from sqlalchemy.orm import *

engine = create_engine("mysql://root:root@localhost")
engine.execute("CREATE DATABASE IF NOT EXISTS cgurado")
engine.execute("USE cgurado")

metadata = MetaData(engine)

vericode_status = Table("vericode_status", metadata,
	Column('vericode', String(40), primary_key=True),
	Column('mobile_number', String(40)),
	Column('status', String(40))
)
inspector = Inspector.from_engine(engine)
#print(inspector.get_table_names()[0])
#for table_name in inspector.get_table_names():
#	print table_name + "\n"
vericode_status.create(checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

client_id="62eb59d295fa6e9dd81c636944c457956e8586147d732502767a374275ed9785"
secret_key="e6886536ec7563e0032c7fb81835b356151190fbb6498e2ff9c8cc0811cdcf7c"
shortcode="292902673"
reply_message=urllib.urlencode({"message":"Message Received"})

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	print("msgid " + os.urandom(16).encode("hex")) 

	return "Hello World!"

@app.route("/foo/<bar>-<fam>")
def lorem(bar, fam):
	return "Lorem Ipsum Dolor SIt Amet" + bar + fam

@app.route("/send/<mobile_number>-<message>")
def sendSMS(mobile_number, message):
	print("---sendSMS")
	#payload = {"message_type":"SEND", "mobile_number":"639175634463", "shortcode":"29290515151", "message_id":os.urandom(16).encode("hex"), "message":"lolwut", "client_id":"c644a80c64da54f56e29c2a3d7c4ed1d0a4a82ae9b3c4aead28d127d69334231", "secret_key":"c5695b7c3425e0fe43584f0208766674d89546f4b8239711e1e6181f99b0970d"}
	#headers = {"Content-type":"application/json"}
	#r = requests.post("https://post.chikka.com/smsapi/request", data=json.dumps(payload), headers=headers)
	message_id=os.urandom(16).encode("hex")
	payload = "message_type=SEND&mobile_number="+mobile_number+"&shortcode="+shortcode+"&message_id="+message_id+"&message="+message+"&client_id="+client_id+"&secret_key="+secret_key
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

@app.route("/reply")
def replySMS():
	print("---replySMS")
	payload = {"message_type":"REPLY", "mobile_number":"639175634463", "shortcode":shortcode, "request_id":"[something from sqlalchemy]", "message_id":os.urandom(16).encode("hex"), "message":"ahahahaha", "request_cost":"FREE", "client_id":client_id, "secret_key":secret_key}
	#headers = {"Content-type":"application/json"}
	#r = requests.post("https://post.chikka.com/smsapi/request", data=json.dumps(payload), headers=headers)
	r = requests.post("https://post.chikka.com/smsapi/request", params=payload)
	print("---calling post chikka " + r.url)

	try:
		result = r.json()
		#print("---result " , result)
		return json.dumps(result)
	except:
		#print("---error" , sys.exc_info())
		return sys.exc_info()
	#return "hoping this is successful"


@app.route("/test/json")
def testJSON():
	json_str="{'request_id': '5048303030534D415254303030303032393230303033303030303030303134303030303036333932393737333233353030303030313430373237303035313435', 'timestamp': '1406393505.88', 'message': 'lolwut', 'mobile_number': '639297732350', 'shortcode': '292902673', 'message_type': 'incoming'}"

	formJSON = ast.literal_eval(json_str)
	print("---formJSON ", formJSON['message'])
	return "hahahahahahahah"

#@app.route("/receive/incoming", methods=["POST"])
@app.route("/sms/receive", methods=["POST"])
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
		#vericode_entry = session.query(vericode_status).filter_by(vericode=formJSON['message']).first()
		#if vericode_entry!=None:
		#print("---vericode_entry " , vericode_entry)
		session.execute("update vericode_status set mobile_number='"+formJSON['mobile_number']+"', status='SENT' where vericode='"+formJSON['message']+"'")
		session.commit()
		message_id=os.urandom(16).encode("hex")
		payload = "message_type=REPLY&mobile_number="+formJSON['mobile_number']+"&shortcode="+formJSON['shortcode']+"&message_id="+os.urandom(16).encode('hex')+"&"+reply_message+"&request_id="+formJSON['request_id']+"&request_cost=FREE&client_id="+client_id+"&secret_key="+secret_key
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

@app.route("/db/testselect")
def testDB():
	try:
		print("---request.data " + request.data)
		#vericode_add = vericode_status(vericode="lolwut")
		#session.add(vericode_add)
		#session.commit()
		vericode_entry = session.query(vericode_status).filter_by(vericode="lolwut").first()
		if vericode_entry!=None:
			print("---vericode_entry " , vericode_entry)
			session.execute("update vericode_status set mobile_number='"+"hahahaha"+"', status='lipsum' where vericode='lolwut'")
			session.commit()
	except:
		print("---error", sys.exc_info())
	return "yoyo"	


@app.route("/notify/outgoing", methods=["POST"])
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
