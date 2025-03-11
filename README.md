# Project Documentation:

# [eCommerce] Project

# Django Project

This is a modular news application built with Python.

This application, built with Django, showcases CRUD capabilities,
a responsive design through Bootstrap, and a modular project structure,
and it employs unit testing following the AAA pattern. Every template incorporates
semantic HTML elements (header, section, article, footer) along with Bootstrap
classes to achieve a responsive and polished design.

Organised project structure extends to the eCommerce news application with a secure
RESTful API and also integrates Twitter’s API to tweet when news articles posted and published.

This Django-based News Web Application allows readers to view articles and
newsletters published by independent journalists and publishers.
It includes role-based authentication, article approval workflows
(with email and X (formerly Twitter) notifications), and a
RESTful API for third-party access.

Reader01:
username: JohnDoe
email: DoeJohn@email.com
password: P@55w0Rd4528_DJ

Reader02:
username: JaneDoe
email: DoeJane@email.com
password: P@55w0Rd4528_MrsDJ

Reader03:
username: PlainJane
email: JanePlain@email.com
password: P@55w0Rd4528_MrsPJ



Journalist01:
username: JohnApple
email: AppleJohn@email.com
password: P@66w0Rd4528_DJ

Journalist02:
username: JohnBanana
email: BananaJohn@email.com
password: P@66w0Rd4528_BJ

Journalist03:
username: PeterSmith
email: SmithPeter@email.com
password: P@66w0Rd8628_PS

Journalist04:
username: JohnSmith
email: SmithJohn@email.com
password: P@36w0Rd8918_JS

Editor01:
username: BigMac
email: MacBigMeal@email.com
password: P@66w0Rd4528_BMM


________________________________________________________________________________
## Project Structure:
django_project_news/	       # Project folder dir 
│
├── myVenv
│
└── news_project/             # This is the (UPPER / OUTER) project directory—i.e. Project ROOT folder / dir.
    │
    ├── manage.py                      # Django management script allowing us to interact with the project.
    ├── README.md					   # Django project description.
    ├── .flake8
    ├── .pyproject.toml
    ├── requirements.txt			  # Project dependencies
    ├── .gitignore
    ├── db.sqlite3					  # (For development. → Will switch to MariaDB)
    │
    ├── news_project/          # Main (CORE / INNER) project folder (Contains project settings)
    │   ├── __init__.py
    │   ├── settings.py                # Global configuration (includes installed apps, static files, etc.)
    │   ├── urls.py                    # Main URL dispatcher. Defines the main URL routes
    │   ├── wsgi.py
    │   └── asgi.py
    │
    │						
    │				==== # Folders for Django apps START here # ====
    │
    ├── newsApp/   					  # Our news website application called 'newsApp'                          
    │   ├── migrations/
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── admin.py                # Model registrations for Django admin
    │   ├── apps.py                 # App configuration
    │   ├── models.py               # Core data Models: CustomUser, Publisher, Article, and Newsletter etc.
    │   ├── forms.py                # Forms for user registration, article submission, etc.
    │   ├── views.py                # Views (Contains view functions for user registration, login, logout, dashboard, article creation, etc.)
    │   ├── urls.py                 # App-specific URL patterns for web views.
    │   ├── tests.py                # Unit tests for models and views following AAA pattern.
    │   ├── static/
    │   │   └── newsApp/
    │   │       ├── css/
    │   │       │   └── styles.css  # Custom CSS (with Bootstrap added via CDN in templates)
    │   │       └── js/
    │   │           └── scripts.js   # (Optional) Custom JavaScript
    │   │
    │   ├── serializers.py			  # Creating Serializers. Model sterilisation. Creates serializers to convert Django model instances to JSON for API interaction.
    │   │
    │   ├── signals.py			     # Sends automated emails to subscr. and is responsible for posting articles to X upon approval.
    │   │
    │   ├── api_views.py			  # Building API Views. Creates API endpoints for 
    │   │  								data retrieval. Defines RESTful API views.
    │   │
    │   ├── api_urls.py			  # Setting Up API URLs. Endpoint registration. API endpoint mapping.
    │   │
    │   │
    │   ├── functions/
    │   │   └── tweet.py    	       # Integrating Twitter API—tweets are sent using this class.
    │   │   └── __init__.py
    │   │
    │   │
    │   └── templates/
    │       └── newsApp/
    │           ├── base.html         			# Base template with Bootstrap & semantic HTML
    │           ├── register.html     			# User registration form
    │           ├── login.html        			# User Login form
    │           ├── dashboard.html  	        # Dashboard showing options based on user role.
    │           ├── article_form.html        	# Create/edit; Form for journalists to create a new article.
    │           ├── article_approval.html    	# Lists pending articles for editors approval.
    │           ├── article_list.html        	# Lists all approved articles for public viewing.
    │           ├── article_detail.html		# Displays details of a completed article.
    │           ├── subscriptions.html			# Displays readers subscriptions page.
    │           └── journalist_articles.html	# Displays readers journalists' subscriptions page.
    │						
    │				==== # Folders for Django apps END here # ====
    │
    │
    │
    ├── templates/                        # Global templates folder
    │   ├── base.html                     # Base HTML template
    │   └── ...
    │
    └── static/                           # (Optional) Global static files (e.g., CSS, JavaScript, images)
        ├── css/
        ├── js/
        └── images/


