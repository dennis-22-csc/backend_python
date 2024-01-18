# SMS API Setup and Testing

## Setup

To test and use this API, follow these steps:

1. **Download the Code using Subversion:**
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install subversion
    $ svn checkout https://github.com/dennis-22-csc/backend_python/trunk/api/fast_api/application/sms_api
    ```

2. **Remove .svn Directory:**
    ```bash
    $ cd sms_api
    $ rm -rf .svn
    ```

3. **Create Virtual Environment:**
    ```bash
    $ python3 -m venv sms_api_env
    ```

4. **Activate Virtual Environment:**
    ```bash
    $ source sms_api_env/bin/activate
    ```

5. **Install Dependencies:**
    ```bash
    $ pip install -r requirements.txt
    ```

6. **Set up MYSQL Database:**

    Run the following commands:

    **Login to root:**
    ```bash
    $ mysql -u root -p
    ```

    **Run MYSQL setup script:**
    ```bash
    $ source setup_mysql_dev.sql
    ```

    **Exit root:**
    ```bash
    $ exit 
    ```

7. **Run the API:**
    ```bash
    $ uvicorn v1.messages.app:app
    ```

7. **Test the API:**

    In a new shell session, run the following commands:

    **Check Status:**
    ```bash
    $ curl -X GET http://localhost:8000/v1/messages/status
    ```
    
    **Send SMS:**
    ```bash
    $ curl -X POST http://localhost:8000/v1/messages/sms \
         -H "Content-Type: application/json" \
         -H "Authorization: xyxwdaorhd" \
         -d '{"to": ["+234871093756"], "message": "Hey there"}' 
    ```
    *Note: The last command will return a JSON response indicating an unauthorized request.*

8. **Get an Access Token:**

    **Kill the message server with CTRL-C and start the auth server with the below:**
    ```bash
    $ uvicorn v1.oauth.app:app
    ```
    
    **In a new shell session, request Authorization Code:**
    ```bash
    $ curl -X POST -H "Content-Type: application/json" -d '{"email": "your_email@example.com"}' http://localhost:8000/v1/oauth/auth_code
    ```
	
    **Register as a Client:**
    ```bash
    $ curl -X POST -H 'Authorization: your_receieved_authorization_code' -H "Content-Type: application/json" -d '{
            "full_name": "Your Full Name",
            "email": "your_email@example.com",
            "password": "your_password"
        }' http://localhost:8000/v1/oauth/register_client
    ```

    *This step will provide you with a client id and client secret.*

    **Request Access Token:**
    ```bash
    $ curl -X POST http://localhost:8000/v1/oauth/access_token?grant_type=client_credentials -H 'Content-Type: application/json' -d '{
        "client_id": "your_client_id","client_secret": "your_client_secret"
    }'
    ```
	
9. **Kill the auth server with CTRL-C and start the messages server with the below:**
  ```bash
    $ uvicorn v1.messages.app:app
  ```
    
10. **Retry Sending a Message with Obtained Token:**
  ```bash
    $ curl -X POST http://localhost:8000/v1/messages/sms \
        -H "Content-Type: application/json" \
        -H "Authorization: your_access_token" \
        -d '{"to": ["+234871093756"], "message": "Hey there"}'
  ```

11. **Tear down MYSQL Database:**

    Run the following commands:

    **Login to root:**
    ```bash
    $ mysql -u root -p
    ```

    **Run MYSQL tear down script:**
    ```bash
    $ source tear_down_mysql_dev.sql
    ```

    **Exit root:**
    ```bash
    $ exit 
    ```
