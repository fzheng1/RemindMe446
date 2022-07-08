# RemindMe446
a little backend for our android app

Steps to startup:

1. clone repo
2. install python
3. [OPTIONAL] make a virtualenv
4. pip install all the dependencies in the `requirements.txt` file into your environment <p>**!! NOTE FRANKLIN JUST COPIED HIS ENTIRE ENVIRONMENT AS REQUIREMENTS SO YOU PROBABLY DON'T NEED SOME PACKAGES BUT JUST TO BE SAFE INSTALL EVERYTHING XD !!**</p>
5. DATABASE SETUP
   1. navigate into the `app` directory
   2. open a python console ($ python OR $ python3)
   3. `>>> from project import *`
   4. `>>> db.create_all(app=create_app())`
   5. exit the console, there should be a `db.sqlite` file in your `app` folder
6. run `flask run` from the repo's root folder `RemindMe446`. You should see something like "http://127.0.0.1:5000", you should now be able to interact with the app on localhost "http://localhost:5000"
7. Franklin has a postman collection for the endpoints to test with he is sometimes willing to share (in messenger group chat)
8. to setup the postman collection just make an environment and set base_url to the hostname you got in step 6
9. idk go nuts I hope we can finish