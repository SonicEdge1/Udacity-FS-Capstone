# Casting Agency

[Introduction](#Introduction) |
[Technologies & Dependencies](#Technologies-&-Dependencies) |
[Folders & File Descriptions](#Folders-&-File-Descriptions) | 
[Project Setup](#Project-Setup) |
[Running Tests](#Running-Tests) |
[User Roles and Permissions](#User-Roles-and-Permissions) |
[Front end pages and endpoints](#Front-end-pages-and-endpoints) |
[API Endpoints](#API-Endpoints) |
[Error Handling](#Error-Handling) |
[Deployment to Heroku](#Deployment-to-Heroku)  
___
Capstone Project for the Udacity Full-Stack course  
Heroku  Deployment Address: https://casting-agent-app.herokuapp.com/
___
## Reviewer Credentials   

For security concerns, Log-in Credentials have been removed post project eval.  
All users have been removed from authentication app.  
Database Credentials have been rotated.  
https://devcenter.heroku.com/articles/heroku-postgresql-credentials#pg-credentials-rotate  
*Note that for future projects, it would be best to submit credentials in the submission notes instead of a repo, and needed environment variables given in the README.md without disclosing them in the setup.sh.  That file should have been included in the .gitignore.*
___
## Introduction 

Casting Agency is mostly a back-end designed for a Full-Stack application.  The app models a company that will create a collection of actors and movies, and then assign actors to the cast of those motion pictures.

While the back-end work is complete, minimal work was done on the front-end.  There are front end pages that were added to assist with authentication, and were based upon Auth0 documentation found at https://auth0.com/docs/quickstart/webapp/python.  

## Technologies & Dependencies

This app was developed on a Linux Ubuntu 20.04.3 LTS OS, hence all following commands listed in this readme will reflect this.
The backend and API of this project was designed using Python and Flask.  
Authentication was implemented using a third party authentication service, Auth0.  
The application was deployed using Heroku.  
Testing was done using both unittest and Postman.

It is recommended to run the project in a virtual environment using virtualenv.
It can be installed usijng 'pip'
```
pip install virtualenv
```
All other required dependencies can be found in the file: requirements.txt  
[Back to Top](#Casting-Agency)  

## Folders & File Descriptions

* `.gitignore` &emsp; - A gitignore template provied by github.com https://github.com/github/gitignore/blob/main/Python.gitignore  
* `app.py` &emsp; - The main app file that defines the API's routes and error handling.  
* `codes.py` &emsp; - A file containing constants representing and describing various http response status codes.   
* `manage.py`  &emsp; - A file that allows Heroku to run the migrations from the locally created database to the hosted platform.
* `Procfile` &emsp; - A file that uses the Gunicorn pure-Python HTTP server to deploy the web app on Heroku.  
* `README.md` &emsp; - This file.  
* `requirements.txt` &emsp; - File that contains all the Python libraries required to support this application.  
* `setup.sh` &emsp; - A Shell Script that sets up the environment variables necessary to run the application and its full suite of tests.  
* `test_app.py` &emsp; - The unittest suite that tests all API endpoints at various group levels of permissions.  
* `auth/auth.py` &emsp; - This code interfaces with Auth0, and handles checking authentication and permissions for the API endpoints defined in `app.py`.  Most of the code is the boilerplate provided in the Project3 Coffee Shop.  
* `database/models.py` &emsp; - Python file defining the data models used to create the database tables.  
* `migrations/` &emsp; - The Alembic database migration folder created using Python's Flask-Migrate library.  
* `templates/` &emsp; - Folder containing html page files for the few front end pages.  

[Back to Top](#Casting-Agency)  

## Project Setup
1. Make sure the code is configured for local deployment.  
   - comment line 21, and uncomment line 23 in `app.py`  
   - comment lines 29-37 & uncomment lines 40-46 in `database/models.py`  
1. Clone the project into a local directory, or fork the project and pull the copy:
    ```
    git clone https://github.com/SonicEdge1/Udacity-FS-Capstone.git  
    cd Udacity-F5-Capstone   
    ```
1. Create a virtual environment & install Python libraries:

    ```
    python -m virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
1. Set up environment variables.  The necessary environment variables are contained in the `setup.sh` file and can be applied to the console environment with:
    ```
    source ./setup.sh  
    ```
1. Set up the postgresql database(s) required.
   - If the postgresql server needs installed and started, follow the instructions on the TablePlus page: https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html
   - From the command line run:
      ```
      sudo -u postgres psql
      ```
    - With the command line displaying 'postgres=#', run:
      ```
      create database casting
      create database casting_testdb
      create user myuser with encrypted password 'mypass';
      grant all privileges on database casting to myuser;
      grant all privileges on database casting_testdb to myuser;
      ```
1. Start the app server:
    ```
    flask run
    ```
1. Check functionality in browser:
Navigate to `http://127.0.0.1:5000/` or `http://127.0.0.1:5000/home`  

[Back to Top](#Casting-Agency)

## Running Tests:
- Follow steps 1-5 in [Project Setup](#Project-Setup) if those steps have not been executed.
- From the command line, run: `python3 test_app.py`  

## User Roles and Permissions  
There are three roles that can be assigned to authenticated users.  
1. The Casting Assistant  
   - Can view actors and movies  
1. The Casting Director  
   - Has all permissions a Casting Assistant has and…  
   - Can add or delete an actor from the database  
   - Can modify actors or movies  
1. The Executive Producer  
   - Has all permissions a Casting Director has and…  
   - Can add or delete a movie from the database  
* Those without an assigned role in Auth0 will only be able to access endpoints:
  * `http://127.0.0.1:5000/`  
  * `http://127.0.0.1:5000/home`  
  * `http://127.0.0.1:5000/dashboard` (after basic authentication with Auth0)  
  
  [Back to Top](#Casting-Agency)  

## Front end pages and endpoints:
`/home`  
  - This basic page shows a picture of a clapperboard and film reel along with the name of the app.  A log-in link is present.  

`/login`  
  - Redirects the user to the app log-in hosted by Auth0.  Allows users to log-in or create new accounts.  

`/logout`  
  - Clears session data and redirects the user to the home page.  

`/dashboard`
  - After log-in landing page that displays user's info along with links to other pages and /logout.  

[Back to Top](#Casting-Agency)  

## API Endpoints
A RESTful API was implemented.  It uses JSON to encode the responses and looks for JSON encoded data in POST and PATCH endpoints.  There are two main categories of endpoints: [Actors](#Actors), and [Movies](#Movies).  

</br>
GET '/'  

* Purpose: This basic endpoint served to test whether the application was alive.
* Permissions: No Roles or Permissions are required.
* Request Body Data: none
* Curl: `curl --location --request GET 'https://casting-agent-app.herokuapp.com/actors' \
--header 'Authorization: Bearer {BearerToken}'`
* It simply returns:
    ```
    {
      "message": "Hello World", 
      "success": true
    }
    ```
### ACTORS
GET '/actors'  

* Purpose: Returns all actors present in the database. 
* Permissions: A Casting Assistant Role or greater is required for access.
* Request Body Data: none
* Curl: `curl 'http://127.0.0.1:5000/actors' --header 'Authorization: Bearer {BearerToken}'`
* Sample Return:
    ```
    {
        "actors": [
            {
                "age": 60,
                "gender": "Male",
                "id": 1,
                "name": "Casey Siemaszko"
            },
            {
                "age": 21,
                "gender": "Male",
                "id": 2,
                "name": "Test Dummy"
            },
            {
                "age": 63,
                "gender": "Female",
                "id": 4,
                "name": "Andie MacDowell"
            }
        ],
        "success": true,
        "total_actors": 3
    }
    ```
GET '/actors/{int:actor_id}'  

* Purpose: Returns a specific actor in the database along with all the movies they have been cast in.
* Permissions: A Casting Assistant Role or greater is required for access.
* Request Body Data: none.
* Curl: `curl 'http://127.0.0.1:5000/actors/1' --header 'Authorization: Bearer {BearerToken}'`
* Sample Return:
    ```
    {
      "actor": {
        "age": 90, 
        "gender": "Male", 
        "id": 2, 
        "name": "Sean Connery"
      }, 
      "cast_in": [
        {
          "id": 6, 
          "releaseDate": "1981-11-06", 
          "title": "Time Bandits"
        }, 
        {
          "id": 7, 
          "releaseDate": "1996-06-07", 
          "title": "The Rock"
        }
      ], 
      "success": true
    }
    ```
POST '/actors'  

* Purpose: Adds an actor into the database. 
* Permissions: A Casting Director Role or greater is required for access.
* Request Body Data: An actor's name, age, and gender.
* Curl: *note - replace the {BearerToken} variable with a vlaid token.
    ```
    curl -X POST 'http://127.0.0.1:5000/actors' \
    --header 'Authorization: Bearer {BearerToken} \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name":"Andie MacDowell",
        "age":"63",
        "gender":"Female"
    }'
      ```
* Sample Return:  
    ```
    {
        "added_actor": {
            "age": 63,
            "gender": "Female",
            "id": 4,
            "name": "Andie MacDowell"
        },
        "success": true,
        "total_actors": 4
    }
    ```  
PATCH '/actors/{int:actor_id}'  

* Purpose: Update the actor's information in the database. 
* Permissions: A Casting Director Role or greater is required for access.
* Request Body Data: Any combination of an actor's name, age, or gender.  If no data is given, the request will return "success": true, along with the actor's original data.
* Curl: *note - replace the {BearerToken} variable with a vlaid token.
    ```
    curl -X PATCH 'http://127.0.0.1:5000/actors/1' \
    --header 'Authorization: Bearer {Bearer_Token} \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "age": "57"
    }'
    ```
* Sample Return:
    ```
    {
        "actor": {
            "age": 57,
            "gender": "Male",
            "id": 1,
            "name": "Casey Siemaszko"
        },
        "success": true
    }
    ```
DELETE '/actors/{int:actor_id}'

* Purpose: Removes an actor from the database. 
* Permissions: A Casting Director Role or greater is required for access.
* Request Body Data: none
* Curl: `curl -X DELETE 'https://127.0.0.1:5000/actors/3' --header 'Authorization: {BearerToken}'`
* Sample Return:
    ```
    {
        "deleted_actor_id": "3",
        "deleted_actor_name": "Another Test Dummy",
        "success": true
    }
    ```
### Movies
GET '/movies'

* Purpose: Returns all movies present in the database. 
* Permissions: A Casting Assistant Role or greater is required for access.
* Request Body Data: none
* Curl: `curl -X GET 'http://127.0.0.1:5000/movies' --header 'Authorization: Bearer {BearerToken}'`
* Sample Return:
    ```
    {
        "movies": [
            {
                "id": 1,
                "releaseDate": "1987-10-09",
                "title": "Three O Clock High"
            },
            {
                "id": 2,
                "releaseDate": "1981-11-06",
                "title": "Time Bandits"
            }
        ],
        "success": true,
        "total_movies": 2
    }
    ```
GET '/movies/{int:movie_id}'  

* Purpose: Returns a specific movie in the database along with the cast of that movie.
* Permissions: A Casting Assistant Role or greater is required for access.
* Request Body Data: none.
* Curl: `curl 'http://127.0.0.1:5000/movies/1' --header 'Authorization: Bearer {BearerToken}'`
* Sample Return:
    ```
    {
      "movie": {
        "id": 6, 
        "releaseDate": "1981-11-06", 
        "title": "Time Bandits"
      }, 
      "movie_cast": [
        {
          "age": 90, 
          "gender": "Male", 
          "id": 2, 
          "name": "Sean Connery"
        }, 
        {
          "age": 60, 
          "gender": "Male", 
          "id": 3, 
          "name": "Jack Purvis"
        }, 
        {
          "age": 51, 
          "gender": "Female", 
          "id": 4, 
          "name": "Shelley Duvall"
        }, 
        {
          "age": 60, 
          "gender": "Male", 
          "id": 5, 
          "name": "John Cleese"
        }
      ], 
      "success": true
    }
    ```
PATCH '/moives/{int:movie_id}'  

* Purpose: Updates the movie's information in the database. 
* Permissions: A Casting Director Role or greater is required for access.
* Request Body Data: Any combination of an movie's title, release_year and release_month and release_day, or actors list.  Note that if any value of the release date is missing, that the request will return a 400 error.  If an actor id that doesn't exist is added to the 'actors' list, then a 422 error will be returned. If no data is given, the request will return "success": true, along with the movie's original data.
* Curl: *note - replace the {BearerToken} variable with a vlaid token.
    ```
    curl -X PATCH 'http://127.0.0.1:5000/movies/4' \
    --header 'Authorization: Bearer {Bearer_Token} \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title": "Cloak and Dagger",
        "actors": ["3","4"]
    }'
    ```
* Sample Return:
    ```
    {
        "movie": {
            "id": 4,
            "releaseDate": "1984-07-13",
            "title": "Cloak and Dagger"
        },
        "movie_cast": [
            {
                "age": 57,
                "gender": "Male",
                "id": 1,
                "name": "Casey Siemaszko"
            }
        ],
        "success": true
    }
    ```
POST '/movies'  

* Purpose: Adds a movie into the database. 
* Permissions: An Executive Producer Role or greater is required for access.
* Request Body Data: The Movie's title, release_year, release_month, and release_day are all required.  The actors id list is optional.
* Curl: *note - replace the {BearerToken} variable with a vlaid token.
    ```
    curl -X POST 'http://127.0.0.1:5000/movies' \
    --header 'Authorization: Bearer {BearerToken} \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title":"The Last Starfighter",
        "release_year":"1984",
        "release_month":"7",
        "release_day":"13",
    }'
    ```
* Sample Return:
    ```
    {
        "added_movie": {
            "id": 3,
            "releaseDate": "1984-07-13",
            "title": "The Last Starfighter"
        },
        "movie_cast": [],
        "success": true,
        "total_movies": 3
    }
    ```
DELETE '/movies/{int:movie_id}'

* Purpose: Removes an actor from the database. 
* Permissions: An Executive Producer Role or greater is required for access.
* Request Body Data: none
* Curl: `curl -X DELETE 'https://127.0.0.1:5000/movies/3' --header 'Authorization: {BearerToken}'`
* Sample Return:
    ```
    {
        "deleted_movie_id": 3,
        "deleted_movie_title": "The Last Starfighter3",
        "success": true
    }
    ```
[Back to Top](#Casting-Agency)  

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request  
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found 
- 405: Method Not Allowed
- 422: Not Processable 
- 500: Internal Server Error  

[Back to Top](#Casting-Agency)  

## Deployment to Heroku
To deploy to heroku:
1. Prep Code for remote deployment.
   - uncomment line 21, and comment line 23 in `app.py`  
   - uncomment lines 29-37 & comment lines 40-46 in `database/models.py`  
1. Make sure the heroku cli is installed: `curl https://cli-assets.heroku.com/install-ubuntu.sh | sh` - or - `sudo snap install --classic heroku`  
1. Create your app with the cli: `heroku create <name_of_your_app> `  
1. Add the heroku git url to your repository: `git remote add heroku <heroku_git_url> `  
1. Add the postgresql add-on for the database: `heroku addons:create heroku-postgresql:hobby-dev --app <name_of_your_app>`  
1. Go to the heroku dashboard for your project, Select the Settings tab, Click on Reveal Config Vars, and add all necessary configuration variables such as the ones contained in the `setup.sh` file.  
1. Run: `heroku config --app <name_of_your_app>` to check configurations variables.
1. Push the repository code to Heroku: `git push heroku master`  
1. Run database migrations: `heroku run python manage.py db upgrade --app <name_of_your_app>`   
1. Confirm deployment by visiting https://<name_if_your_app>.herokuapp.com/

### Useful Heroku commands :
`heroku run bash` - Opens shell in Heroku environment to navigate uploaded files.  
`heroku pg:psql` - Accesses the deployed PostgreSQL db.  
`heroku pg:backups:capture <name_of_your_app>` - Creates a backup file of the database data.  
`heroku pg:backups:download` - Downloads the backup data file.  
[Back to Top](#Casting-Agency)  

## PEP 8 Styling
* Code was partially auto-stylized using autopep8  
  https://pypi.org/project/autopep8/  
  ```
  pip install --upgrade autopep8
  autopep8 --in-place --aggressive --aggressive <filename>
  ```
* Code was tested for sytle compliance using pycodestyle  
  https://pypi.org/project/pycodestyle/  
  ```
  pip install pycodestyle
  pycodestyle --first <filename>
  ```
