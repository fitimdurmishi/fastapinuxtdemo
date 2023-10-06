# datacosechallenge

# api
python -m uvicorn main:app --reload
uvicorn main:app --reload
uvicorn main:app --reload --port 8001

curl -X POST "http://127.0.0.1:8000/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=password"

curl -X GET "http://127.0.0.1:8000/secure-data" -H "accept: application/json" -H "Authorization: Bearer <YOUR_TOKEN>"


# dashboard

	npm install

  To get started:
	cd dashboard
	npm run dev

  To build & start for production:
	cd dashboard
	npm run build
	npm run start