________________________________________________________________________________
For .flake8:
[flake8]
max-line-length = 79
exclude = .git,**pycache**,tests,venv
ignore = E203, E266, E501, W503

For .pyproject.toml:
[tool.black]
line-length = 79

________________________________________________________________________________
## Setup Instructions:
1. Create 'django_projects' folder in file explorer.
	"C:\...\django_project_news" => project folder dir
2. Create a virtual environment - while in project folder dir
	Type: 'python -m venv myVenv' into vs code terminal
2.1. Activate virtual environment
	Type: 'source myVenv/Scripts/activate' into vs code terminal, then
	Type: 'pip freeze' into the vs code term.
3. Install django - still while in project folder dir
	Type: 'pip install django' into the vs code terminal, then
	Type: 'pip freeze' into the vs code term.
4. Create a new django project and application
4.1. Create a new django project:
	Type: 'django-admin startproject news_project' into vs code term, while still in proj. folder dir
4.2. Change directory to proj ROOT dir
	Type: 'cd news_project' into vs code term
4.3. Create a new Django application:
	Type: 'django-admin startapp newsApp' into vs code term
	Type: 'ls' into vs code term
5. Run initial database migrations to set up the database tables:
	Type: 'python manage.py migrate' into the vs code term
6. Create a superuser to access the Django admin interface:
	Type: 'python manage.py createsuperuser' into the vs code term, then,
	Fill in: username, email (rrrr@rrrr.com), password (1234 --this is a fictitious password)
7. Start the Django development server:
	Type: 'python manage.py runserver' into the vs code term, then follow the http://... link in term
8. Create the necessary subfolders and modules where needed within the proj folder dir or proj root dir
9. Edit and populate the different modules and subfolders
10. Install flake8:
	Type: 'pip install flake8' into the vs code term and create and populate the .flake8 file.
11. Install Black:
	Type: 'pip install black' into the vs code term
12. Perform black and flake8 PEP 8 standards. >>> Don't use prettier on HTML, CSS, JavaScript. It causes app errors
13. Install MySQL on your local machine, define host, port, username, and password accordingly.
Then, connect to your MySQL server.
14. Run Migrations:
	Open your terminal and execute the following commands in your project’s ROOT directory:
	Type: 'python manage.py makemigrations'
	      'python manage.py migrate' into the vs code term
15. Restart Your Development Server:
	Type: 'python manage.py runserver' into the vs code term, then follow the http://... link in term
16. Use your application and check if it works.
17. Generate requirements.exe file:
	Type: 'pip freeze > requirements.txt' into vs code term, while in proj root dir.
18. Generate README.md file.
NOTE: Perform migrations to ensure that any new changes are reflected in the database, and restart the development server to test your application.
19. Install djangorestframework:
	Type: 'pip install djangorestframework' into the vs code term, while still in the proj root dir.
20. Install requests:
	Type: 'pip install requests' into the vs code term, while still in the proj root dir.
21. Install mysqlclient:
	Type: 'pip install mysqlclient' into the vs code term, while still in the proj root dir.
22. Run Migrations:
	Open your terminal and execute the following commands in your project’s ROOT directory:
	Type: 'python manage.py makemigrations'
	      'python manage.py migrate' into the vs code term
23. Perform application functionality tests:
1. Manual (Functional) Testing
1.1. Basic Project Setup
1.1.1. Activate your virtual environment and install dependencies:
pip install -r requirements.txt
1.1.2. Apply migrations and create a superuser:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
1.1.3. Run the server:
python manage.py runserver
1.1.4. Access the application in your browser at http://127.0.0.1:8000/.

1.2. Testing the Admin Site
Go to http://127.0.0.1:8000/admin/ → Log in using your superuser credentials → Create or view data (e.g., Publishers, Articles, CustomUser, etc.) → Verify that you can add/edit/delete records via the admin interface.
1.3. Testing Registration & Login
1.4. Testing Role-Based Access
1.5. Testing via Postman

24. Install Postman:
25. Test GET Endpoints: test the endpoint that lists all stores, set the method to GET within Postman.
	Use the URL: 'http://127.0.0.1:8000/api/articles/' and click send.
	use basic auth → a readers credenials then a journalist credentials
 
25.1. Inspect the JSON response in Postman → you should receive 200 OK message.
26. Test POST Endpoints:
26.1. Set the method to POST → use the URL: 'http://127.0.0.1:8000/api/articles/', then
26.2. In the Authorization tab, choose Basic Auth and enter one of your journalists username and password.
26.3. In the Body tab, select raw and choose JSON as the type.
	Type: 
		'{
  "title": "My New Article",
  "content": "This is the body of my article.",
  "status": "pending"
}' into the field → then click send

26.4. If successful, you should receive a JSON response with the new store’s data and an HTTP status code of 201.
27. Run tests once again. i.e. 
	Type: 'python manage.py test' and 'python manage.py test --verbosity 2' into the vs code term.

________________________________________________________________________________
Frequently used commands:

django-admin startproject news_project


django-admin startapp newsApp

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

python manage.py makemigrations
python manage.py migrate


http://127.0.0.1:8000/admin/
________________________________________________________________________________














