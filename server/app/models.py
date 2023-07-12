from app import db, login
from flask_login import UserMixin
from sqlalchemy import event
from hashlib import md5

user_course = db.Table('user_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    courses = db.relationship('Course', secondary='user_course', backref='users')

    groups = db.relationship('Group', secondary='user_group', backref='users')

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"

    def profile_photo(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(digest, size)
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "role": self.role,
                }

@event.listens_for(User, 'before_delete')
def remove_courses_from_user(mapper, connection, target):
    connection.execute(user_course.delete().where(user_course.c.user_id == target.id))

@event.listens_for(User, 'before_delete')
def remove_courses_from_user(mapper, connection, target):
    connection.execute(user_group.delete().where(user_group.c.user_id == target.id))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100),nullable=False)
    semester=db.Column(db.String)
    section_num=db.Column(db.Integer)
    course_instructor = db.Column(db.Integer, db.ForeignKey('user.id'))

    groups = db.relationship('Group', backref='course')

    def __repr__(self):
        return f"Course(id={self.id}, course_name='{self.course_name}', instructor_id='{self.course_instructor}')"

    def get_students(self):
        students = User.query.join(user_course, (user_course.c.user_id == User.id)
                            ).filter_by(user_course.c.course_id == self.id)
        
    def serialize(self):
        return {"id": self.id,
                "course_name": self.course_name,
                "semester": self.semester,
                "section_num": self.section_num,
                "course_instructor": self.course_instructor
                }


@event.listens_for(Course, 'before_delete')
def remove_users_from_course(mapper, connection, target):
    connection.execute(user_course.delete().where(user_course.c.course_id == target.id))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    def __repr__(self):
        return f"Group(id={self.id}, group_name='{self.group_name}', course_id={self.course_id})"

@event.listens_for(Group, 'before_delete')
def remove_users_from_group(mapper, connection, target):
    connection.execute(user_group.delete().where(user_group.c.group_id == target.id))

class Labs(db.Model):
    __tablename__="labs"
    lab_id=db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False , unique=True)
    questions=db.Column(db.String)
    answers=db.Column(db.String)
    lab_num=db.Column(db.Integer,nullable=False , unique=True)

class Student_lab (db.Model): 
   __tablename__= "student_answers"
   answer_id=db.Column(db.Integer, primary_key=True)
   question_num=db.Column(db.Integer)
   group_name=db.Column(db.String)
   course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
   submit_time =db.Column(db.TIMESTAMP)
   saved_answer=db.Column(db.String)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.lab_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String)