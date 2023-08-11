# Lab Orchestration

_USD Lab Orchestration Site_

## Features
* Vue-JS frontend and Flask backend
* SQLAlchemy database of lab assignments, courses, and users
* Group creation and collaboration on assignments
* Different user permission levels
* Live feedback for professors and students during in-person lab sessions

## Run on local server
1. Clone the repository

2. Create virtual environment

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    ```

3. Initialize database 

    ```sh
    (env)$ flask db upgrade
    ```

4. Create an admin user with your information

    ```sh
    (env)$ flask shell
    >>> from app import app, db
    >>> user = User('YOUR_NAME', 'YOUR_EMAIL', 'admin', 'YOUR_PASSWORD')
    >>> db.session.add(user)
    >>> db.session.commit()
    >>> exit()
    ```

5. Run the flask server

    ```sh
    (env)$ flask run --port=5001 --debug
    ```

6. Create a new terminal window and run Vue-JS app

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
    ```

7. Navigate to the website in your browser of choice
    [http://localhost:5173/login](http://localhost:5173/login)

8. Login with the user you created