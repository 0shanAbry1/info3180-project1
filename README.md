# INFO3180 Project 1
Flask based application that accepts and displays user proﬁle information

#### Request: GET >> Response: Renders an HTML template
- New User Profile >> curl -X GET http://0.0.0.0:8080/profile
- User Profiles (List) >> curl -X GET http://0.0.0.0:8080/profiles
- User Profile (Individual) >> curl -X GET http://0.0.0.0:8080/profile/<userid>

#### Request: POST >> Response: Returns a JSON object
- User Profiles (List) >> curl -H "Content-Type: application/json" -X POST http://0.0.0.0:8080/profiles
- User Profile (Individual) >> curl -H "Content-Type: application/json" -X POST http://0.0.0.0:8080/profile/<userid>
