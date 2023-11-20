# SMS API Setup and Testing

## Setup

To test and use this API, follow these steps:
1. **Download the Code:**
   ```bash
   $ sudo apt-get update
   $ sudo apt-get install subversion
   $ svn checkout https://github.com/dennis-22-csc/backend_python/trunk/api/sms_api

2. **Remove .svn Directory:**
   ```bash
   $ cd sms_api
   $ rm -rf .svn
   
3. **Create Virtual Environment:**
	```bash
	$ python3 -m venv sms_api_env

4. **Activate Virtual Environment:**
	```bash
	$ source sms_api_env/bin/activate

5. **Install Dependencies:**
	```bash
	$ pip install -r requirements.txt

6. **Run the API:**
	```bash
	$ python3 -m v1.messages.app

7. **Test the API:**

In a new shell session, run the following commands:

**Check Status:**
    ```bash
    $ curl -X GET http://localhost:5000/v1/messages/status

**Get Headers and Status:**
    ```bash
    $ curl -sI http://localhost:5000/v1/messages/status

**Send SMS:**
    ```bash
    $ curl -X POST http://localhost:5000/v1/messages/sms \
         -H "Content-Type: application/json" \
         -H "Authorization: xxxxxxadfrt" \
         -d '{"to": "+234871093756", "message": "Hey there"}'

*Note: The last command will return a JSON response indicating an unauthorized request.*

8. **Get an Access Token:**

**Request Authorization Code:**
    ```bash
    $ curl -X POST -H "Content-Type: application/json" -d '{"email": "your_email@example.com"}' http://localhost:5000/v1/oauth/auth_code

**Register as a Client:**
    ```bash
    $ curl -X POST -H 'Authorization: your_authorization_code' -H "Content-Type: application/json" -d '{
        "full_name": "Your Full Name",
        "email": "your_email@example.com",
        "password": "your_password"
    }' http://localhost:5000/v1/oauth/register_client
   
    *This step will provide you with a client id and client secret.*

**Request Access Token:**
    ```bash
    $ curl -X POST http://localhost:5000/v1/oauth/access_token \
        -H "Content-Type: application/json" \
        -d '{"client_id": "your_client_id", "client_secret": "your_client_secret"}' \
        -d 'grant_type=client_credentials'
    

9. **Retry Sending a Message with Obtained Token:**
	```bash
	$ curl -X POST http://localhost:5000/v1/messages/sms \
     -H "Content-Type: application/json" \
     -H "Authorization: your_access_token" \
     -d '{"to": "+234871093756", "message": "Hey there"}'

