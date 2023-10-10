# datacosechallenge

# api

starting api app

python -m uvicorn main:app --reload
uvicorn main:app --reload
uvicorn main:app --reload --port 8001

-- when starting on Windows we need to add: 'python -m'
python -m uvicorn main3:app --reload

uvicorn api2.main:app --reload
python -m uvicorn main:app --reload

curl -X POST "http://127.0.0.1:8000/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=password"
curl -X GET "http://127.0.0.1:8000/secure-data" -H "accept: application/json" -H "Authorization: Bearer <YOUR_TOKEN>"


pip install databases databases[postgresql]
pip install alembic psycopg2 python-dotenv

resources
https://www.educative.io/answers/how-to-use-postgresql-database-in-fastapi
https://fastapi.tiangolo.com/tutorial/sql-databases/#create-your-fastapi-path-operations
https://www.smashingmagazine.com/2020/05/getting-started-axios-nuxt/


curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Item Name", "description": "Updated Item Description"}' http://127.0.0.1:8001/items/3



# dashboard

	create-nuxt-app {app-name}

	npm install

  To get started:
	cd dashboard
	npm run dev

  To build & start for production:
	cd dashboard
	npm run build
	npm run start