HTTP Basic Authentication is a simple authentication mechanism used in Hypertext Transfer Protocol (HTTP) for securing web resources. It is a widely supported method for authenticating users and is based on a challenge-response mechanism. When a server requires HTTP Basic Authentication, the client must send a username and password in the form of a base64-encoded string in the HTTP request headers.

Here's how it works:

Server Request: When you try to access a resource protected by HTTP Basic Authentication, the server responds with a status code of 401 Unauthorized and includes a WWW-Authenticate header field in the response. This header contains the authentication method, which is typically "Basic," and a realm, which is a description of the protected area.

Client Response: The client (e.g., a web browser) receives the 401 response and prompts the user for their username and password. The client then encodes the username and password as a single string in the format "username:password."

Base64 Encoding: The client encodes the "username:password" string in Base64 format. This encoded string is then sent in the Authorization header in the subsequent request.

Server Verification: The server receives the request with the Authorization header, decodes the Base64-encoded string, and verifies the credentials. If the credentials are valid, the server grants access to the protected resource.

for example:

GET /secure/resource HTTP/1.1
Host: example.com
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
In the Authorization header, "dXNlcm5hbWU6cGFzc3dvcmQ=" is the Base64-encoded string "username:password."

It's important to note that HTTP Basic Authentication is not considered highly secure on its own, as the credentials are transmitted in an easily decodable format (Base64) and can be intercepted by malicious actors. To enhance security, it is often used in combination with HTTPS (SSL/TLS) to encrypt the communication between the client and server.

More secure authentication mechanisms, such as OAuth 2.0 or JSON Web Tokens (JWT), are recommended for modern web applications to provide better security and user authentication features.


# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

