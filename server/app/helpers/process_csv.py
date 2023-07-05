from app.models import User
from app import app, db
import csv
import os
from werkzeug.utils import secure_filename

def read_csv(csv_file):
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
    name = row[1] + ' ' + row[0]
    email = row[2] + '@sandiego.edu'
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(name=name, email=email, role='student')
        db.session.add(user)
        db.session.commit()
    return user