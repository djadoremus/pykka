pykka
==============

Pykka (Python + Chikka) is a Chikka SMS API library done in python.

All that's needed for your application is to
* [Signup for a Chikka account](https://api.chikka.com/)
* Set the URL paths in API Settings
 * [ip address]/pykka/receive - this will not work for trial accounts, you need to purchase credits from their shop
 * [ip address]/pykka/outgoing
* Configure the pykka.py with your
 * secret_key
 * client_id
* Run the application!




I'm still trying out python (technically, I'm still a noob at it) as the first iteration of this project is for the AngelHack 2014 hackathon. I've cleaned it up and am trying the Flask-Classy extension, but it seems to have a "1 Class - 1 POST method" limitation; I still have to look into it though.



My goal for this project is to have an easy and simple implementation of the Chikka SMS API, following the necessary guidelines set by Chikka in their [documentation](https://api.chikka.com/docs/overview). I had a bit of trouble at the start because of the scarcity of the resources available at the time. As well as to properly consume/produce data of the POST method in Python. But hey, I'm learning, right? :D



You can contribute to this project as well, just fork a copy and if there are changes that can be added, lets see what we can do about it.
