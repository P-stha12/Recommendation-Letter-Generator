# reco_letter

# How to run?
================================================================================================================== 
* Install the packages from package.json file 
=> npm install

* Create a python virtual environment
=> python -m venv venv

* Activate virtual environment
Firstly, go to the project directory.
Then run,
# In windows 
=> ./venv/Scripts/Activate.ps1
# In *Unix
=> source venv/bin/activate

* Install all the requirements
=> python -m pip install -r ./requirements.txt

* Perform migration
=> python manage.py migrate

* Create a superuser
=> python manage.py createsuperuser

* Activate the server
=> python manage.py runserver

* Open web browser and you know what to do, right?
# For admin
	1. Open admin panel
	2. Create Programs: Example BE
	3. Create Departments: Example BCT
	4. Create Teacher info
# Remember: You need to create a superuser for the teacher with his/her full name consisting of his/her unique id (available in the teacher's info) after a slash '/'. This is how the code works.

# For student
	1. Register
	2. Login
	3. Request for the recommendation letter
	
# For teacher 
	1. Ask the admin to create your profile
	2. Login
	3. View requests (You can also view the list of students that you have recommended.)
	4. Generate the recommendation letter 
	
==================================================================================================================

# We have used the app password for SMTP in the settings.py file. We may delete it due to security reasons. In case you get a SMTP error, you need to enable app password for a valid gmail account and use that password for SMTP in settings.py file.  

# Enjoy & have a good day.
