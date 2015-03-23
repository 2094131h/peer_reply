# Peer Reply
Group project for WAD2
Created by Mike, Craig, Lovisa, Gulen & Monika

#Description
A question and answer resource to aid students in their studies.

#Install Instructions
In a terminal or command prompt, create a new virtual enviroment to install Peer Reply in.

Navigate to a directory where you want to install Peer Reply.  Then issue the git clone command using the applications repository url. eg.

>>git clone https://github.com/2094131h/peer_reply.git

This will copy the repository into the directory on your machine.  Navigate to the peer_reply/peer_reply_project directory and issue the command

>>pip install -r requirements.txt

to install the required applications needed to run Peer Reply.

Once completed, issue the command

>>python manage.py syncdb

to build the applications database.  When it prompts you to create a superuser, select yes and enter your details.

To populate the database with the sample data we have provided, issue the command

>>python populate_peer_reply.py

This may take a few minutes to complete.  Once the script completes you can start the application by typing

>>python manage.py runserver

Then, in your web browser, navigate to http://127.0.0.1:8000/peer_reply/ where you will be presented with the Peer Reply home page.  Congratulations!  You just installed Peer Reply!

#Users
Six users are currently registered with the application.  You can use these accounts to test functionality.  The login details for each are as follows:

Username/Password

test/test

haroldabbott/password

peterrabbit/password

jennyfielding/password

fredricogalleoni/password

kleopatraramsey/password



