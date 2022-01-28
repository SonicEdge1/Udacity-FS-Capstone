# Udacity-FS-Capstone
Capstone Project for the Udacity Full-Stack course

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
https://auth0.com/docs/quickstart/webapp/python
https://howtocreateapps.com/fetch-and-display-json-html-javascript/

pip install -r requirements.txt

pip list
FLASK_DEBUG=true


python3
import app.py
import db, Model1, Model2
model1 = Model1(item="text")
model2 = Model2(item="test", second_item=3)
db.session.add(model1, model2)
db.session.commit()

psql <dbname>
select * from model1;
\q


python3
>>> import models
>>> from models import db, Actor, Movie


>>> date1 = date(2005,12,25)
>>> movie1 = Movie(title="Earth Swarm", releaseDate=date1)
>>> date2 = date(1995,7,3)
>>> movie2 = Movie(title="Earth Dead", releaseDate=date2)
>>> actor1 = Actor(name="John Wayne", age=50, gender="Male")
>>> actor2 = Actor(name="Sean Connery", age=55, gender="male")
>>> actorList = [actor1, actor2]
>>> movie2 = Movie(title="Earth Dead", releaseDate=date2, actors=actorList)





export FLASK_ENV=development
export FLASK_APP=api.py
flask run --reload

curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/actors
curl -X POST -H "Content-Type: application/json" -d '{"name":"Sean Connery", "age":"77", "gender":"Male"}' http://127.0.0.1:5000/actors



curl -X POST -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZGYxNjkzYTFlM2FjMDA2OWVhMGZiOSIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDI2MTU2MDcsImV4cCI6MTY0MzIyMDQwNywiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCIsInBhdGNoOmFjdG9ycy1hbmQtbW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.brabOGdocQUTTtGGvTla3wkZApk0XzMtzcKKNX6QN041_e-NibTT8_2SnJI352mWYkLjq2WfNG-NfRW4ZG8N-9Z51ZfOGVKzWTA-XNVq9AVVjtgPbI4rcSJyVC7-JM4n0MoYB-znOCqPoM9j_ieK86IGgEYrM2cRQyrAOfoXBpt4nOAk6uQqugcHkh_zK56ek6KdbwwdMs4q72sU5HPcsAbYCIlshkk8XoGQpyDapKZWFanK8qVvktWFl3Asg6oqnmJjsaVm-GE4pBNxexW8XYQG6i3eAaQ-cjwb-JIHQpXlbqre70c3qJ-kzrUfwTMJDPzLWaJXp2m1lFrMAxJR2g" -H "Content-Type: application/json" -d '{"name":"Test Dummy", "age":"77", "gender":"Male"}' http://127.0.0.1:5000/actors

curl -X POST -H "Authorization: Bearer "$EXE_JWT -H "Content-Type: application/json" -d '{"name":"Another Test Dummy", "age":"77", "gender":"Male"}' http://127.0.0.1:5000/actors

curl -X POST -H "Authorization: Bearer "$EXE_JWT -H "Content-Type: application/json" -d '{"title":"Me and the Big Guy", "release_year":"1987", "release_month":"10", "release_day":"9"}' http://127.0.0.1:5000/movies

curl -X POST -H "Content-Type: application/json" -d '{"name":"Casey Siemaszko", "age":"60", "gender":"Male"}' http://127.0.0.1:5000/actors

curl -X POST -H "Content-Type: application/json" -d '{"name":"Casey Siemaszko", "age":"60", "gender":"Male"}' http://127.0.0.1:5000/actors


curl -X PATCH -H "Content-Type: application/json" -d '{"name":"Sean Connery", "age":"90", "gender":"Male"}' http://127.0.0.1:5000/actors/1

curl -X PATCH -H "Content-Type: application/json" -d '{"gender":"Female"}' http://127.0.0.1:5000/actors/1

curl -X POST -H "Content-Type: application/json" -d '{"title":"Three O Clock High", "release_year":"1987", "release_month":"10", "release_day":"9"}' http://127.0.0.1:5000/movies

curl -X POST -H "Content-Type: application/json" -d '{"title":"Time Bandits", "release_year":"1981", "release_month":"11", "release_day":"6"}' http://127.0.0.1:5000/movies


curl http://127.0.0.1:5000/movies

curl -X PATCH -H "Content-Type: application/json" -d '{"title":"Three O Clock High", "release_year":"1987", "release_month":"10", "release_day":"9", "actors": '["1","2"]'}' http://127.0.0.1:5000/movies/1

curl -X POST -H "Content-Type: application/json" -d '{"title":"Cloak & Dagger", "release_year":"1984", "release_month":"7", "release_day":"13", "actors": '["1","2"]' }' http://127.0.0.1:5000/movies


flask db init
flask db migrate
//no worky?//
DATABASE_URL=sqlite:/// flask db migrate
// other error
ERROR [flask_migrate] Error: Can't locate revision identified by 'bb2aa6fe2c2b'
flask db revision --rev-id bb2aa6fe2c2b
have to delete the albemic table in the db to remove all revision history

