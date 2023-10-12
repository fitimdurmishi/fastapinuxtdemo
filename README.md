Below are infos about the configuration needed to run the projects


# DB related

First of all, database environment is needed to configure.

RDBMS system used for this project is Postgresql, so we need Postgresql server (i have used localhost, if you want to use different server, then you need appropriate connection string, will show on connection string below on API configs).

First on the DB server (i have it here on localhost), we create the database named 'datacose', withe the command:

	createdb -h localhost -p 5432 -U postgres datacose

Then we create/restore the schema of the DB, with seeded data for the tables. This is done by using the file db_datacose.sql and the following command:

	psql -h localhost -p 5432 -U postgres -d datacose -f {ENTER-HERE-THE-PATH-TO-THIS-FILE}/db_datacose.sql




# api

API project is located on the folder: ~/src/api . FastAPI is used as technology for the development of the REST service.

Needed python libraries are needed to install.

We need to set the appropriate connection string to the database. This is done by editing the value of DATABASE_URL key on the env file: ~/src/api/.env

	DATABASE_URL = "postgresql://postgres:postgres@localhost/datacose"

I have used here, localhost server, datacose is the name of the database, and username/password as postgres/postgres. You can set here the correct values for your environment.

To start the api server, cd to the ~/src/api folder and execute the command:

	# for MAC operating systems
	uvicorn main:app --reload --port 8000

	# for Windows
	python -m uvicorn main:app --reload --port 8000




# dashboard

The front-end project is located on the folder: ~/src/dashboard . Nuxt 2 is used as technology here.

Here also we have env file, located on the folder ~/src/dashboard/.env where we need to set the correct API_URL value for your environment:

	API_URL = http://127.0.0.1:8000

To start the app, first we install the required modules with:

	npm install

then

	npm run dev


To login on the system you will use these ceredentials: fito/fito