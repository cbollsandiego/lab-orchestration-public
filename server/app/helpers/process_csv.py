from app.models import User
from app import app, db
import csv
import os
from werkzeug.utils import secure_filename

def read_csv(csv_file):
    '''
    This function reads through a .csv file, and creates a new User in the database for each user in the file.
    The .csv file must have the user's last name in the first column, first name in the second column, and USD username in the 
    third column (not including '@sandiego.edu'). This is the same format that Blackboard will give a file of students in.
    params: 
        -csv_file: the csv file to be read and added into the databse.
    '''
    filename = secure_filename(csv_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    csv_file.save(filepath)
    users_list = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            users_list.append(make_user(row=row))
    os.remove(filepath)
    return users_list

def make_user(row):
    '''
    This is the function that actually creates a User object and adds the user to the database, given a row from the csv file
    given to the function above.
    '''
    name = row[1] + ' ' + row[0]
    email = row[2] + '@sandiego.edu'
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(name, email, 'student', 'password')
        db.session.add(user)
        db.session.commit()
    return user