flask db stamp head

flask db migrate
flask db upgrade
flask db downgrade

https://alembic.sqlalchemy.org/en/latest/
https://flask-migrate.readthedocs.io/en/latest/


https://joes-casting-agency.us.auth0.com/authorize?
  response_type=token&
  client_id=JuRJnYtiGutFcvYN4Wtx2O1bynCd4Eoo&
  connection=CONNECTION&
  redirect_uri=https://127.0.0.1:5000/login-results

https://joes-casting-agency.us.auth0.com/authorize?audience=CastingAgencyAPI&response_type=token&client_id=OhcNdLC90mi5E0R77RlC526RP1Khrl7q&redirect_uri=http://127.0.0.1:5000/

http://127.0.0.1:5000/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZDhjMThmODEzYzFkMDA2YTk1ZTZmMyIsImF1ZCI6IkNhc3RpbmdBZ2VuY3lBUEkiLCJpYXQiOjE2NDE5MzQ5NTgsImV4cCI6MTY0MTk0MjE1OCwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtYW5kLW1vdmllcyJdfQ.Xa0aPoRLhuWRdC8_ZPzAoBqL-d-UqRYSL8YBGeFzDxAzQ9fKGqpaprKk2_Ri8jjskOxOQjBiY0kHxhT1NuEDSWAdR_3XT9d8F3tjYS6zWNPLNRseiQD2ORXhFfFB7TkG5Uuej_Ae3LJGJmr0lbsSx6xeuIx8vRpCcE2wvSjqNo2uDh2vSpMPvQwgGceYV67dMoDGTYFPJKEoty7bkgPqpoteO_J4qkXhiK7WgAK0T7GLYrqDHwCClVyrpd5Dx6uiiNmkTXkvA4UyatJLoKGYxu5bkpoXrr8rC8LNTLyRIav8-H83lUy9HbtmzG15RYTk8xQebx3fuWjKqqxwgz8dWQ&expires_in=7200&token_type=Bearer



sandbox / casting assistant key
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZDhjMThmODEzYzFkMDA2YTk1ZTZmMyIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDIwMDc5NjUsImV4cCI6MTY0MjYxMjc2NSwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCJdfQ.tIiWQq8gOT7_6ILcDPnAxtDfEerX3LeHgeMeywjobMaBEB3xTDpFxSpX9tLGqyz3ay-TQ-RjlLWhvkblSXs6d1ktTn--imjeF9vJMwKJgZo2BCwfUT55YN9-vrE6NIuR_-kh5tGaI9iQ7mT2gGF-fXS3o8-ihS_okoFfHNqjb1EYbGmptUJo5Ok5S_S_R8vGMPCfc0E92omjRzYpX0TOI0iWL3ysrsLzlNvyr9BQtV-BIVdiXQlRbCHIAmG5nsoosuu1nH1jPm7VxCYBlikvuKhKkx_5Q9k4wzN1ki4vdHZPYgGjU-5FhNo-sgUIIpmJZkFQ_N9gxeLlJGEZPfrQhg

sonofskywalker / casting director
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZGYxNDNkN2E5NThjMDA3MGE0NjcyZCIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDIwMDk5OTgsImV4cCI6MTY0MjYxNDc5OCwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCIsInBhdGNoOmFjdG9ycy1hbmQtbW92aWVzIiwicG9zdDphY3RvciJdfQ.e_Ucyc6rOxkUGpbXhGTEg46Q77dJiQyaa1fK7Kkwo6mBLgnOq3SOkPk7kbDwgHWSUU2YtRrSyKgmb0nFmHL7ybP8C0R4yTYhkGCaS3IhdUTvIRnq_sublvexLoNcErzD6uLut2KUHenAD0NY18meN4zRM_v8Z26elsdO_HIzJWIDYLdHZXRB1u2fFlN1AMQvDbMq0ImY8U93LgXl0VWLdtBPhlsmU1AvwwiqZLi3Ynzco1xj3HdZtP581mqGOwcjMd6ihPJUWm5yP29oRHLIdu4TQhSGD5Q0XP9KgvtZWBJbsNSVwdKATkMNkyU18iUm-OzZjEB2pbxUm100zAhw9A

emailjoebell / executive producer
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZGYxNjkzYTFlM2FjMDA2OWVhMGZiOSIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDIwMTAzNzYsImV4cCI6MTY0MjYxNTE3NiwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCIsInBhdGNoOmFjdG9ycy1hbmQtbW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.OuDG77ThXxK-zv83Da4SQb65ASBJe9cixGwLpgV1Pf5NZWX6eBNqaQ8hNIEGdxxBsIjHSLMLEpfZR8b4ztbqoePsuLuIbSiEMRnOD2MQvAFifT8mled9nvZDDy8UjPYdE9qetH4eHb49n9TI-ceEbjAS-lTCw_X2viepiZ92PPjXAIedAyg7QoqDar1oH1_5hxqFdR5fHjuR5fh2huywXsA6Lw8B6T0D0k8FvxzmsQraFUc7dkH7FejtqZjysYkO8fT8mtSBxd-bLDLlb9JumLljQ-tBEUQL9Ir_dL5WXpdhyLMPxydcdKI447ch-VuiESi3GrjaVrLML1vPg-84bQ





