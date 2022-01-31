#!/bin/bash
export AUTH0_ALGORITHMS=['RS256']
export AUTH0_API_AUDIENCE='CastingAgencyAPI'  #when setting up in heroku, leave off the ''
export AUTH0_API_BASE_URL=https://joes-casting-agency.us.auth0.com
export AUTH0_CALLBACK_URL=http://127.0.0.1:5000/callback
export AUTH0_CLIENT_ID=
export AUTH0_CLIENT_SECRET='' #when setting up in heroku, leave off the ''
export AUTH0_DOMAIN=joes-casting-agency.us.auth0.com
export AUTH0_REMOTE_CALLBACK_URL=https://casting-agent-app.herokuapp.com/callback

export FLASK_ENV=development
export FLASK_APP=app.py
export FLASK_DEBUG=true

export HEROKU_URI=''

export SECRET_KEY='' #when setting up in heroku, leave off the ''
export SESSION_KEY="access_token" #when setting up in heroku, leave off the ""

export EXEC_JWT=''
export DIRECT_JWT=''
export ASSIST_JWT=''
echo "done";