header:  {('Authorization', 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZGYxNjkzYTFlM2FjMDA2OWVhMGZiOSIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDIwMTAzNzYsImV4cCI6MTY0MjYxNTE3NiwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCIsInBhdGNoOmFjdG9ycy1hbmQtbW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.OuDG77ThXxK-zv83Da4SQb65ASBJe9cixGwLpgV1Pf5NZWX6eBNqaQ8hNIEGdxxBsIjHSLMLEpfZR8b4ztbqoePsuLuIbSiEMRnOD2MQvAFifT8mled9nvZDDy8UjPYdE9qetH4eHb49n9TI-ceEbjAS-lTCw_X2viepiZ92PPjXAIedAyg7QoqDar1oH1_5hxqFdR5fHjuR5fh2huywXsA6Lw8B6T0D0k8FvxzmsQraFUc7dkH7FejtqZjysYkO8fT8mtSBxd-bLDLlb9JumLljQ-tBEUQL9Ir_dL5WXpdhyLMPxydcdKI447ch-VuiESi3GrjaVrLML1vPg-84bQ'), ('Content-Type', 'application/json')}

header:  {('Content-Type', 'application/json'), ('Authorization', 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYYW5ieVliZHBoTmUyTFB4bC1nSSJ9.eyJpc3MiOiJodHRwczovL2pvZXMtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZGYxNjkzYTFlM2FjMDA2OWVhMGZiOSIsImF1ZCI6WyJDYXN0aW5nQWdlbmN5QVBJIiwiaHR0cHM6Ly9qb2VzLWNhc3RpbmctYWdlbmN5LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDIwMTAzNzYsImV4cCI6MTY0MjYxNTE3NiwiYXpwIjoiT2hjTmRMQzkwbWk1RTBSNzdSbEM1MjZSUDFLaHJsN3EiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycy1hbmQtbW92aWVzIiwiZ2V0OmRhc2hib2FyZCIsInBhdGNoOmFjdG9ycy1hbmQtbW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.OuDG77ThXxK-zv83Da4SQb65ASBJe9cixGwLpgV1Pf5NZWX6eBNqaQ8hNIEGdxxBsIjHSLMLEpfZR8b4ztbqoePsuLuIbSiEMRnOD2MQvAFifT8mled9nvZDDy8UjPYdE9qetH4eHb49n9TI-ceEbjAS-lTCw_X2viepiZ92PPjXAIedAyg7QoqDar1oH1_5hxqFdR5fHjuR5fh2huywXsA6Lw8B6T0D0k8FvxzmsQraFUc7dkH7FejtqZjysYkO8fT8mtSBxd-bLDLlb9JumLljQ-tBEUQL9Ir_dL5WXpdhyLMPxydcdKI447ch-VuiESi3GrjaVrLML1vPg-84bQ')}

curl --request POST --url https://joes-casting-agency.us.auth0.com/oauth/token --header 'content-type: application/json' --data '{"client_id":"JuRJnYtiGutFcvYN4Wtx2O1bynCd4Eoo" "client_secret":"rYCLRCHYTSRAJo4pT2c0Yw4freQpHaYYGZTgY9cZlc1pWq1z6Mf7LhlpD1SXMgwQ","audience":"CastingAgencyAPI","grant_type":"client_credentials"}'


json:  {'title': 'Goonies', 'release_year': '1985', 'release_month': '6', 'release_day': '7', 'actors': ['1', '2', '3']}
json:  {'edited_movie_title': 'New Title', 'edited_movie_year': '1984', 'edited_movie_month': '7', 'actors': ['1']}


AUTO STYLE CODE TO PEP8 STANDARDS
https://pypi.org/project/autopep8/
$ pip install --upgrade autopep8
$ autopep8 --in-place --aggressive --aggressive <filename>

-Testing if code is compliant
https://pypi.org/project/pycodestyle/
$ pip install pycodestyle
$ pycodestyle --first <filename>



deploy to heroku:
heroku create <name_of_your_app>
git remote add heroku <heroku_git_url>
heroku addons:create heroku-postgresql:hobby-dev --app <name_of_your_app>  //add-on for db instance
heroku config --app <name_of_your_app>


Creating ⬢ casting-agent-app... done
https://casting-agent-app.herokuapp.com/ | https://git.heroku.com/casting-agent-app.git
=== casting-agent-app Config Vars
DATABASE_URL: postgres://xibzplxukrsyqb:ac5916d7271da41c21c3695491e47d3595ba31c5a1ee644413715e097320bfdb@ec2-52-1-20-236.compute-1.amazonaws.com:5432/d23cmcbfab52ss

Useful Heroku commands :

heroku run bash - To see if files are there.
heroku pg:psql - To get access to your PostgreSQL db.
heroku pg:backups:capture --app your_app_name - To make a backup of your data
heroku pg:backups:download - To download your backup